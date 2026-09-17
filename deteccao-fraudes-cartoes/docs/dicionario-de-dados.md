# Dicionário de Dados

> Preencher/ajustar conforme a base escolhida (ver `docs/escopo.md`).

## Base bruta — `data/raw/transacoes.csv`
| Coluna | Tipo | Descrição | Observação |
|---|---|---|---|
| `id_transacao` | int | Identificador da transação | Chave |
| `tempo` | int/datetime | Momento da transação | Converter para timestamp no ETL |
| `valor` | float | Valor monetário | Base para KPIs financeiros |
| `v1 … vN` | float | Variáveis anonimizadas (PCA) | Dependem da base escolhida |
| `classe` | int | 0 = legítima, 1 = fraude | Variável alvo |

## Dataset tratado — `data/processed/transacoes_tratadas.parquet`
| Coluna | Tipo | Origem |
|---|---|---|
| Colunas da base bruta | — | Após limpeza e tipagem |
| `hora_do_dia` | int | Derivada de `tempo` |
| `faixa_valor` | categoria | Derivada de `valor` |
| `valor_padronizado` | float | Escalonamento |

## Saída do modelo — `data/processed/predicoes.csv` (fonte do Power BI)
| Coluna | Tipo | Descrição |
|---|---|---|
| `id_transacao` | int | Chave de ligação |
| `classe_real` | int | Rótulo observado (quando disponível) |
| `classe_prevista` | int | Previsão do modelo no limiar escolhido |
| `probabilidade_fraude` | float | Score entre 0 e 1 |
| `modelo` | string | Algoritmo que gerou a previsão |

## Métricas — `data/processed/metricas_modelo.csv`
| Coluna | Descrição |
|---|---|
| `modelo` | Nome do algoritmo |
| `metrica` | recall, precision, f1, auc_pr… |
| `valor` | Valor da métrica |
| `data_execucao` | Timestamp do treino |
