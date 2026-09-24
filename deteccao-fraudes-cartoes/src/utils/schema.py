"""Validação de schema — falha cedo, com mensagem útil."""
import pandas as pd

from src.config import SCHEMA_ESPERADO
from src.utils.logger import get_logger

log = get_logger(__name__)


class SchemaInvalido(Exception):
    """A tabela não tem as colunas que o pipeline espera."""


def validar(nome_tabela: str, df: pd.DataFrame) -> None:
    """Confere se a tabela tem as colunas mínimas.

    Erra aqui, com o nome da coluna faltando, em vez de estourar um
    KeyError incompreensível três etapas adiante.
    """
    esperadas = SCHEMA_ESPERADO.get(nome_tabela, [])
    faltando = [c for c in esperadas if c not in df.columns]
    if faltando:
        raise SchemaInvalido(
            f"Tabela '{nome_tabela}': faltam as colunas {faltando}. "
            f"Colunas encontradas: {list(df.columns)}. "
            f"Se a base usa outros nomes, ajuste SCHEMA_ESPERADO em src/config.py."
        )
    log.info("Schema de '%s' OK (%s linhas, %s colunas)", nome_tabela, len(df), df.shape[1])


def validar_todas(dfs: dict) -> None:
    for nome, df in dfs.items():
        validar(nome, df)
