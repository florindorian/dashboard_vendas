import pandas as pd
import plotly.express as px
import requests


class Elements:
	def __init__(self):
		pass

	@staticmethod
	def dados(url, query_string):
		# -- Requisição HTTP para obter o Dataset
		response = requests.get(url, params=query_string)
		dados = pd.DataFrame.from_dict(response.json())
		dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')
		return dados

	@staticmethod
	def tab_vendedores(dados):
		return pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

	@staticmethod
	def tab_receita_categorias(dados):
		return dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

	@staticmethod
	def tab_receita_mensal(dados):
		receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
		receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
		receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()
		return receita_mensal

	@staticmethod
	def tab_receita_estados(dados: pd.DataFrame):
		receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
		receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(
			receita_estados, left_on='Local da compra', right_index=True
		).sort_values('Preço', ascending=False)
		return receita_estados

	@staticmethod
	def tab_vendas_estados(dados: pd.DataFrame):
		tab_vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count())
		tab_vendas_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(
			tab_vendas_estados,
			left_on='Local da compra',
			right_index=True
		).sort_values('Preço', ascending=False)
		return tab_vendas_estados

	@staticmethod
	def tab_vendas_mensal(dados: pd.DataFrame):
		tab_vendas_mensal = pd.DataFrame(
			dados.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].count()).reset_index()
		tab_vendas_mensal['Ano'] = tab_vendas_mensal['Data da Compra'].dt.year
		tab_vendas_mensal['Mes'] = tab_vendas_mensal['Data da Compra'].dt.month_name()
		return tab_vendas_mensal

	@staticmethod
	def tab_vendas_categorias(dados: pd.DataFrame):
		tab_vendas_categorias = pd.DataFrame(
			dados.groupby('Categoria do Produto')[['Preço']].count().sort_values(by='Preço', ascending=False)
		)
		return tab_vendas_categorias

	@staticmethod
	def fig_mapa_receita(receita_estados: pd.DataFrame):
		fig_mapa_receita = px.scatter_geo(
			receita_estados,
			lat='lat',
			lon='lon',
			scope='south america',
			size='Preço',
			template='seaborn',
			hover_name='Local da compra',
			hover_data={'lat': False, 'lon': False},
			title='Receita por estado'
		)
		return fig_mapa_receita

	@staticmethod
	def fig_receita_mensal(receita_mensal: pd.DataFrame):
		fig_receita_mensal = px.line(
			receita_mensal,
			x='Mes',
			y='Preço',
			markers=True,
			range_y=(0, receita_mensal.max()),
			color='Ano',
			line_dash='Ano',
			title='Receita mensal'
		)
		fig_receita_mensal.update_layout(yaxis_title='Receita')  # -- para alterar o nome do eixo y
		return fig_receita_mensal

	@staticmethod
	def fig_receita_estados(tab_receita_estados):
		fig_receita_estados = px.bar(
			tab_receita_estados.head(),
			x='Local da compra',
			y='Preço',
			text_auto=True,  # -- Coloca o valor da receita em cima de cada uma das colunas automaticamente
			title='Top estados (receita)'
		)
		fig_receita_estados.update_layout(yaxis_title='Receita')  # -- para alterar o nome do eixo y
		return fig_receita_estados

	@staticmethod
	def fig_receita_categorias(receita_categorias):
		fig_receita_categorias = px.bar(
			receita_categorias,
			text_auto=True,
			title='Receita por categoria'
		)
		fig_receita_categorias.update_layout(yaxis_title='Receita')  # -- para alterar o nome do eixo y
		return fig_receita_categorias

	@staticmethod
	def fig_mapa_vendas(tab_vendas_estados):
		fig_mapa_vendas = px.scatter_geo(
			tab_vendas_estados,
			lat='lat',
			lon='lon',
			scope='south america',
			# fitbounds='locations',
			template='seaborn',
			size='Preço',
			hover_name='Local da compra',
			hover_data={'lat': False, 'lon': False},
			title='Vendas por estado'
		)
		return fig_mapa_vendas

	@staticmethod
	def fig_vendas_mensal(tab_vendas_mensal):
		fig_vendas_mensal = px.line(
			tab_vendas_mensal,
			x='Mes',
			y='Preço',
			markers=True,
			range_y=(0, tab_vendas_mensal.max()),
			color='Ano',
			line_dash='Ano',
			title='Quantidade de vendas mensal'
		)
		fig_vendas_mensal.update_layout(yaxis_title='Quantidade de vendas')
		return fig_vendas_mensal

	@staticmethod
	def fig_vendas_estados(tab_vendas_estados):
		fig_vendas_estados = px.bar(
			tab_vendas_estados.head(),
			x='Local da compra',
			y='Preço',
			text_auto=True,
			title='Top 5 estados'
		)
		fig_vendas_estados.update_layout(yaxis_title='Quantidade de vendas')
		return fig_vendas_estados

	@staticmethod
	def fig_vendas_categorias(tab_vendas_categorias):
		fig_vendas_categorias = px.bar(
			tab_vendas_categorias,
			text_auto=True,
			title='Vendas por categoria'
		)
		fig_vendas_categorias.update_layout(showlegend=False, yaxis_title='Quantidade de vendas')
		return fig_vendas_categorias
