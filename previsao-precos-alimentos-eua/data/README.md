# Dados

Só a estrutura das pastas e os CSVs do dashboard (`processed/powerbi/`) são versionados (ver `.gitignore`). O resto é gerado pelo pipeline.

## Como obter a base

1. Baixar o dataset **US Grocery and Gas Prices (2015-2026)** no Kaggle:
   https://www.kaggle.com/datasets/harshitsama/us-grocery-and-gas-prices-2015-2026
2. Extrair o zip em `data/raw/`. O pipeline só precisa de `us_average_prices_monthly.csv`.

Ou pela CLI do Kaggle:

```bash
kaggle datasets download harshitsama/us-grocery-and-gas-prices-2015-2026 -p data/raw --unzip
```

## Pastas

| Pasta | Conteúdo | Gerado por |
|---|---|---|
| `raw/` | CSVs originais do Kaggle | download manual |
| `interim/` | grade mensal, tabela de itens, séries rejeitadas | `src.etl.run_pipeline` |
| `processed/` | base de modelagem | `src.etl.run_pipeline` |
| `processed/powerbi/` | tabelas do dashboard | `src.models.evaluate` e `src.models.predict_model` |

A versão usada no projeto foi a atualizada no Kaggle em 06/09/2026 (dados até jul/2026).
