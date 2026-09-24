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

Prever o preço médio de cada item com 3 meses de antecedência e mostrar, no dashboard,
a evolução histórica, a previsão e o quanto dá para confiar nela.

## Objetivos específicos

1. Entender a base: cobertura das séries, buracos, erros de categoria, sazonalidade e volatilidade.
2. Montar um ETL reprodutível que trate os buracos e corrija as categorias.
3. Treinar pelo menos três algoritmos e comparar com duas regras simples (ingênuo e sazonal).
4. Validar com separação temporal e mais de um período de teste.
5. Publicar histórico, previsões e métricas no Power BI.

## Perguntas que o projeto responde

- Quais itens e categorias mais subiram de 2015 a 2026? Quais ficaram abaixo da inflação?
- Quais são os mais voláteis e quais têm sazonalidade?
- A gasolina ajuda a prever o preço dos alimentos?
- Um modelo de ML consegue prever melhor que "o preço de daqui a 3 meses é o de hoje"? Em quais categorias?
- O que o modelo espera para os próximos 3 meses?

## Decisões de modelagem

| Decisão | Motivo |
|---|---|
| Horizonte de 3 meses | Testamos 1, 3 e 6 meses (WAPE do ingênuo: 2,3%, 4,3% e 6,4%). Com 1 mês a previsão quase não difere do preço atual; 3 meses é o meio-termo entre utilidade e erro. |
| Alvo = variação em log, não o preço | Permite um único modelo para itens de US$ 0,20 (kWh) a US$ 14,59 (libra de sirloin). |
| Um modelo global para todas as séries | Cada série tem no máximo 139 meses; separadas, teriam pouco dado. |
| Treino até dez/2024, teste a partir dele | Separação temporal; no teste o modelo nunca viu preço posterior ao mês-base. |
| Backtest com cortes em 2021, 2022 e 2023 | Um único período de teste pode ter dado sorte. |
| WAPE como métrica principal | Soma dos erros / soma dos preços. Não explode em itens baratos como o MAPE. |
| Modelo final = menor WAPE médio nos cortes | Estabilidade pesa mais que vencer um único período. |

## Premissas e limitações

- Preços nominais em dólar; não corrigimos pela inflação.
- Média nacional (U.S. city average).
- O modelo usa só o histórico de preços. Não tem dados de clima, safra, câmbio, tarifas ou surtos de gripe aviária.
- Séries descontinuadas ou com mais de 25% de meses faltando ficam fora da modelagem, mas entram no dashboard histórico.

## Fora do escopo

- Previsão por região ou por loja.
- Atualização automática mensal da base.
- Modelos de séries temporais clássicos por item (ARIMA/Prophet). Ficou como possível extensão.

## Critérios de conclusão

- Pipeline executável de ponta a ponta com um comando por etapa.
- Três algoritmos comparados com os baselines, com métricas documentadas.
- Testes automatizados, incluindo o de vazamento de informação do futuro.
- Dashboard no Power BI com histórico, previsão e desempenho do modelo.
