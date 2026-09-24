# Dados

Nada aqui é versionado (ver `.gitignore`) — cada integrante gera localmente.

| Pasta | Conteúdo |
|---|---|
| `raw/` | As seis tabelas originais do curso, baixadas do Drive |
| `interim/` | `transacoes_validas.parquet` e `transacoes_rejeitadas.parquet` (quarentena) |
| `processed/` | `dataset_modelagem.parquet` e os CSVs que o Power BI consome |
| `external/` | Dados de apoio, se houver |

## Como obter a base

O download é automático — basta rodar o pipeline:

```bash
python -m src.etl.run_pipeline
```

`src/etl/extract.py` baixa os seis CSVs do Google Drive usando os mesmos IDs
dos notebooks das aulas. Se já existirem em `raw/`, ele pula o download.

Sem acesso ao Drive, use a base sintética de mesmo schema:

```bash
python -m tools.gerar_dados_exemplo --linhas 20000 --destino data/raw
```

> Base sintética serve para testar o código. Os números dela **não** valem como
> resultado do projeto.

## A base

Seis tabelas relacionais de fraude em cartão, usadas nas aulas 2, 5, 6, 7, 8, 9
e 10 do AI Talent Academy. Schema completo em `docs/dicionario-de-dados.md`.
