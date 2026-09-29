# Dashboard no Power BI

Projeto do Power BI no formato PBIP (pasta de arquivos em texto, que o git consegue versionar).
Já vem com as tabelas, os relacionamentos, as medidas e as 4 páginas montadas.

## Como abrir

1. Abra o arquivo **`DashboardPrecos.pbip`** no Power BI Desktop.
2. Se aparecer erro de arquivo não encontrado, ajuste a pasta dos dados:
   **Página Inicial > Transformar dados > Editar parâmetros > PastaDados** e coloque o caminho
   da pasta onde estão os 8 CSVs, **terminando com `\`**. Exemplo:
   `C:\Users\seu-usuario\Downloads\csvs-dashboard\`
3. Clique em **Atualizar**.

O caminho que vem configurado é o da pasta `data\processed\powerbi\` do repositório no computador do Breno.

## Páginas

| Página | O que mostra |
|---|---|
| Panorama | Quanto os preços subiram de 2015 a 2026, por categoria e por produto |
| Série temporal | Histórico do produto, sazonalidade por mês, produtos que mais oscilam, tendência x sazonalidade |
| Previsão | Preço atual, previsto para 3 meses à frente e faixa provável |
| Confiabilidade | Erro do modelo comparado com repetir o preço de hoje |

Filtros de **Categoria** e **Produto** no topo de cada página.

Para trocar de página, use o menu lateral. No modo de edição do Power BI Desktop é preciso segurar **Ctrl** ao clicar no botão; na leitura ou depois de publicado, basta clicar.

## Para conferir se carregou certo

- Panorama: 63 produtos acompanhados, alta mediana de 40,9%.
- Confiabilidade: erro do modelo 3,86%, erro repetindo o preço 4,38%.

## Salvar

Pode continuar salvando como `.pbip` (recomendado para o git) ou usar **Arquivo > Salvar como** e gerar
um `.pbix` para mandar por e-mail. Os arquivos em `.pbi/` (cache) não vão para o git.
