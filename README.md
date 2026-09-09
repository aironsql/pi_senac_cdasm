# Projeto Integrador – Análise de Absenteísmo no Trabalho

## Observação

Como foi pedido nas observações da primeira entrega, utilizamos a biblioteca Streamlit, e mudamos de um arquivo .ipynb para um arquivo .py que abrirá um logalhost com o Dashboard
Vamos manter o arquivo .ipynb anterior e adicionaremos o novo arquivo .py, além, dessas alterações no Readme e um arquivo .txt com as especificações das versões das bibliotecas usadas, tivemos auxílio do copilot cli, que nos orientou a como criar o localhost com o streamlit, além de correções ortográficas nesse atual arquivo, o desenvolvimento e a produção do readme foram feitos em conjunto em reuniões que marcamos, uma vez que já somos o mesmo grupo de projetos integradores anteriores.

Utilizamos os livros de ciência de dados e banco de dados para tomada de decisão, ambos da SENAC e disponibiliza gratuitamente para os alunos, além do livros Streamlit Essentials From basics to advanced data app development e Storytelling Com Dados - Vamos Praticar, ambos sendo recomendações do Gemini e encontrado gratuitamente, mas não tão honestamente, no annas-archive.

## Objetivo

Este projeto tem como objetivo realizar uma análise exploratória de dados sobre absenteísmo corporativo utilizando Python, Pandas e Matplotlib.

A análise busca identificar fatores que possam influenciar as ausências dos colaboradores no ambiente de trabalho e como essas informações podem auxiliar na tomada de decisão organizacional.

---

## Dataset Utilizado

Fonte dos dados:
- Absenteeism at Work
- UCI Machine Learning Repository

Link:
https://archive.ics.uci.edu/dataset/445/absenteeism+at+work

---

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Streamlit
- Plotly

---

## Etapas Desenvolvidas

- Importação e tratamento dos dados
- Tradução e padronização das colunas
- Análise exploratória dos dados
- Criação de visualizações gráficas
- Interpretação dos resultados

---

## Visualizações Criadas

1. Frequência dos motivos de ausência
2. Distribuição de idade dos colaboradores
3. Distância casa-trabalho x horas de ausência
4. Consumo de álcool x absenteísmo
5. IMC x horas de ausência

---

## Objetivo da Análise

Identificar padrões relacionados ao absenteísmo corporativo e gerar insights que possam auxiliar estratégias de gestão de pessoas, saúde ocupacional e produtividade.

## Dashboard interativo

O projeto também disponibiliza um painel interativo em Streamlit. A aplicação organiza
os dados em uma camada analítica filtrável e apresenta indicadores-chave, distribuição
dos motivos de ausência, perfil dos colaboradores e relações entre distância, hábitos,
IMC e horas de absenteísmo.

### Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O painel foi estruturado como uma interface de apoio à decisão: os filtros funcionam
como recortes analíticos, os cartões exibem os indicadores-chave de desempenho (KPIs)
e as abas detalham as evidências que sustentam a interpretação dos resultados.

---

## Autores

Projeto desenvolvido por Airon Leonardo do Monte Rufino, João Pedro Lopes dos Santos, Stella de Lima Bezerra e Stuart Santos Idalgo, para o Projeto Integrador do curso de Banco de Dados.
