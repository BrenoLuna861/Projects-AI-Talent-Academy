# Plano de Atividades e Divisão do Grupo

## Etapas
| # | Etapa | Entregável | Responsável | Prazo | Status |
|---|---|---|---|---|---|
| 1 | Definição do tema e escopo | `docs/escopo.md` | Grupo | — | ✅ Concluído |
| 2 | Escolha da base de dados | Base em `data/raw/` + `docs/dicionario-de-dados.md` | | | ⬜ |
| 3 | Análise exploratória | `notebooks/01_analise_exploratoria.ipynb` | | | ⬜ |
| 4 | ETL em Python | `src/etl/` + `data/processed/` | | | ⬜ |
| 5 | Engenharia de atributos | `src/features/build_features.py` | | | ⬜ |
| 6 | Treino e comparação de modelos | `notebooks/03_modelagem.ipynb`, `src/models/` | | | ⬜ |
| 7 | Avaliação e escolha do limiar | `notebooks/04_avaliacao_e_export_powerbi.ipynb` | | | ⬜ |
| 8 | Dashboard Power BI | `powerbi/dashboard-fraudes.pbix` | | | ⬜ |
| 9 | Documentação e apresentação final | `README.md` + slides | Grupo | | ⬜ |

## Papéis sugeridos
- **Dados/ETL** — base, limpeza, pipeline, dicionário de dados.
- **Modelagem** — features, treino, tuning, métricas.
- **Dashboard/BI** — modelo semântico, medidas DAX, layout e narrativa.
- **Documentação** — README, relatórios de acompanhamento, apresentação.

> Preencher as colunas *Responsável* e *Prazo* na primeira reunião após a escolha da base.
