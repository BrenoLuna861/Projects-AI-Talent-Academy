# Indicadores do dashboard

Filtros em todas as páginas: categoria, item, período.

## Página 1 - Panorama de preços

| Indicador | Cálculo |
|---|---|
| Itens acompanhados | Contagem de séries ativas |
| Variação mediana (12m inicial x 12m final) | Mediana de `variacao_12m_pct` |
| Itens acima da inflação | Séries com variação > 35% (CPI-U no período) |
| Maior alta | Item com maior `variacao_12m_pct` |

Visuais:
- Linha: índice por categoria (média de 2019 = 100)
- Barras: variação por categoria, com linha de referência da inflação
- Tabela: itens, preço atual, variação, ativa/descontinuada

## Página 2 - Volatilidade e sazonalidade

- Linha do item selecionado com os meses interpolados destacados
- Matriz categoria x mês com o desvio sazonal médio
- Ranking de volatilidade mensal (desvio-padrão da variação mês a mês)

## Página 3 - Previsão

| Indicador | Cálculo |
|---|---|
| Preço atual | Último `preco` do item |
| Preço previsto | `preco_previsto` de `previsao_futura` |
| Variação prevista | `variacao_prevista_pct` |
| Faixa provável | `faixa_inferior` a `faixa_superior` |

Visuais:
- Linha com histórico + ponto previsto e faixa (barra de erro)
- Barras: variação prevista por categoria
- Tabela das maiores altas e quedas previstas

## Página 4 - Confiabilidade do modelo

| Métrica | Por que importa |
|---|---|
| WAPE | Erro médio ponderado pelo preço. Métrica principal. |
| Ganho sobre o ingênuo | Se não for positivo, o modelo não agrega nada |
| % de séries em que o modelo ganha do ingênuo | Mostra se o ganho é geral ou puxado por poucos itens |
| Viés | Se o modelo tende a prever alto ou baixo |

Visuais:
- Colunas: WAPE por corte de backtest e modelo
- Barras: WAPE por categoria, modelo final x ingênuo
- Linha: real x previsto no período de teste para o item selecionado

> Acurácia e R² não entram: com preços que mudam poucos % ao mês, o R² sobre o preço
> fica perto de 1 para qualquer modelo e não diz nada. A comparação com o ingênuo é o
> que mostra se o modelo tem valor.
