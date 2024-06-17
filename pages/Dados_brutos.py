import streamlit as st
import requests
import pandas as pd
import functions

# -- Função para manter o arquivo gerado armazenado em cache
# -- Caso o DataFrame não tenha sido filtrado, a base de dados já será mantida

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
	colunas = st.multiselect(
		label='Selecione as colunas',
		options=list(dados.columns),
		default=list(dados.columns)
	)

st.sidebar.title('Filtros')
# -- Categórica
with st.sidebar.expander('Nome do produto'):
	produtos = st.multiselect(
		label='Selecione os produtos',
		options=dados['Produto'].unique(),
		default=dados['Produto'].unique()
	)

# -- Categórica
with st.sidebar.expander('Categoria'):
	categoria = st.multiselect(
		label='Seleciona as categorias',
		options=dados['Categoria do Produto'].unique(),
		default=dados['Categoria do Produto'].unique()
	)

# -- Numérica
with st.sidebar.expander(label='Preço do produto'):
	preco = st.slider(label='Selecione o preço', min_value=0, max_value=5000, value=(0,5000))
	# value=(0,5000) permitirá selecionar mais de um valor

# -- Numérica
with st.sidebar.expander(label='Frete'):
	vmin = dados['Frete'].min()
	vmax = dados['Frete'].max()
	frete = st.slider(label='Selecione o frete', min_value=vmin, max_value=vmax, value=(vmin, vmax))

# -- Data
with st.sidebar.expander(label='Data da compra'):
	data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

# -- Categórica
with st.sidebar.expander(label='Vendedor'):
	vendedor = st.multiselect(
		'Selecione os vendedores',
		options=dados['Vendedor'].unique(),
		default=dados['Vendedor'].unique()
	)

# -- Categórica
with st.sidebar.expander(label='Local da compra'):
	local_compra = st.multiselect(
		label='Selecione o local da compra',
		options=dados['Local da compra'].unique(),
		default=dados['Local da compra'].unique()
	)

# -- Numérica
with st.sidebar.expander(label='Avaliação da compra'):
	vmin = dados['Avaliação da compra'].min()
	vmax = dados['Avaliação da compra'].max()
	avaliacao_compra = st.slider(
		label='Selecione a avaliação da compra',
		min_value=vmin,
		max_value=vmax,
		value=(vmin, vmax)
	)

# -- Categórica
with st.sidebar.expander(label='Tipo de pagamento'):
	tipo_pagamento = st.multiselect(
		label='Selecione o tipo de pagamento',
		options=dados['Tipo de pagamento'].unique(),
		default=dados['Tipo de pagamento'].unique()
	)

# -- Numérica
with st.sidebar.expander(label='Quantidade de parcelas'):
	vmin = dados['Quantidade de parcelas'].min()
	vmax = dados['Quantidade de parcelas'].max()
	quantidade_parcelas = st.slider(
		label='Selecione a quantidade de parcelas',
		min_value=vmin,
		max_value=vmax,
		value=(vmin, vmax)
	)

query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local_compra and \
@avaliacao_compra[0] <= `Avaliação da compra` <= @avaliacao_compra[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@quantidade_parcelas[0] <= `Quantidade de parcelas` <= @quantidade_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para um arquivo')
coluna1, coluna2 = st.columns(2)

with coluna1:
	nome_arquivo = st.text_input(' ', label_visibility='collapsed', value='dados')
	nome_arquivo += '.csv'

with coluna2:
	st.download_button(
		label='Fazer o download da tabela em csv',
		data=functions.converte_csv(dados_filtrados),
		file_name=nome_arquivo,
		mime='text/csv',  # -- tipo do arquivo
		on_click=functions.mensagem_sucesso()
	)
