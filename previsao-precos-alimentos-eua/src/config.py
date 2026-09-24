"""Caminhos e parâmetros usados em todo o projeto."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DATA_DIR = RAIZ / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
POWERBI_DIR = PROCESSED_DIR / "powerbi"
MODELS_DIR = RAIZ / "models"
FIGURES_DIR = RAIZ / "reports" / "figures"

ARQUIVO_BRUTO = RAW_DIR / "us_average_prices_monthly.csv"
ARQUIVO_PRECOS = INTERIM_DIR / "precos_mensais.parquet"
ARQUIVO_REJEITADOS = INTERIM_DIR / "series_rejeitadas.csv"
ARQUIVO_ITENS = INTERIM_DIR / "itens.parquet"
ARQUIVO_MODELAGEM = PROCESSED_DIR / "base_modelagem.parquet"

# Quantos meses à frente o modelo prevê.
HORIZONTE = 3

# Tudo que tem data-alvo até aqui é treino; depois disso é teste.
FIM_TREINO = "2024-12-01"

# Série precisa de pelo menos isso de histórico para entrar na modelagem.
MIN_MESES_HISTORICO = 36

# Buracos de até N meses são interpolados; maiores ficam vazios.
MAX_MESES_INTERPOLACAO = 2

# Gasolina comum entra como variável externa para todos os itens.
SERIE_GASOLINA = "APU000074714"

SEED = 42


def garantir_pastas() -> None:
    for pasta in (INTERIM_DIR, PROCESSED_DIR, POWERBI_DIR, MODELS_DIR, FIGURES_DIR):
        pasta.mkdir(parents=True, exist_ok=True)
