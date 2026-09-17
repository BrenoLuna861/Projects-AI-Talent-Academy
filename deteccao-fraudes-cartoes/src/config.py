"""Caminhos e parâmetros centrais do projeto."""
from pathlib import Path

# --- diretórios ---
RAIZ = Path(__file__).resolve().parents[1]
DATA_DIR = RAIZ / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = RAIZ / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = RAIZ / "models"

# --- arquivos ---
ARQUIVO_BRUTO = RAW_DIR / "transacoes.csv"
ARQUIVO_TRATADO = PROCESSED_DIR / "transacoes_tratadas.parquet"
ARQUIVO_PREDICOES = PROCESSED_DIR / "predicoes.csv"
ARQUIVO_METRICAS = PROCESSED_DIR / "metricas_modelo.csv"

# --- parâmetros ---
COLUNA_ALVO = "classe"
SEED = 42
TAMANHO_TESTE = 0.25
LIMIAR_DECISAO = 0.5  # ajustar após a curva precision-recall

for _d in (INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
