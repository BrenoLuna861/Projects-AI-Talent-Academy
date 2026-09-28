# Acompanhamento 04 - 27/09/2026

**Integrantes:** Breno Luna e Paula Carlesso

## O que o grupo concluiu desde o último acompanhamento?

Incluímos a análise de série temporal que faltava: até aqui o preço era tratado só como
problema de regressão com features do passado. Agora cada item também é analisado e
modelado como série (valor passado -> valor futuro), e testamos qual granularidade de
dado prevê melhor.

## Principais entregas/evidências

| Entrega | Onde |
|---|---|
| Decomposição STL, força de tendência e sazonalidade por item | `notebooks/05_series_temporais_e_granularidade.ipynb` |
| Testes de estacionariedade (ADF) e ACF/PACF | notebook 05 |
| SARIMA e Holt-Winters por item, com o mesmo protocolo de teste do ML | `src/models/series_temporais.py` |
| Modelo combinado (gradient boosting + SARIMA), agora o modelo final | `src/models/evaluate.py`, `predict_model.py` |
| Experimento de granularidade: mensal x trimestral x anual; item x agregado | notebook 05 |
| Força da tendência/sazonalidade exportada para o dashboard | `data/processed/powerbi/dim_item.csv` |

## Resultados

- SARIMA e Holt-Winters sozinhos ficam no nível do ingênuo (4,13% e 4,26% de WAPE, contra 4,10% do ingênuo).
- A média entre gradient boosting e SARIMA é o melhor modelo: 3,80%, ganhando do ingênuo nos 4 cortes.
- Dados mensais preveem o trimestre seguinte melhor que dados trimestrais (2,6% x 3,3%). Mantivemos a granularidade mensal.

- Na auditoria encontramos um vazamento pequeno: previsões feitas a partir de um mês interpolado (out/2025) usavam, sem querer, o preço de nov/2025. Essas linhas saíram do treino e do teste e há um teste automatizado para isso. As métricas mudaram na segunda casa decimal.

## Dificuldades encontradas

- SARIMA por item é lento se reestimado a cada mês. Resolvido estimando os parâmetros uma vez por corte e só atualizando o filtro com os novos meses.

## Próximas etapas

| Etapa | Responsável | Prazo |
|---|---|---|
| Dashboard, incluindo a página de série temporal | Paula | |
| Slides e ensaio | Breno e Paula | |
