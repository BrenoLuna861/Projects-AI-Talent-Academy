"""Extract — obtenção e leitura das seis tabelas."""
import pandas as pd

from src.config import DRIVE_IDS, RAW_DIR, TABELAS
from src.utils.logger import get_logger
from src.utils.schema import validar_todas

log = get_logger(__name__)


def baixar_do_drive(forcar: bool = False) -> None:
    """Baixa os CSVs do Google Drive, se ainda não estiverem em data/raw/."""
    try:
        import gdown
    except ImportError as exc:  # pragma: no cover
        raise ImportError("gdown não instalado. Rode: pip install gdown") from exc

    for arquivo, file_id in DRIVE_IDS.items():
        destino = RAW_DIR / arquivo
        if destino.exists() and not forcar:
            log.info("%s já existe, pulando download", arquivo)
            continue
        log.info("Baixando %s...", arquivo)
        gdown.download(f"https://drive.google.com/uc?id={file_id}", str(destino), quiet=True)


def carregar_tabelas(baixar_se_faltar: bool = True) -> dict:
    """Lê as seis tabelas de data/raw/ e valida o schema de cada uma."""
    faltando = [t for t in TABELAS if not (RAW_DIR / f"{t}.csv").exists()]
    if faltando:
        if not baixar_se_faltar:
            raise FileNotFoundError(f"Faltam CSVs em {RAW_DIR}: {faltando}")
        log.info("Faltando em data/raw/: %s — baixando do Drive", faltando)
        baixar_do_drive()

    dfs = {t: pd.read_csv(RAW_DIR / f"{t}.csv") for t in TABELAS}
    validar_todas(dfs)
    return dfs


if __name__ == "__main__":
    for nome, df in carregar_tabelas().items():
        print(f"{nome}: {df.shape}")
