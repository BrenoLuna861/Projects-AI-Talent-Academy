# Escopo do Projeto

## Tema
Machine Learning para **Detecção de Fraudes em Cartões**.

## Objetivo geral
Construir um modelo capaz de identificar transações com alta probabilidade de
fraude e disponibilizar os resultados em um dashboard que apoie a análise e a
tomada de decisão.

## Objetivos específicos
1. Selecionar e documentar a base de dados de transações.
2. Realizar a análise exploratória (EDA) entendendo volume, valores, distribuição temporal e o grau de desbalanceamento entre classes.
3. Construir um pipeline de ETL em Python que entregue dados tratados e reprodutíveis.
4. Treinar e comparar modelos de classificação, priorizando a captura de fraudes (recall) sem inviabilizar a operação por falsos positivos.
5. Publicar os resultados em um dashboard Power BI com indicadores de negócio e de desempenho do modelo.

## Perguntas que o projeto responde
- Qual o volume e o valor financeiro das transações suspeitas no período?
- Em quais faixas de valor, horários e perfis a fraude se concentra?
- Quão confiável é o modelo — quantas fraudes ele captura e quantos alertas falsos gera?
- Como a taxa de fraude evolui ao longo do tempo?

## Premissas
- Base de dados pública, anonimizada, de transações de cartão de crédito.
- Classes fortemente desbalanceadas (fraude costuma ficar abaixo de 1%), o que torna acurácia uma métrica inadequada.
- O custo de deixar passar uma fraude é maior que o de revisar um alerta falso — o limiar de decisão será ajustado com isso em mente.

## Fora do escopo (versão 1)
- API de scoring em tempo real e integração com sistemas transacionais.
- Retreinamento automático em produção.
- Dados pessoais identificáveis.

## Critérios de conclusão
- Pipeline de ETL executável de ponta a ponta.
- Pelo menos três algoritmos comparados com métricas documentadas.
- Dashboard Power BI publicado com os indicadores definidos.
- Repositório organizado, documentado e com o histórico de acompanhamentos.
