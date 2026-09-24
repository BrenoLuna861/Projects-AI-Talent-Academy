"""Caminhos, schema e parâmetros centrais do projeto."""
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

# --- as seis tabelas da base do curso ---
TABELAS = [
    "transacoes",
    "cartoes",
    "clientes",
    "lojistas",
    "categorias",
    "contestacoes",
]

# IDs no Google Drive (os mesmos usados nos notebooks das aulas)
DRIVE_IDS = {
    "cartoes.csv": "13Xf9ILhqxaIcvjq0vENJFCPD-HX-FLjM",
    "categorias.csv": "1NeAB_U66QnzRHZ1tJesP5lZ0jccXLAke",
    "clientes.csv": "1zgr0k17FdKp5aRkSd96qtLyJ9x0b4bFv",
    "contestacoes.csv": "1lSpAe8stD3JEMDJMFbiiYrQH0jYtHzT8",
    "lojistas.csv": "1vydqkbd2fONvNAfNKon9izr0pqaGBqhy",
    "transacoes.csv": "1OR3lgLjqVQZoajau2wrSExWPYc8xUsFS",
}

# Colunas mínimas que o pipeline exige de cada tabela.
# Se a base mudar de nome de coluna, é AQUI que se ajusta — e o
# validador em src/utils/schema.py acusa antes de o pipeline quebrar.
SCHEMA_ESPERADO = {
    "transacoes": ["id_transacao", "id_cartao", "id_lojista", "valor", "data_hora", "canal"],
    "cartoes": ["id_cartao", "id_cliente"],
    "clientes": ["id_cliente"],
    "lojistas": ["id_lojista", "id_categoria"],
    "categorias": ["id_categoria"],
    "contestacoes": ["id_transacao"],
}

# --- arquivos de saída ---
ARQUIVO_VALIDAS = INTERIM_DIR / "transacoes_validas.parquet"
ARQUIVO_REJEITADAS = INTERIM_DIR / "transacoes_rejeitadas.parquet"
ARQUIVO_DATASET = PROCESSED_DIR / "dataset_modelagem.parquet"
ARQUIVO_PREDICOES = PROCESSED_DIR / "predicoes.csv"
ARQUIVO_METRICAS = PROCESSED_DIR / "metricas_modelo.csv"
ARQUIVO_TRANSACOES_BI = PROCESSED_DIR / "transacoes_dashboard.csv"

# --- modelagem ---
COLUNA_ALVO = "fraude"
COLUNA_TEMPO = "data_hora"
SEED = 42
# Split TEMPORAL: os últimos 25% do período viram teste.
# Split aleatório em fraude é vazamento — o modelo treina com o futuro.
PROPORCAO_TESTE = 0.25
LIMIAR_DECISAO = 0.5  # ajustar após a curva precision-recall

# --- regras de negócio (aula 08) ---
VALOR_TESTE_CARTAO = 5.0      # transações de até R$5 = possível teste de cartão
MIN_TRANSACOES_TESTE = 4      # 4+ no mesmo cartão/lojista/dia
HORA_MADRUGADA_INICIO = 1
HORA_MADRUGADA_FIM = 3

for _d in (RAW_DIR, INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)
