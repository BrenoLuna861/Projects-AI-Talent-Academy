"""Transform — limpeza, tipagem e padronização."""
import pandas as pd

from src.config import COLUNA_ALVO
from src.utils.logger import get_logger

log = get_logger(__name__)


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.drop_duplicates()
    log.info("Duplicatas removidas: %s", antes - len(df))
    return df


def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    nulos = df.isna().sum()
    if nulos.any():
        log.info("Colunas com nulos:\n%s", nulos[nulos > 0])
    # estratégia a definir na EDA: imputação ou descarte
    return df


def padronizar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    if COLUNA_ALVO in df.columns:
        df[COLUNA_ALVO] = df[COLUNA_ALVO].astype("int8")
    return df


def transformar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica a sequência de transformações do ETL."""
    return df.pipe(remover_duplicatas).pipe(tratar_nulos).pipe(padronizar_tipos)
