# Acompanhamento 03 - 24/09/2026

**Integrantes:** Breno Luna e Paula Carlesso

## O que o grupo concluiu desde o último acompanhamento?

Trocamos o tema. Na revisão do projeto de detecção de fraude, o professor comentou que as
bases de fraude disponíveis são muito manjadas e indicou como exemplo a base de preços
médios do BLS publicada no Kaggle. Adotamos essa base e o projeto passou a ser
**previsão de preços de alimentos e energia nos EUA, 3 meses à frente**.

Aproveitamos a estrutura que já existia (ETL em módulos, notebooks por etapa, exportação
para o Power BI, testes) e reescrevemos o conteúdo para o novo problema. Com isso, o
pipeline já está completo e rodando com os dados reais.

## Principais entregas/evidências

| Entrega | Onde |
|---|---|
| Novo escopo, com o histórico da troca | `docs/escopo.md` |
| EDA completa: buracos, categorias erradas, sazonalidade, volatilidade | `notebooks/01_analise_exploratoria.ipynb` |
| ETL com correção de categorias e grade mensal | `src/etl/` |
| 12 features sem vazamento de futuro (com teste) | `src/features/build_features.py`, `tests/` |
| 3 algoritmos + 2 baselines, backtest com 4 cortes | `src/models/`, notebooks 03 e 04 |
| Tabelas e medidas DAX para o dashboard | `data/processed/powerbi/`, `powerbi/` |

## Resultados até aqui

- O modelo final (gradient boosting) tem WAPE médio de 3,86% contra 4,08% de repetir o
  preço atual. Ganha em 3 dos 4 cortes; empata no de dez/2022 (ano da desinflação).
- O ganho está em frutas, ovos e carne bovina. Em aves, padaria, laticínios e bebidas o
  ingênuo é igual ou melhor.
- Achados da base: out/2025 quase sem dados (shutdown do governo americano), café e
  batata chips com categoria errada no dataset, 14 séries descontinuadas.

## Dificuldades encontradas

- A troca de tema no meio do prazo. Minimizada porque a estrutura do repositório foi reaproveitada.
- Base pequena (60 séries utilizáveis x no máximo 139 meses). Resolvido com um modelo
  global que prevê variação percentual em vez de um modelo por item.
- Primeira versão da faixa de previsão era igual para todas as categorias e ficava
  estreita demais para energia e ovos. Passou a ser calculada por categoria.

## Próximas etapas

| Etapa | Responsável | Prazo |
|---|---|---|
| Montar o dashboard (4 páginas) | Paula | |
| Revisar textos dos notebooks e README | Paula | |
| Testar preços corrigidos pela inflação (extra) | Breno | |
| Slides e ensaio da apresentação | Breno e Paula | |
