# Plano de Atividades e Divisão do Grupo

## Integrantes
| Integrante | Frente principal |
|---|---|
| **Breno Luna** | ETL, modelagem e estrutura do repositório |
| **Paula Carlesso** | Análise exploratória, dashboard Power BI e documentação |

> Divisão proposta — ajustar na primeira reunião conforme a preferência de cada um.

## Etapas
| # | Etapa | Entregável | Responsável | Prazo | Status |
|---|---|---|---|---|---|
| 1 | Definição do tema e escopo | `docs/escopo.md` | Breno e Paula | — | ✅ Concluído |
| 2 | Escolha da base de dados | Base em `data/raw/` + `docs/dicionario-de-dados.md` | Breno e Paula | | ⬜ |
| 3 | Análise exploratória | `notebooks/01_analise_exploratoria.ipynb` | Paula | | ⬜ |
| 4 | ETL em Python | `src/etl/` + `data/processed/` | Breno | | ⬜ |
| 5 | Engenharia de atributos | `src/features/build_features.py` | Breno | | ⬜ |
| 6 | Treino e comparação de modelos | `notebooks/03_modelagem.ipynb`, `src/models/` | Breno | | ⬜ |
| 7 | Avaliação e escolha do limiar | `notebooks/04_avaliacao_e_export_powerbi.ipynb` | Breno e Paula | | ⬜ |
| 8 | Dashboard Power BI | `powerbi/dashboard-fraudes.pbix` | Paula | | ⬜ |
| 9 | Documentação e apresentação final | `README.md` + slides | Breno e Paula | | ⬜ |

## Observações

- A **escolha da base** (etapa 2) trava todas as outras: sem ela, nem a EDA nem o ETL avançam. É a primeira decisão a tomar.
- As etapas 3 e 4 podem correr em paralelo depois que a base estiver definida.
- A etapa 8 depende da 7: o dashboard consome `predicoes.csv` e `metricas_modelo.csv`.
- Preencher a coluna **Prazo** na primeira reunião e atualizar o **Status** a cada acompanhamento.
