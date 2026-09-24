# Acompanhamento 02 — 20/09/2026

**Integrantes:** Breno Luna e Paula Carlesso

## O que o grupo concluiu desde o último acompanhamento?

Definimos a base de dados e implementamos o projeto de Machine Learning
completo: pipeline de ETL, engenharia de atributos, treino comparativo de três
algoritmos e avaliação com escolha de ponto de corte.

A base escolhida foi a **própria base relacional do curso** (as seis tabelas das
aulas 2, 5, 6, 7, 8, 9 e 10), em vez de uma base pública do Kaggle. O motivo: as
bases anonimizadas mais citadas têm colunas sem significado (`V1`–`V28`), o que
inviabilizaria o dashboard por categoria de lojista, canal e faixa de valor —
justamente o que prometemos no escopo. O rótulo vem da tabela `contestacoes`.

## Principais entregas/evidências

| Entrega | Onde |
|---|---|
| Definição da base e do rótulo, com limitações documentadas | `docs/escopo.md`, `docs/dicionario-de-dados.md` |
| ETL com quarentena de dados (nada descartado sem rastro) | `src/etl/transform.py` |
| Unificação das seis tabelas e criação do rótulo | `src/etl/build_dataset.py` |
| 15 features construídas só com informação anterior a cada transação | `src/features/build_features.py` |
| Treino com split temporal e três algoritmos | `src/models/train_model.py` |
| Métricas de base desbalanceada e escolha de limiar por recall mínimo | `src/models/evaluate.py` |
| Exportação para o Power BI | `src/models/predict_model.py` |
| Medidas DAX do dashboard | `powerbi/dax/medidas.dax` |
| 9 testes automatizados, todos passando | `tests/` |
| Gerador de base sintética para rodar sem o Drive | `tools/gerar_dados_exemplo.py` |

O pipeline foi validado de ponta a ponta com base sintética de mesmo schema —
20 mil transações, 1,66% de fraude. Os números dessa execução não valem como
resultado; servem para provar que o código roda.

## Decisões técnicas que valem registrar

- **Split temporal, não aleatório.** Fraude evolui; treinar com o futuro infla as métricas.
- **Nenhuma feature olha adiante.** Agregados usam `expanding().shift(1)` — sobretudo a taxa de contestação do lojista, onde a ausência do shift levaria o rótulo para dentro da feature.
- **Limiar escolhido por critério de negócio.** No corte padrão de 0,5, dois dos três modelos não acusavam nenhuma fraude. O `escolher_limiar()` exige recall mínimo de 70% e maximiza a precisão dentro disso.
- **Acurácia descartada como métrica.** Com ~1% de fraude, ela premia o modelo que nunca acusa nada.

## Próximas etapas

| Etapa | Responsável |
|---|---|
| Rodar o pipeline sobre a base real do curso | Breno |
| EDA sobre os dados reais | Paula |
| Construção do dashboard no Power BI | Paula |
| Relatório final e apresentação | Ambos |
