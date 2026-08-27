# Projects — AI Talent Academy

Repositório com as atividades práticas desenvolvidas ao longo do **AI Talent Academy**.

Cada aula vive na sua própria pasta, com o notebook executado (saídas preservadas) e um
README explicando o que foi feito, as decisões técnicas e os resultados.

**Autor:** Breno Luna — [@BrenoLuna861](https://github.com/BrenoLuna861)

---

## Atividades

| # | Atividade | Tema | Autoria | Notebook |
|---|---|---|---|---|
| 04 | Prática 02 — Semana 2 | Classificação de reclamações com LLM via API | Grupo 01 | [Abrir](./aula-04-pratica-02/) |

> As próximas aulas serão adicionadas seguindo o mesmo padrão.

**Grupo 01:** Breno Luna · Ricardo Lima · Paula Carlesso

---

## Como está organizado

```
Projects-AI-Talent-Academy/
├── README.md                    ← você está aqui
└── aula-04-pratica-02/
    ├── README.md                ← detalhes desta atividade
    └── Aula_04_Pratica_02_Semana_2.ipynb
```

A convenção de pastas é `aula-NN-nome-curto/`. Assim as atividades ficam em ordem e a
raiz não vira um monte de arquivo solto.

## Como executar os notebooks

Todos foram feitos para o **Google Colab**. Cada notebook tem um botão *Open in Colab*
no topo — é o caminho mais rápido, não precisa instalar nada.

Os notebooks que chamam APIs externas leem as credenciais dos **Secrets do Colab**
(ícone 🔑 na barra lateral), nunca do código. O README de cada atividade diz qual nome
de secret é esperado.

```python
from google.colab import userdata
api_key = userdata.get('NOME_DO_SECRET')
```

Nenhuma chave de API está versionada neste repositório.

## Tecnologias

`Python` · `Google Colab` · `pandas` · `tiktoken` · `datasets` ·
`OpenAI SDK` · `NVIDIA NIM API`

---

## Sobre o curso

O AI Talent Academy trabalha o uso prático de modelos de linguagem: tokenização,
engenharia de prompt, chamadas de API, avaliação de resultados e as decisões de
engenharia por trás de cada uma — quando usar reasoning, qual temperatura, como medir
acurácia de forma honesta.

O foco das atividades não é treinar modelos, e sim usar bem os que já existem.
