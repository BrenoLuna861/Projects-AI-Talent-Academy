"""Engenharia de atributos para o modelo e para o dashboard."""
import numpy as np
import pandas as pd

from src.utils.logger import get_logger

log = get_logger(__name__)

FAIXAS_VALOR = [0, 50, 200, 1000, np.inf]
ROTULOS_FAIXA = ["ate_50", "50_a_200", "200_a_1000", "acima_1000"]


def adicionar_hora_do_dia(df: pd.DataFrame, coluna_tempo: str = "tempo") -> pd.DataFrame:
    """Deriva a hora do dia a partir da coluna de tempo (segundos ou datetime)."""
    if coluna_tempo not in df.columns:
        return df
    if np.issubdtype(df[coluna_tempo].dtype, np.number):
        df["hora_do_dia"] = (df[coluna_tempo] // 3600 % 24).astype("int8")
    else:
        df["hora_do_dia"] = pd.to_datetime(df[coluna_tempo]).dt.hour.astype("int8")
    return df


def adicionar_faixa_valor(df: pd.DataFrame, coluna_valor: str = "valor") -> pd.DataFrame:
    if coluna_valor in df.columns:
        df["faixa_valor"] = pd.cut(
            df[coluna_valor], bins=FAIXAS_VALOR, labels=ROTULOS_FAIXA, right=False
        )
    return df


def construir_features(df: pd.DataFrame) -> pd.DataFrame:
    df = adicionar_hora_do_dia(df)
    df = adicionar_faixa_valor(df)
    log.info("Features criadas. Colunas finais: %s", df.shape[1])
    return df
