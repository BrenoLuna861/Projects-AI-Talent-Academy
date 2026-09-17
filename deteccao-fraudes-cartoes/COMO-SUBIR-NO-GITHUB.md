# Como enviar esta estrutura para o repositório do GitHub

A pasta foi criada em:
`C:\Users\edmil\Documents\Projects-AI-Talent-Academy\deteccao-fraudes-cartoes`

O repositório remoto é `https://github.com/BrenoLuna861/Projects-AI-Talent-Academy`.

## Opção A — ainda não tem o repositório clonado no PC (caso atual)

Abra o **Git Bash** ou o **PowerShell** na pasta `Projects-AI-Talent-Academy`:

```bash
cd "C:/Users/edmil/Documents/Projects-AI-Talent-Academy"

git init
git remote add origin https://github.com/BrenoLuna861/Projects-AI-Talent-Academy.git
git fetch origin
git checkout main            # traz README.md e aula-04-pratica-02 sem apagar a pasta nova

git add deteccao-fraudes-cartoes
git commit -m "Add estrutura do projeto de deteccao de fraudes em cartoes"
git push origin main
```

> `git checkout main` funciona porque os arquivos novos estão em uma pasta que
> não existe no repositório remoto — não há conflito.

## Opção B — já tem o repositório clonado em outro lugar

Copie a pasta `deteccao-fraudes-cartoes` para dentro do clone e rode:

```bash
git add deteccao-fraudes-cartoes
git commit -m "Add estrutura do projeto de deteccao de fraudes em cartoes"
git push origin main
```

## Depois do primeiro push

1. Crie o ambiente virtual e instale as dependências:
   ```bash
   cd deteccao-fraudes-cartoes
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Preencha `docs/plano-de-atividades.md` com responsáveis e prazos.
3. Coloque a base escolhida em `data/raw/` e preencha `data/README.md` e `docs/dicionario-de-dados.md`.

## Dica de organização do grupo
Trabalhem em branches por etapa (`etl`, `modelagem`, `dashboard`) e abram Pull
Request para `main`. Isso evita sobrescrever o trabalho de outro integrante —
especialmente com notebooks, que geram conflitos difíceis de resolver.
