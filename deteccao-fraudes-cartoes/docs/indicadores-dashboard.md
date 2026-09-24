# Indicadores do Dashboard

**Autores:** Breno Luna e Paula Carlesso

Fontes: `transacoes_dashboard.csv`, `predicoes.csv` e `metricas_modelo.csv`,
gerados em `data/processed/`. Medidas prontas em `powerbi/dax/medidas.dax`.

## Página 1 — Visão Geral
| Indicador | Medida DAX | Leitura |
|---|---|---|
| Total de transações | `Total Transacoes` | Volume analisado |
| Valor total | `Valor Total` | Exposição total |
| Transações suspeitas | `Transacoes Suspeitas` | Alertas gerados pelo modelo |
| Taxa de alerta | `Taxa de Alerta %` | Quanto da base cai na fila de revisão |
| Valor em risco | `Valor em Risco` | Soma das transações alertadas |
| Taxa de fraude real | `Taxa de Fraude Real %` | Contestações observadas |

Sempre lado a lado: **taxa de alerta** e **taxa de fraude real**. A distância
entre as duas é o custo operacional do modelo — se o modelo alerta 40% da base
para achar 1% de fraude, nenhuma equipe dá conta de revisar.

## Página 2 — Perfil da Fraude
- Fraudes por **faixa de valor** (`faixa_valor`)
- Fraudes por **hora do dia** e destaque de madrugada (`% na Madrugada`)
- Fraudes por **categoria de lojista** (`nome_categoria`)
- **Canal**: online x presencial (`% Online`)
- Transações com **padrão de teste de cartão** (`Transacoes com Padrao Teste de Cartao`)
- Tabela Top 50 por `probabilidade_fraude`, com formatação condicional

Esta página só existe porque a base tem campos de negócio — é a razão de termos
preferido a base do curso às bases anonimizadas do Kaggle.

## Página 3 — Desempenho do Modelo
| Métrica | Medida | Por que importa |
|---|---|---|
| Recall | `Recall` | % das fraudes capturadas — métrica principal |
| Precision | `Precision` | % dos alertas que eram fraude — custo da operação |
| F1 | `F1 Score` | Equilíbrio entre as duas |
| Matriz de confusão | VP/FP/FN/VN | Números absolutos |
| Valor não detectado | `Fraudes Nao Detectadas (Valor)` | Prejuízo que passou |
| Limiar | `Limiar Utilizado` | Deixa explícito o corte usado |

> Acurácia não entra como KPI. Com ~1% de fraude, um modelo que nunca acusa
> nada acerta 99% — e é inútil.

## Filtros globais
Período · faixa de valor · canal · categoria de lojista · classe prevista ·
faixa de probabilidade.
