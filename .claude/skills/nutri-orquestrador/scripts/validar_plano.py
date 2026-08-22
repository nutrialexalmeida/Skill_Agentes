#!/usr/bin/env python3
"""Valida um plano alimentar contra as metas do cálculo metabólico.

Confere, de forma determinística, tudo que é aritmética pura na auditoria:
somas, tolerâncias, uniformidade de proteína/gordura e pirâmide de
carboidrato. O que exige julgamento clínico continua com o auditor.

Uso:
    python validar_plano.py caso.json
    python validar_plano.py --stdin < caso.json

O arquivo de entrada é um único JSON contendo os blocos CALCULO e
PRESCRICAO no formato de HANDOFF.md:

    {"CALCULO": {...}, "PRESCRICAO": {...}}

Saída: relatório legível em stdout e um JSON com os achados em stderr
quando --json for passado.

Código de saída:
    0  plano aprovado em todos os testes automáticos
    1  ao menos uma falha encontrada
    2  entrada inválida (JSON malformado ou campo obrigatório ausente)

As tolerâncias vêm de calculos.json quando ele existir na raiz do
repositório da skill; caso contrário usam os padrões declarados abaixo.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Padrões usados quando calculos.json não está disponível. Cada valor tem
# origem declarada — nenhuma constante sem justificativa.
PADROES = {
    # Gate final do sistema: calorias reais dentro de ±2% da meta.
    "tolerancia_kcal_pct": 2.0,
    # Gate final do sistema: macros reais dentro de ±5% das metas.
    "tolerancia_macro_pct": 5.0,
    # Amplitude máxima entre a maior e a menor oferta de proteína ou gordura
    # entre refeições. 15% é o padrão assumido quando calculos.json não
    # define a tolerância versionada.
    "tolerancia_uniformidade_pct": 15.0,
    # Diferença abaixo da qual duas refeições são tratadas como empate na
    # pirâmide de carboidrato, para não reprovar por ruído de arredondamento
    # de gramas.
    "epsilon_carboidrato_g": 0.5,
}

MACROS = ("proteina", "carboidrato", "gordura")


class EntradaInvalida(Exception):
    """A entrada não tem a estrutura mínima para ser validada."""


def carregar_tolerancias(raiz: Path) -> dict:
    """Lê calculos.json se existir; senão devolve os padrões declarados."""
    tolerancias = dict(PADROES)
    arquivo = raiz / "calculos.json"
    if not arquivo.exists():
        tolerancias["_origem"] = "padroes internos (calculos.json ausente)"
        return tolerancias

    try:
        configurado = json.loads(arquivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise EntradaInvalida(
            f"calculos.json existe mas nao e um JSON valido: {erro}"
        ) from erro

    for chave in PADROES:
        if chave in configurado:
            tolerancias[chave] = configurado[chave]
    tolerancias["_origem"] = str(arquivo)
    return tolerancias


def exigir(dados: dict, chave: str, contexto: str):
    if chave not in dados:
        raise EntradaInvalida(f"campo obrigatorio ausente: {contexto}.{chave}")
    return dados[chave]


def desvio_pct(real: float, meta: float) -> float:
    """Desvio percentual do valor real em relação à meta.

    Meta zero é tratada como caso especial: qualquer valor real acima de
    zero é desvio infinito, e zero contra zero é desvio nulo.
    """
    if meta == 0:
        return 0.0 if real == 0 else float("inf")
    return (real - meta) / meta * 100.0


class Relatorio:
    def __init__(self) -> None:
        self.itens: list[dict] = []

    def registrar(self, item: str, passou: bool, evidencia: str) -> None:
        self.itens.append(
            {"item": item, "resultado": "passou" if passou else "falhou",
             "evidencia": evidencia}
        )

    @property
    def falhas(self) -> list[dict]:
        return [i for i in self.itens if i["resultado"] == "falhou"]

    def imprimir(self) -> None:
        for i in self.itens:
            marca = "OK  " if i["resultado"] == "passou" else "FALHA"
            print(f"[{marca}] {i['item']}")
            print(f"         {i['evidencia']}")
        print()
        if self.falhas:
            print(f"REPROVADO — {len(self.falhas)} falha(s) de {len(self.itens)} testes.")
        else:
            print(f"APROVADO nos {len(self.itens)} testes automaticos.")
            print("Os itens de julgamento clinico continuam com o auditor.")


def somar_alimentos(refeicao: dict, indice: int) -> dict:
    """Soma kcal e macros dos alimentos listados em uma refeição."""
    alimentos = exigir(refeicao, "alimentos", f"PRESCRICAO.refeicoes[{indice}]")
    total = {"kcal": 0.0, "proteina": 0.0, "carboidrato": 0.0, "gordura": 0.0}
    for alimento in alimentos:
        total["kcal"] += alimento.get("kcal", 0) or 0
        for macro in MACROS:
            total[macro] += alimento.get(f"{macro}_g", 0) or 0
    return total


def validar_somas(prescricao: dict, rel: Relatorio) -> list[dict]:
    """Confere se os totais declarados batem com a soma dos alimentos.

    Esta é a falha mais comum e a mais fácil de passar batido em revisão
    humana: um total declarado que não corresponde aos itens listados.
    """
    refeicoes = exigir(prescricao, "refeicoes", "PRESCRICAO")
    if not refeicoes:
        raise EntradaInvalida("PRESCRICAO.refeicoes esta vazio")

    somados = []
    for indice, refeicao in enumerate(refeicoes):
        nome = refeicao.get("nome", f"refeicao {indice + 1}")
        calculado = somar_alimentos(refeicao, indice)
        declarado = refeicao.get("totais", {})
        somados.append({"nome": nome, "calculado": calculado})

        divergencias = []
        for campo, valor in (
            ("kcal", calculado["kcal"]),
            ("proteina_g", calculado["proteina"]),
            ("carboidrato_g", calculado["carboidrato"]),
            ("gordura_g", calculado["gordura"]),
        ):
            informado = declarado.get(campo)
            if informado is None:
                divergencias.append(f"{campo} nao declarado")
            elif abs(informado - valor) > 0.5:
                divergencias.append(
                    f"{campo}: declarado {informado:.1f}, soma dos itens {valor:.1f}"
                )

        rel.registrar(
            f"Soma dos alimentos confere com os totais de '{nome}'",
            not divergencias,
            "; ".join(divergencias) if divergencias
            else f"kcal {calculado['kcal']:.0f}, P {calculado['proteina']:.1f} g, "
                 f"C {calculado['carboidrato']:.1f} g, G {calculado['gordura']:.1f} g",
        )
    return somados


def validar_totais_dia(prescricao: dict, somados: list[dict], rel: Relatorio) -> dict:
    """Confere se os totais do dia batem com a soma das refeições."""
    total = {"kcal": 0.0, "proteina": 0.0, "carboidrato": 0.0, "gordura": 0.0}
    for refeicao in somados:
        for chave in total:
            total[chave] += refeicao["calculado"][chave]

    declarado = prescricao.get("totais_dia", {})
    divergencias = []
    for campo, valor in (
        ("kcal", total["kcal"]),
        ("proteina_g", total["proteina"]),
        ("carboidrato_g", total["carboidrato"]),
        ("gordura_g", total["gordura"]),
    ):
        informado = declarado.get(campo)
        if informado is None:
            divergencias.append(f"{campo} nao declarado")
        elif abs(informado - valor) > 1.0:
            divergencias.append(
                f"{campo}: declarado {informado:.1f}, soma das refeicoes {valor:.1f}"
            )

    rel.registrar(
        "Totais do dia conferem com a soma das refeicoes",
        not divergencias,
        "; ".join(divergencias) if divergencias
        else f"kcal {total['kcal']:.0f}, P {total['proteina']:.1f} g, "
             f"C {total['carboidrato']:.1f} g, G {total['gordura']:.1f} g",
    )
    return total


def validar_metas(calculo: dict, real: dict, tol: dict, rel: Relatorio) -> None:
    """Confere as tolerâncias de ±2% em kcal e ±5% nos macros."""
    meta_kcal = exigir(calculo, "meta_energetica_kcal", "CALCULO")
    desvio = desvio_pct(real["kcal"], meta_kcal)
    limite = tol["tolerancia_kcal_pct"]
    rel.registrar(
        f"Calorias reais dentro de +-{limite}% da meta",
        abs(desvio) <= limite,
        f"meta {meta_kcal:.0f} kcal, real {real['kcal']:.0f} kcal, desvio {desvio:+.2f}%",
    )

    macros = exigir(calculo, "macros", "CALCULO")
    limite = tol["tolerancia_macro_pct"]
    for macro in MACROS:
        meta = exigir(macros, macro, "CALCULO.macros").get("g_dia")
        if meta is None:
            raise EntradaInvalida(f"CALCULO.macros.{macro}.g_dia ausente")
        desvio = desvio_pct(real[macro], meta)
        rel.registrar(
            f"{macro.capitalize()} real dentro de +-{limite}% da meta",
            abs(desvio) <= limite,
            f"meta {meta:.1f} g, real {real[macro]:.1f} g, desvio {desvio:+.2f}%",
        )


def validar_uniformidade(somados: list[dict], tol: dict, rel: Relatorio) -> None:
    """Confere se proteína e gordura estão uniformes entre as refeições.

    A amplitude é medida contra a média, não contra o menor valor: com duas
    refeições de 10 g e 30 g, medir contra o menor daria 200% e contra a
    média dá 100% — a média representa melhor o quanto a distribuição se
    afasta do uniforme quando há mais de duas refeições.
    """
    limite = tol["tolerancia_uniformidade_pct"]
    for macro in ("proteina", "gordura"):
        valores = [r["calculado"][macro] for r in somados]
        media = sum(valores) / len(valores)
        if media == 0:
            rel.registrar(
                f"{macro.capitalize()} uniforme entre as refeicoes",
                False,
                f"media de {macro} e zero — verifique se os alimentos foram preenchidos",
            )
            continue
        amplitude = (max(valores) - min(valores)) / media * 100.0
        maior = somados[valores.index(max(valores))]["nome"]
        menor = somados[valores.index(min(valores))]["nome"]
        rel.registrar(
            f"{macro.capitalize()} uniforme entre as refeicoes (amplitude <= {limite}%)",
            amplitude <= limite,
            f"maior '{maior}' {max(valores):.1f} g, menor '{menor}' {min(valores):.1f} g, "
            f"amplitude {amplitude:.1f}% da media {media:.1f} g",
        )


def validar_piramide(somados: list[dict], modo: str, tol: dict, rel: Relatorio) -> None:
    """Confere a pirâmide de carboidrato, par a par.

    Comparar par a par, e não apenas primeira contra última, é o que detecta
    uma subida no meio do dia — que "no geral decrescente" esconderia.
    """
    epsilon = tol["epsilon_carboidrato_g"]
    quebras = []
    for anterior, atual in zip(somados, somados[1:]):
        carb_ant = anterior["calculado"]["carboidrato"]
        carb_at = atual["calculado"]["carboidrato"]
        if carb_at >= carb_ant - epsilon:
            quebras.append(
                f"'{anterior['nome']}' {carb_ant:.1f} g -> "
                f"'{atual['nome']}' {carb_at:.1f} g"
            )

    if modo == "padrao":
        rel.registrar(
            "Carboidrato estritamente decrescente da primeira a ultima refeicao",
            not quebras,
            "; ".join(quebras) if quebras
            else " > ".join(f"{r['calculado']['carboidrato']:.1f}" for r in somados) + " g",
        )
    else:
        rel.registrar(
            f"Modo '{modo}': quebra da piramide permitida, exige justificativa",
            True,
            f"{len(quebras)} quebra(s) encontrada(s) — o auditor confere a "
            f"justificativa e as refeicoes estrategicas em referencia/modos-especiais.md",
        )


def validar_gramas_explicitas(prescricao: dict, rel: Relatorio) -> None:
    """Confere que todo alimento tem gramas e nenhum usa medida vaga."""
    vagos = {"livre", "a vontade", "à vontade", "q.b.", "a gosto"}
    problemas = []
    for refeicao in prescricao.get("refeicoes", []):
        nome_ref = refeicao.get("nome", "?")
        for alimento in refeicao.get("alimentos", []):
            nome = alimento.get("alimento", "?")
            gramas = alimento.get("gramas")
            if gramas is None or gramas <= 0:
                problemas.append(f"'{nome}' em '{nome_ref}' sem gramas")
            medida = str(alimento.get("medida_caseira", "")).strip().lower()
            if medida in vagos:
                problemas.append(f"'{nome}' em '{nome_ref}' com medida vaga: '{medida}'")

    rel.registrar(
        "Todos os alimentos tem gramas explicitas e nenhuma medida vaga",
        not problemas,
        "; ".join(problemas) if problemas else "nenhum item sem gramas ou com medida vaga",
    )


def validar(caso: dict, tol: dict) -> Relatorio:
    rel = Relatorio()
    calculo = exigir(caso, "CALCULO", "raiz")
    prescricao = exigir(caso, "PRESCRICAO", "raiz")
    modo = prescricao.get("modo", "padrao")

    somados = validar_somas(prescricao, rel)
    real = validar_totais_dia(prescricao, somados, rel)
    validar_metas(calculo, real, tol, rel)
    validar_uniformidade(somados, tol, rel)
    validar_piramide(somados, modo, tol, rel)
    validar_gramas_explicitas(prescricao, rel)
    return rel


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("arquivo", nargs="?", help="JSON com os blocos CALCULO e PRESCRICAO")
    parser.add_argument("--stdin", action="store_true", help="ler a entrada de stdin")
    parser.add_argument("--json", action="store_true", help="emitir os achados como JSON em stderr")
    parser.add_argument(
        "--raiz", default=".",
        help="raiz do repositorio da skill, onde calculos.json e procurado (padrao: .)",
    )
    args = parser.parse_args()

    if not args.stdin and not args.arquivo:
        parser.error("informe um arquivo ou use --stdin")

    try:
        bruto = sys.stdin.read() if args.stdin else Path(args.arquivo).read_text(encoding="utf-8")
    except OSError as erro:
        print(f"erro ao ler a entrada: {erro}", file=sys.stderr)
        return 2

    try:
        caso = json.loads(bruto)
    except json.JSONDecodeError as erro:
        print(f"entrada nao e um JSON valido: {erro}", file=sys.stderr)
        return 2

    try:
        tolerancias = carregar_tolerancias(Path(args.raiz))
        relatorio = validar(caso, tolerancias)
    except EntradaInvalida as erro:
        print(f"entrada invalida: {erro}", file=sys.stderr)
        return 2

    print(f"Tolerancias: {tolerancias['_origem']}")
    print()
    relatorio.imprimir()

    if args.json:
        json.dump(
            {"itens": relatorio.itens, "falhas": relatorio.falhas},
            sys.stderr, ensure_ascii=False, indent=2,
        )
        print(file=sys.stderr)

    return 1 if relatorio.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
