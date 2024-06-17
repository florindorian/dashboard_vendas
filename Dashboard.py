import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -- Biblioteca de funções auxiliares
import functions
from Elements import Elements

# -- Configurações da página inicial do Dashboard
st.set_page_config(layout='wide')
st.title('DASHBOARD DE VENDAS :shopping_trolley:')


# -- Opções de Filtragem
st.sidebar.title('Filtros')
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sul']
regiao = st.sidebar.selectbox('Região', regioes)
todos_anos = st.sidebar.checkbox('Dados de todo o período', value=True)  # -- value: valor habilitado por padrão

# -- Habilitando controles condicionalmente:
if regiao == 'Brasil':
	regiao = ''

if todos_anos:  # -- se essa checkbox estiver marcada
	ano = ''
else:
	ano = st.sidebar.slider(label='Ano', min_value=2020, max_value=2023)

# -- Requisição HTTP para obter o Dataset
url = 'https://labdados.com/produtos'
query_string = {'regiao': regiao.lower(), 'ano': ano}
dados = Elements.dados(url, query_string)

filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:  # Se esse filtro estiver marcado com alguma opção no select
	dados = dados[dados['Vendedor'].isin(filtro_vendedores)]


# -- Tabelas de Receitas
tab_receita_mensal = Elements.tab_receita_mensal(dados)
tab_receita_estados = Elements.tab_receita_estados(dados)
tab_receita_categorias = Elements.tab_receita_categorias(dados)
# -- Tabela de Vendas
tab_vendas_estados = Elements.tab_vendas_estados(dados)
tab_vendas_mensal = Elements.tab_vendas_mensal(dados)
tab_vendas_categorias = Elements.tab_vendas_categorias(dados)
# -- Tabelas vendedores
tab_vendedores = Elements.tab_vendedores(dados)


# -- Gráficos de Mapa
fig_mapa_receita = Elements.fig_mapa_receita(tab_receita_estados)
fig_mapa_vendas = Elements.fig_mapa_vendas(tab_vendas_estados)
# -- Gráficos de Linha
fig_receita_mensal = Elements.fig_receita_mensal(tab_receita_mensal)
fig_vendas_mensal = Elements.fig_vendas_mensal(tab_vendas_mensal)
# -- Gráficos de Barra
fig_receita_estados = Elements.fig_receita_estados(tab_receita_estados)
fig_receita_categorias = Elements.fig_receita_categorias(tab_receita_categorias)
fig_vendas_estados = Elements.fig_vendas_estados(tab_vendas_estados)
fig_vendas_categorias = Elements.fig_vendas_categorias(tab_vendas_categorias)


# -- Visualização no Streamlit
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de Vendas', 'Vendedores'])

with aba1:
	coluna1, coluna2 = st.columns(2)
	with coluna1:
		st.metric('Receita', functions.formata_numero(dados['Preço'].sum(), 'R$'))
		# -- use_container_width: serve para evitar a sobreposição de gráficos
		st.plotly_chart(fig_mapa_receita, use_container_width=True)
		st.plotly_chart(fig_receita_estados, use_container_width=True)

	with coluna2:
		st.metric('Quantidade de Vendas', functions.formata_numero(dados.shape[0]))
		# -- use_container_width: serve para evitar a sobreposição de gráficos
		st.plotly_chart(fig_receita_mensal, use_container_width=True)
		st.plotly_chart(fig_receita_categorias, use_container_width=True)

	# st.dataframe(dados)

with aba2:
	with aba2:
		coluna1, coluna2 = st.columns(2)
		with coluna1:
			st.metric('Receita', functions.formata_numero(dados['Preço'].sum(), 'R$'))
			st.plotly_chart(fig_mapa_vendas, use_container_width=True)
			st.plotly_chart(fig_vendas_estados, use_container_width=True)

		with coluna2:
			st.metric('Quantidade de vendas', functions.formata_numero(dados.shape[0]))
			st.plotly_chart(fig_vendas_mensal, use_container_width=True)
			st.plotly_chart(fig_vendas_categorias, use_container_width=True)

with aba3:
	# Criando um input:
	qtd_vendedores = st.number_input('Quantidade de Vendedores', 2, 10, 5)
	#   depois do nome, vem: qtd mínima; qtd máxima; valor inicial

	coluna1, coluna2 = st.columns(2)
	with coluna1:
		st.metric('Receita', functions.formata_numero(dados['Preço'].sum(), 'R$'))

		fig_receita_vendedores = px.bar(
			tab_vendedores['sum'].sort_values(ascending=False).head(qtd_vendedores),
			x='sum',
			y=tab_vendedores['sum'].sort_values(ascending=False).head(qtd_vendedores).index,
			text_auto=True,  # para colocar os valores das receitas em cada barra
			title=f'Top {qtd_vendedores} vendedores (receita)'
		)
		st.plotly_chart(fig_receita_vendedores)

	with coluna2:
		st.metric('Quantidade de Vendas', functions.formata_numero(dados.shape[0]))

		fig_vendas_vendedores = px.bar(
			tab_vendedores['count'].sort_values(ascending=False).head(qtd_vendedores),
			x='count',
			y=tab_vendedores['count'].sort_values(ascending=False).head(qtd_vendedores).index,
			text_auto=True,  # para colocar os valores das receitas em cada barra
			title=f'Top {qtd_vendedores} vendedores (quantidade de vendas)'
		)
		st.plotly_chart(fig_vendas_vendedores)
