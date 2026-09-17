# Layout das Páginas

## Página 1 — Visão Geral
```
┌────────────┬────────────┬────────────┬────────────┐
│ Transações │ Valor Total│ Suspeitas  │ Valor em   │
│   (KPI)    │   (KPI)    │   (KPI)    │ Risco (KPI)│
├────────────┴────────────┴────────────┴────────────┤
│ Evolução da taxa de fraude (linha, por dia)       │
├───────────────────────────┬───────────────────────┤
│ Fraudes por faixa de valor│ Fraudes por hora do   │
│ (barras)                  │ dia (colunas)         │
└───────────────────────────┴───────────────────────┘
Filtros laterais: período, faixa de valor, modelo
```

## Página 2 — Perfil da Fraude
- Mapa de calor hora x dia da semana
- Comparativo de ticket médio (fraude x legítima)
- Tabela Top 50 transações por `probabilidade_fraude`, com formatação condicional

## Página 3 — Desempenho do Modelo
- Cartões: Recall, Precision, F1
- Matriz de confusão (matriz com VP/FP/FN/VN)
- Gráfico comparando os modelos treinados (fMetricas)
- Cartão de destaque: valor das fraudes não detectadas
