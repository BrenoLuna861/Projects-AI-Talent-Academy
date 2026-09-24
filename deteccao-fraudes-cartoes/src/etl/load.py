"""Load — gravação dos datasets."""
from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger

log = get_logger(__name__)


def salvar(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if caminho.suffix == ".parquet":
        df.to_parquet(caminho, index=False)
    else:
        df.to_csv(caminho, index=False)
    log.info("Salvo: %s (%s linhas)", caminho.name, len(df))
