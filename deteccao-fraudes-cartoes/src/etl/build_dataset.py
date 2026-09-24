"""Unify — junta as tabelas e constrói o rótulo de fraude.

O rótulo vem de `contestacoes`: uma transação contestada é o proxy de
fraude disponível nesta base. Isso tem limites reais, documentados em
docs/escopo.md — nem toda contestação é fraude (pode ser erro de
cobrança ou arrependimento) e nem toda fraude é contestada.
"""
import pandas as pd

from src.config import COLUNA_ALVO
from src.utils.logger import get_logger

log = get_logger(__name__)


def adicionar_rotulo(transacoes: pd.DataFrame, contestacoes: pd.DataFrame) -> pd.DataFrame:
    """Marca 1 nas transações que aparecem em contestacoes."""
    contestadas = set(contestacoes["id_transacao"].dropna().unique())
    df = transacoes.copy()
    df[COLUNA_ALVO] = df["id_transacao"].isin(contestadas).astype("int8")

    positivos = int(df[COLUNA_ALVO].sum())
    log.info(
        "Rotulo: %s fraudes em %s transacoes (%.3f%%)",
        positivos, len(df), 100 * positivos / max(len(df), 1),
    )
    return df


def unificar(dfs: dict, transacoes_validas: pd.DataFrame) -> pd.DataFrame:
    """Junta transações com cartão, cliente, lojista e categoria.

    Os sufixos evitam a colisão de `nome`, que existe em clientes,
    lojistas e categorias — a mesma armadilha do Passo 3 da Aula 10.
    """
    df = transacoes_validas.merge(
        dfs["cartoes"][["id_cartao", "id_cliente"]], on="id_cartao", how="left"
    )
    df = df.merge(
        dfs["lojistas"].rename(columns={"nome": "nome_lojista"}),
        on="id_lojista", how="left",
    )
    df = df.merge(
        dfs["categorias"].rename(columns={"nome": "nome_categoria"}),
        on="id_categoria", how="left",
    )
    log.info("Base unificada: %s linhas, %s colunas", len(df), df.shape[1])
    return df
