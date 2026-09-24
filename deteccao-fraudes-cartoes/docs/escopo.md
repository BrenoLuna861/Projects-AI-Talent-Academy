# Escopo do Projeto

**Autores:** Breno Luna e Paula Carlesso

## Tema
Machine Learning para **Detecção de Fraudes em Cartões**.

## Objetivo geral
Identificar transações com alta probabilidade de fraude na base relacional do
curso e apresentar os resultados em um dashboard que apoie a análise.

## Base de dados
As seis tabelas usadas nas aulas 2, 5, 6, 7, 8, 9 e 10: `transacoes`,
`cartoes`, `clientes`, `lojistas`, `categorias` e `contestacoes`.

A escolha é deliberada. Comparada às bases públicas de fraude:

| | Base do curso | Kaggle ULB | Sparkov |
|---|---|---|---|
| Campos de negócio (lojista, categoria, canal) | ✅ | ❌ (só `V1`–`V28` anonimizados) | ✅ |
| Já conhecida pelo grupo | ✅ | ❌ | ❌ |
| Rótulo disponível | ✅ via contestação | ✅ | ✅ |
| Dashboard com significado | ✅ | ❌ | ✅ |

Com o ULB não daria para fazer "fraude por categoria de lojista" — as colunas
não têm significado. Nossa base tem, e ainda vem com a EDA da Aula 08 e o
pipeline PySpark da Aula 10 já feitos.

## Definição do rótulo

`fraude = 1` quando a transação aparece em `contestacoes`.

**Isso é um proxy, e a limitação é parte do trabalho:**

- Nem toda contestação é fraude — pode ser erro de cobrança, cobrança duplicada ou arrependimento do titular.
- Nem toda fraude é contestada — valores baixos passam despercebidos, e é justamente aí que mora o teste de cartão.
- A contestação chega **depois** da transação, às vezes semanas depois. Em produção, o rótulo de hoje só existe daqui a um mês.

O modelo, portanto, aprende a prever *transação que será contestada*. É a melhor
aproximação disponível nesta base, e o relatório final precisa dizer isso com
todas as letras.

## Objetivos específicos
1. Pipeline de ETL reprodutível, com quarentena de dados (nada sumir sem rastro).
2. Features construídas apenas com informação anterior a cada transação.
3. Comparar ao menos três algoritmos com métricas próprias de base desbalanceada.
4. Escolher o ponto de corte por critério de negócio, não pelo 0,5 de fábrica.
5. Dashboard Power BI com indicadores de negócio e de desempenho do modelo.

## Decisões técnicas

**Split temporal, não aleatório.** Os últimos 25% do período viram teste. Fraude
evolui: o padrão de ataque de março não é o de janeiro. Split aleatório deixa o
modelo treinar com transações posteriores às do teste — resultado inflado que
não se repete em produção.

**Sem vazamento nas features.** Todo agregado histórico (média do cartão, taxa
de contestação do lojista) usa `expanding().shift(1)`. A taxa de contestação do
lojista é a mais perigosa: sem o `shift`, o rótulo da própria linha entra na
feature que tenta prevê-lo.

**Desbalanceamento via `class_weight`.** Mais simples que reamostrar e não
inventa dados. SMOTE fica como alternativa a testar.

**Acurácia não é métrica.** Com ~1% de fraude, prever "nunca é fraude" dá 99%
de acerto e zero utilidade. Usamos recall, precision, F1 e AUC-PR.

## Fora do escopo (versão 1)
- API de scoring em tempo real e integração com sistema transacional.
- Retreinamento automático.
- Explicabilidade individual (SHAP) — desejável numa v2.

## Critérios de conclusão
- [x] Pipeline executável de ponta a ponta
- [x] Três algoritmos comparados com métricas documentadas
- [x] Escolha de limiar por critério de negócio
- [ ] Execução sobre a base real (falta baixar os CSVs)
- [ ] Dashboard Power BI publicado
- [ ] Relatório final e apresentação
