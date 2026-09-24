"""Transform com quarentena — nada é descartado sem deixar rastro.

Mesma ideia do pipeline PySpark da Aula 10: em vez de dropar linha
problemática com .dropna(), marcar o motivo e separar em duas tabelas.
Se alguém perguntar depois "por que sumiram N linhas?", a resposta está
em transacoes_rejeitadas.
"""
import pandas as pd

from src.config import COLUNA_TEMPO
from src.utils.logger import get_logger

log = get_logger(__name__)

OBRIGATORIAS = ["id_transacao", "id_cartao", "id_lojista", "valor", "data_hora"]


def marcar_motivo_rejeicao(transacoes: pd.DataFrame) -> pd.DataFrame:
    """Adiciona a coluna motivo_rejeicao (NaN = linha válida)."""
    df = transacoes.copy()

    nulo_obrigatorio = df[OBRIGATORIAS].isna().any(axis=1)
    duplicado = df.duplicated(subset="id_transacao", keep=False)
    valor_invalido = pd.to_numeric(df["valor"], errors="coerce").le(0)
    data_invalida = pd.to_datetime(df[COLUNA_TEMPO], errors="coerce").isna()

    # A ordem importa: o primeiro motivo que casar é o registrado.
    df["motivo_rejeicao"] = None
    for condicao, motivo in [
        (nulo_obrigatorio, "campo obrigatorio nulo"),
        (duplicado, "id_transacao duplicado"),
        (valor_invalido, "valor menor ou igual a zero"),
        (data_invalida, "data_hora invalida"),
    ]:
        sem_motivo = df["motivo_rejeicao"].isna()
        df.loc[sem_motivo & condicao.fillna(False), "motivo_rejeicao"] = motivo

    return df


def separar_quarentena(transacoes: pd.DataFrame):
    """Devolve (validas, rejeitadas)."""
    df = marcar_motivo_rejeicao(transacoes)
    rejeitadas = df[df["motivo_rejeicao"].notna()].copy()
    validas = df[df["motivo_rejeicao"].isna()].drop(columns=["motivo_rejeicao"]).copy()

    validas[COLUNA_TEMPO] = pd.to_datetime(validas[COLUNA_TEMPO])
    validas["valor"] = pd.to_numeric(validas["valor"])

    if len(rejeitadas):
        log.info("Quarentena — motivos:\n%s", rejeitadas["motivo_rejeicao"].value_counts())
    log.info("Validas: %s | Rejeitadas: %s", len(validas), len(rejeitadas))

    # Reconciliação: nenhuma linha some sem explicação.
    assert len(validas) + len(rejeitadas) == len(transacoes), "linha perdida na quarentena"
    return validas, rejeitadas
