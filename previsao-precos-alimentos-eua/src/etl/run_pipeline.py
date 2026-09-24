"""ETL completo: bruto -> grade mensal -> itens -> base de modelagem.

    python -m src.etl.run_pipeline
"""
from src.config import (
    ARQUIVO_ITENS,
    ARQUIVO_MODELAGEM,
    ARQUIVO_PRECOS,
    ARQUIVO_REJEITADOS,
    garantir_pastas,
)
from src.etl.extract import carregar_bruto
from src.etl.load import salvar
from src.etl.transform import (
    motivo_exclusao_modelagem,
    padronizar,
    regularizar_grade,
    resumir_itens,
    validar_linhas,
)
from src.features.build_features import construir_base
from src.utils.logger import get_logger

log = get_logger(__name__)


def main() -> None:
    garantir_pastas()

    bruto = carregar_bruto()
    df = padronizar(bruto)
    df, linhas_rejeitadas = validar_linhas(df)
    precos = regularizar_grade(df)
    itens = resumir_itens(precos)

    itens["motivo_exclusao"] = motivo_exclusao_modelagem(itens)
    fora = itens[itens["motivo_exclusao"].notna()]
    log.info("Séries fora da modelagem: %s de %s", len(fora), len(itens))
    for motivo, n in fora["motivo_exclusao"].value_counts().items():
        log.info("  %s: %s", motivo, n)

    series_ok = itens.loc[itens["motivo_exclusao"].isna(), "serie_id"]
    base = construir_base(precos, series_ok)

    salvar(precos, ARQUIVO_PRECOS)
    salvar(itens, ARQUIVO_ITENS)
    salvar(fora[["serie_id", "item", "inicio", "fim", "meses_publicados", "motivo_exclusao"]], ARQUIVO_REJEITADOS)
    if len(linhas_rejeitadas):
        salvar(linhas_rejeitadas, ARQUIVO_REJEITADOS.with_name("linhas_rejeitadas.csv"))
    salvar(base, ARQUIVO_MODELAGEM)


if __name__ == "__main__":
    main()
