# Indicadores do Dashboard

## Página 1 — Visão Geral do Negócio
| Indicador | Cálculo | Leitura |
|---|---|---|
| Total de transações | Contagem de linhas | Volume analisado |
| Valor total transacionado | Soma de `valor` | Exposição total |
| Transações suspeitas | Contagem onde `classe_prevista = 1` | Alertas gerados |
| Taxa de fraude (%) | Suspeitas / Total | Incidência |
| Valor em risco | Soma de `valor` das suspeitas | Impacto financeiro |
| Ticket médio — fraude x legítima | Média de `valor` por classe | Perfil da fraude |

## Página 2 — Perfil da Fraude
- Fraudes por **faixa de valor** (barras)
- Fraudes por **hora do dia** (coluna/linha)
- Evolução diária/semanal da **taxa de fraude** (linha)
- Concentração por categoria ou canal, quando a base permitir (treemap)
- Top N transações por probabilidade de fraude (tabela detalhada)

## Página 3 — Desempenho do Modelo
| Métrica | Por que importa neste problema |
|---|---|
| Recall (sensibilidade) | % das fraudes reais que o modelo capturou — métrica principal |
| Precision | % dos alertas que eram fraude de fato — mede o custo operacional |
| F1-Score | Equilíbrio entre as duas |
| AUC-PR | Mais informativa que ROC em base desbalanceada |
| Matriz de confusão | VP, FP, VN, FN em números absolutos |
| Curva Precision-Recall por limiar | Apoia a escolha do ponto de corte |

> **Atenção:** acurácia não entra como KPI principal. Com ~0,2% de fraudes, um
> modelo que nunca acusa fraude ainda acerta 99,8% — e é inútil.

## Filtros globais sugeridos
Período, faixa de valor, hora do dia, classe prevista, faixa de probabilidade.
