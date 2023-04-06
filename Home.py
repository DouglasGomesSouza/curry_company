# criar pasta pages e colocar os arquivos da pagina dentro
# criar arquivo home
import streamlit as st
from PIL import Image

#st.set_page_config( page_title= 'Home' )
st.set_page_config ( page_title= 'Home', layout = 'wide') #  funcao para distribuir o grafico na pagina

#image_path = 'datasets/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=190 )

st.sidebar.markdown( '# Curry Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )



st.write( '# Curry Company Growth Dashboard' )

st.markdown(
	'''
	Growth Dashboard foi construido para acompanharas metricas de crescimento dos Entregadores e Restaurantes.
	### Como utilizar esse Growth Dashboard ?
	- Visao Empresa:
		- Visao Gerencial: Métricas gerais de comportamento.
		- Visao Tática: Indicadores semanais de crescimento.
		- Visao Geografica: Insights de geolocalizaçao.
	- Visao Entregador:
		- Acompanhamento dos indicadores semanais de crescimento.
	- Visao Restaurantes:
		- Indicadores semanais de crescimento dos restaurantes.
	### Ask for Help
	- Email douglas12gs@gmail.com
		''')