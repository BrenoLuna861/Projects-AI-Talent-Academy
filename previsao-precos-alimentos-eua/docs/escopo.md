# Escopo do projeto

**Autores:** Breno Luna e Paula Carlesso

## Tema

Previsão de preços médios de alimentos e energia nos EUA com machine learning, com
os resultados em um dashboard no Power BI.

## Histórico da escolha

O primeiro tema do grupo foi detecção de fraude em cartão. Na revisão, o professor
apontou que as bases públicas de fraude são muito manjadas e sugeriu trabalhar com uma
base como a de preços do BLS publicada no Kaggle em set/2026. Trocamos o tema e
aproveitamos a estrutura de pipeline (ETL, features, modelos, exportação para o Power BI)
que já estava montada.

## Objetivo geral

Analisar o preço médio de cada item como série temporal (o valor que ele teve e o que
pode vir a ter), prever esse preço com 3 meses de antecedência e mostrar, no dashboard, a
evolução histórica, a previsão e o quanto dá para confiar nela.

## Para quem é

Analista de compras e custos de uma rede de supermercados ou restaurantes nos EUA. Precisa saber se
o preço dos itens que compra vai subir ou cair nos próximos meses para negociar com fornecedores,
antecipar compras ou ajustar preços de venda. No dashboard, usa a previsão por produto, a faixa
provável (risco), a sazonalidade (melhor época de comprar) e a página de confiabilidade (em quais
produtos dá para confiar na previsão).

## Objetivos específicos

1. Entender a base: cobertura das séries, buracos, erros de categoria, sazonalidade e volatilidade.
2. Montar um ETL reprodutível que trate os buracos e corrija as categorias.
3. Treinar pelo menos três algoritmos de ML e comparar com duas regras simples (ingênuo e sazonal).
4. Analisar as séries como séries temporais (decomposição, estacionariedade, autocorrelação), comparar com modelos clássicos (SARIMA, Holt-Winters) e definir a granularidade adequada.
5. Validar com separação temporal e mais de um período de teste.
6. Publicar histórico, previsões e métricas no Power BI.

## Perguntas que o projeto responde

- Quais itens e categorias mais subiram de 2015 a 2026? Quais ficaram abaixo da inflação?
- Quais são os mais voláteis e quais têm sazonalidade?
- A gasolina ajuda a prever o preço dos alimentos?
- Um modelo de ML consegue prever melhor que "o preço de daqui a 3 meses é o de hoje"? Em quais categorias?
- Modelos clássicos de série temporal funcionam melhor que ML aqui? E combinados?
- Qual granularidade prevê melhor: mensal ou trimestral? Item específico ou agregado?
- O que o modelo espera para os próximos 3 meses?

## Decisões de modelagem

| Decisão | Motivo |
|---|---|
| Horizonte de 3 meses | Testamos 1, 3 e 6 meses (erro do ingênuo: ~2%, ~4% e ~6%). Com 1 mês a previsão quase não difere do preço atual; 3 meses é o meio-termo entre utilidade e erro. |
| Alvo = variação em log, não o preço | Permite um único modelo para itens de US$ 0,20 (kWh) a US$ 14,59 (libra de sirloin). |
| Um modelo global para todas as séries | Cada série tem no máximo 139 meses; separadas, teriam pouco dado. |
| Treino até dez/2024, teste a partir dele | Separação temporal; no teste o modelo nunca viu preço posterior ao mês-base. |
| Backtest com cortes em 2021, 2022 e 2023 | Um único período de teste pode ter dado sorte. |
| WAPE como métrica principal | Soma dos erros / soma dos preços. Não explode em itens baratos como o MAPE. |
| Modelo final = menor WAPE médio nos cortes | Estabilidade pesa mais que vencer um único período. O vencedor foi a média de gradient boosting e SARIMA. |
| Granularidade mensal | É a mais fina publicada; no teste, dados mensais previram o trimestre seguinte melhor que dados trimestrais (notebook 05). |
| SARIMA(1,1,1)(0,1,1)12 no log do preço | Diferença simples e sazonal deixam a série estacionária (ADF); ordem baixa para não sobreajustar séries de ~130 meses. |

## Premissas e limitações

- Preços nominais em dólar; não corrigimos pela inflação.
- Média nacional (U.S. city average).
- O modelo usa só o histórico de preços. Não tem dados de clima, safra, câmbio, tarifas ou surtos de gripe aviária.
- Séries descontinuadas ou com mais de 25% de meses faltando ficam fora da modelagem, mas entram no dashboard histórico.

## Fora do escopo

- Previsão por região ou por loja.
- Atualização automática mensal da base.
- Busca automática da melhor ordem de SARIMA por item (auto-ARIMA) e Prophet. Usamos uma ordem fixa para todas as séries.

## Critérios de conclusão

- Pipeline executável de ponta a ponta com um comando por etapa.
- Três algoritmos de ML e dois modelos clássicos de série temporal comparados com os baselines.
- Análise de série temporal (STL, ADF, ACF/PACF) e de granularidade documentada.
- Testes automatizados, incluindo o de vazamento de informação do futuro.
- Dashboard no Power BI com histórico, previsão e desempenho do modelo.
