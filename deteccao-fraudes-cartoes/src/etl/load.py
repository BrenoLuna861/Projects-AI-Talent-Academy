"""Load — gravação dos dados tratados."""
import pandas as pd

from src.config import ARQUIVO_TRATADO
from src.utils.logger import get_logger

log = get_logger(__name__)


def salvar_tratado(df: pd.DataFrame, caminho=ARQUIVO_TRATADO) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(caminho, index=False)
    log.info("Dataset tratado salvo em %s (%s linhas)", caminho, len(df))
