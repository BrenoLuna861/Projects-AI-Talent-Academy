"""Leitura do arquivo bruto (formato longo) com checagem de schema."""
import pandas as pd

from src.config import ARQUIVO_BRUTO
from src.utils.logger import get_logger

log = get_logger(__name__)

COLUNAS_ESPERADAS = ["date", "year", "month", "item", "unit", "category", "price", "series_id"]


def carregar_bruto(caminho=ARQUIVO_BRUTO) -> pd.DataFrame:
    if not caminho.exists():
        raise FileNotFoundError(
            f"{caminho} não encontrado. Baixe o dataset do Kaggle e extraia em data/raw/ "
            "(instruções em data/README.md)."
        )
    df = pd.read_csv(caminho, dtype={"series_id": str})

    faltando = set(COLUNAS_ESPERADAS) - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas ausentes no arquivo bruto: {sorted(faltando)}")

    log.info("Bruto: %s linhas, %s séries", len(df), df["series_id"].nunique())
    return df
