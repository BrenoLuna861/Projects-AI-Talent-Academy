# Plano de atividades

| Integrante | Frente principal |
|---|---|
| **Breno Luna** | ETL, modelagem e estrutura do repositório |
| **Paula Carlesso** | Análise exploratória, dashboard Power BI e documentação |

## Etapas

| # | Etapa | Entregável | Responsável | Status |
|---|---|---|---|---|
| 1 | Troca de tema e escopo | `docs/escopo.md` | Breno e Paula | Concluído |
| 2 | Base de dados | `data/README.md`, `docs/dicionario-de-dados.md` | Breno e Paula | Concluído |
| 3 | Análise exploratória | `notebooks/01_analise_exploratoria.ipynb` | Paula | Concluído |
| 4 | ETL | `src/etl/`, `notebooks/02_preparacao_dados.ipynb` | Breno | Concluído |
| 5 | Features | `src/features/build_features.py` | Breno | Concluído |
| 6 | Treino e comparação | `src/models/`, `notebooks/03_modelagem.ipynb` | Breno | Concluído |
| 7 | Backtest e exportação | `notebooks/04_avaliacao_e_export_powerbi.ipynb` | Breno e Paula | Concluído |
| 8 | Série temporal e granularidade | `notebooks/05_series_temporais_e_granularidade.ipynb`, `src/models/series_temporais.py` | Breno | Concluído |
| 9 | Dashboard | `powerbi/` | Paula | Em andamento |
| 10 | Apresentação final | slides | Breno e Paula | A fazer |

## Observações

- O dashboard consome só os CSVs de `data/processed/powerbi/`. Se o modelo mudar, basta rodar o pipeline de novo e atualizar as fontes no Power BI.
- Possível extensão se sobrar tempo: testar preços corrigidos pela inflação (CPI) e auto-ARIMA por item.
