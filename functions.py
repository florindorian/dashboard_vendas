import streamlit as st
import time
import pandas as pd


def formata_numero(valor, prefixo=''):
	for unidade in ['', 'mil']:
		if valor < 1000:
			return f'{prefixo} {valor:.2f} {unidade}'

		valor /= 1000
	return f'{prefixo} {valor:.2f} milhões'


@st.cache_data
def converte_csv(df: pd.DataFrame):
	return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
	sucesso = st.success('Arquivo baixado com sucesso!', icon="✅")  # -- Por padrão, essa mensagem não some sozinha
	time.sleep(5)
	sucesso.empty()  # -- Elimina a mensagem
