"""Extract — leitura da base bruta."""
import pandas as pd

from src.config import ARQUIVO_BRUTO
from src.utils.logger import get_logger

log = get_logger(__name__)


def carregar_dados_brutos(caminho=ARQUIVO_BRUTO) -> pd.DataFrame:
    """Lê a base bruta de transações."""
    log.info("Lendo base bruta: %s", caminho)
    df = pd.read_csv(caminho)
    log.info("Linhas: %s | Colunas: %s", len(df), df.shape[1])
    return df


if __name__ == "__main__":
    carregar_dados_brutos().info()
