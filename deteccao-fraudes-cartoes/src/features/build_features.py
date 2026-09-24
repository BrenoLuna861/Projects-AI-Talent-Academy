"""Engenharia de atributos — só com informação disponível ANTES da transação.

Regra que governa este arquivo: nenhuma feature pode usar o futuro.
Uma média "do cartão" calculada sobre a base inteira inclui transações
que ainda não aconteceram no momento da compra — o modelo fica ótimo no
teste e inútil na vida real. Por isso todo agregado aqui é expanding +
shift(1): olha só o passado daquela linha.
"""
import numpy as np
import pandas as pd

from src.config import (
    COLUNA_TEMPO,
    HORA_MADRUGADA_FIM,
    HORA_MADRUGADA_INICIO,
    MIN_TRANSACOES_TESTE,
    VALOR_TESTE_CARTAO,
)
from src.utils.logger import get_logger

log = get_logger(__name__)

FAIXAS_VALOR = [0, 50, 200, 1000, np.inf]
ROTULOS_FAIXA = ["ate_50", "50_a_200", "200_a_1000", "acima_1000"]


def features_temporais(df: pd.DataFrame) -> pd.DataFrame:
    dt = pd.to_datetime(df[COLUNA_TEMPO])
    df["hora_do_dia"] = dt.dt.hour.astype("int8")
    df["dia_semana"] = dt.dt.dayofweek.astype("int8")
    df["fim_de_semana"] = (df["dia_semana"] >= 5).astype("int8")
    df["madrugada"] = (
        (df["hora_do_dia"] >= HORA_MADRUGADA_INICIO) & (df["hora_do_dia"] < HORA_MADRUGADA_FIM)
    ).astype("int8")
    df["data"] = dt.dt.date
    return df


def features_valor(df: pd.DataFrame) -> pd.DataFrame:
    df["faixa_valor"] = pd.cut(df["valor"], bins=FAIXAS_VALOR, labels=ROTULOS_FAIXA, right=False)
    df["log_valor"] = np.log1p(df["valor"])
    df["valor_baixo"] = (df["valor"] <= VALOR_TESTE_CARTAO).astype("int8")
    return df


def features_historicas_cartao(df: pd.DataFrame) -> pd.DataFrame:
    """Comportamento passado do cartão, sem olhar o futuro."""
    df = df.sort_values(COLUNA_TEMPO).reset_index(drop=True)
    g = df.groupby("id_cartao")["valor"]

    df["media_valor_cartao_ate_agora"] = g.transform(lambda s: s.expanding().mean().shift(1))
    df["qtd_transacoes_cartao_ate_agora"] = g.transform(lambda s: s.expanding().count().shift(1))
    df["razao_valor_media_cartao"] = df["valor"] / df["media_valor_cartao_ate_agora"]

    # Tempo desde a transação anterior do mesmo cartão (em minutos)
    anterior = df.groupby("id_cartao")[COLUNA_TEMPO].shift(1)
    df["minutos_desde_ultima_do_cartao"] = (
        (pd.to_datetime(df[COLUNA_TEMPO]) - pd.to_datetime(anterior)).dt.total_seconds() / 60
    )
    return df


def feature_teste_de_cartao(df: pd.DataFrame) -> pd.DataFrame:
    """Padrão de 'teste de cartão' encontrado na Aula 08.

    4+ transações de até R$5 no mesmo cartão, mesmo lojista, mesmo dia.
    Contamos apenas as ocorrências ANTERIORES dentro do grupo, para não
    usar o resto do dia como informação.
    """
    df["_baixo"] = df["valor"] <= VALOR_TESTE_CARTAO
    contagem_ate_agora = (
        df.sort_values(COLUNA_TEMPO)
        .groupby(["id_cartao", "id_lojista", "data"])["_baixo"]
        .transform(lambda s: s.cumsum().shift(1).fillna(0))
    )
    df["baixos_no_dia_ate_agora"] = contagem_ate_agora.astype(float)
    df["padrao_teste_cartao"] = (
        df["baixos_no_dia_ate_agora"] >= (MIN_TRANSACOES_TESTE - 1)
    ).astype("int8")
    return df.drop(columns=["_baixo"])


def features_lojista(df: pd.DataFrame, coluna_alvo: str | None = None) -> pd.DataFrame:
    """Histórico do lojista até aquela transação.

    Se o alvo estiver disponível (treino), calcula a taxa de contestação
    histórica — também expanding + shift, senão é vazamento direto do
    rótulo para dentro da feature.
    """
    df = df.sort_values(COLUNA_TEMPO).reset_index(drop=True)
    df["qtd_transacoes_lojista_ate_agora"] = (
        df.groupby("id_lojista")["valor"].transform(lambda s: s.expanding().count().shift(1))
    )
    if coluna_alvo and coluna_alvo in df.columns:
        df["taxa_contestacao_lojista_ate_agora"] = (
            df.groupby("id_lojista")[coluna_alvo]
            .transform(lambda s: s.expanding().mean().shift(1))
        )
    return df


COLUNAS_MODELO = [
    "valor",
    "log_valor",
    "hora_do_dia",
    "dia_semana",
    "fim_de_semana",
    "madrugada",
    "valor_baixo",
    "media_valor_cartao_ate_agora",
    "qtd_transacoes_cartao_ate_agora",
    "razao_valor_media_cartao",
    "minutos_desde_ultima_do_cartao",
    "baixos_no_dia_ate_agora",
    "padrao_teste_cartao",
    "qtd_transacoes_lojista_ate_agora",
    "taxa_contestacao_lojista_ate_agora",
    "canal_online",
]


def construir_features(df: pd.DataFrame, coluna_alvo: str | None = None) -> pd.DataFrame:
    df = features_temporais(df)
    df = features_valor(df)
    df = features_historicas_cartao(df)
    df = feature_teste_de_cartao(df)
    df = features_lojista(df, coluna_alvo)
    df["canal_online"] = (
        df["canal"].astype(str).str.lower().str.strip().eq("online").astype("int8")
    )
    log.info("Features construidas. Colunas: %s", df.shape[1])
    return df
