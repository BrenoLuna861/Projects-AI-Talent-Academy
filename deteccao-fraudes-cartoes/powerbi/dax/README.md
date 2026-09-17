# Scripts DAX

| Arquivo | Como usar |
|---|---|
| `dCalendario.dax` | Power BI Desktop → **Modelagem → Nova tabela** → colar o script inteiro. Depois marcar como tabela de datas. |
| `medidas.dax` | Criar uma tabela vazia `_Medidas` (Inserir dados → tabela em branco) e colar cada medida com **Nova medida**. |

## Organização sugerida das medidas

- **Volume** — `Total Transacoes`, `Valor Total`
- **Fraude** — `Transacoes Suspeitas`, `Taxa de Fraude %`, `Valor em Risco`, tickets médios
- **Matriz de confusão** — VP, FP, FN, VN
- **Desempenho** — `Recall`, `Precision`, `F1 Score`, `Fraudes Nao Detectadas (Valor)`

Agrupe em pastas de exibição com esses nomes para o painel de campos não virar uma lista solta.

## Ao editar

Toda medida alterada no Power BI deve ser copiada de volta para o `.dax`
correspondente. O `.pbix` é binário — o Git não mostra o que mudou dentro dele,
então esses arquivos de texto são o histórico real das medidas.
