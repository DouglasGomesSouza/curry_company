# Libraries
import plotly.express as px

# Bibliotecas
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config ( page_title= 'Visão Empresa', layout = 'wide') #  funcao para distribuir o grafico na pagina

#============================================
# Funções
#============================================
def country_maps ( df1 ):
	""" Esta função tem a responsabilidade de mostrar um mapa da localização central de cada cidade por tipo de tráfego.
		
		Input: DataFrame
		Output: None
	"""
	cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
	df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()
	
	m = folium.Map()
	
	for i, location_info in df_aux.iterrows():
		folium.Marker( [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']]).add_to( m )

	folium_static(m, width=1024, height= 600 )
	
	return None

def order_share_week ( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico do numero de entregas por entregador por semana
		
		Input: DataFrame
		Output: fig
	"""
	df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
	df_aux2 = df1.loc[:, ['Delivery_person_ID','week_of_year']].groupby('week_of_year').nunique().reset_index()
	df_aux = pd.merge( df_aux1, df_aux2, how = 'inner')
	df_aux['order_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
	fig = px.line( df_aux, x = 'week_of_year', y = 'order_delivery')

	return fig

def order_by_week( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico da quantidade de pedidos por semana
		
		Input: DataFrame
		Output: fig
	"""
	df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
	cols = ['ID', 'week_of_year']
	df1_aux = df1.loc[:, cols].groupby(['week_of_year']).count().reset_index()
	fig = px.line( df1_aux, x = 'week_of_year', y = 'ID')

	return fig

def traffic_order_city( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico da comparação do volume de pedidos por cidade e tipo de tráfego.
		
		Input: DataFrame
		Output: fig
	"""
	df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
	fig = px.scatter( df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')

	return fig

def traffic_order_share( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico da comparação da distribuição dos pedidos por tipo de tráfego.
		
		Input: DataFrame
		Output: fig
	"""
	df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
	df_aux['perc_ID'] = df_aux['ID'] / df_aux['ID'].sum()
	fig = px.pie( df_aux, values= 'perc_ID', names = 'Road_traffic_density')
	
	return fig

def order_metric ( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico da quantidade de pedidos por dia
		
		Input: DataFrame
		Output: fig
	"""
	cols = ['ID', 'Order_Date']
	df1_aux = df1.loc[:, cols].groupby(['Order_Date']).count().reset_index()
	fig = px.bar( df1_aux, x = 'Order_Date', y = 'ID')
	
	return fig

def clean_code( df1 ):
	""" Esta função tem a responsabilidade de limpar o dataframe
	
		Tipos de limpeza:
		- Remoção dos dados NaN
		- Mudança do tipo da coluna de dados
		- Remoção dos espaços das variaveis de texto
		- Formatação da coluna de datas
		- Limpeza da coluna de tempo ( remoção do texto da variavel numerica)
		
		Input: DataFrame
		Output: DataFrame
	"""
	#Limpando dados NaN e convertendo tipos

	linhas_vazias = (df1['Delivery_person_Age'] != 'NaN ')
	df1 = df1.loc[linhas_vazias, :].copy()
	df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

	df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

	df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

	linhas_vazias = (df1['multiple_deliveries'] != 'NaN ')
	df1 = df1.loc[linhas_vazias, :].copy()
	df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

	linhas_vazias = df1['Road_traffic_density'] != 'NaN '
	df1 = df1.loc[linhas_vazias,:].copy()

	linhas_vazias = df1['Festival'] != 'NaN '
	df1 = df1.loc[linhas_vazias, :].copy()

	linhas_vazias = df1['City'] != 'NaN '
	df1 = df1.loc[linhas_vazias, :].copy()

	# Removendo espaços de string

	df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
	df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
	df1.loc[:, 'Weatherconditions'] = df1.loc[:, 'Weatherconditions'].str.strip()
	df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
	df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
	df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
	df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
	df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

	# Limpando a coluna de time taken
	## .split() -> quebra a string em substrings; divide em outras string
	## .replace( oldvalue, newvalue, count) -> substitui a string por outra string
	## .apply() -> função que permite aplicar um comando linha a linha
	df1.loc[:, 'Time_taken(min)'] = df1.loc[:, 'Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1] )
	df1.loc[:, 'Time_taken(min)']  = df1.loc[:, 'Time_taken(min)'].astype(int)

	return df1

#============================================ Inicio da Estrutura logica do codigo ============================================

# Import dataset
df = pd.read_csv('datasets/train.csv')

# Limpando os dados
df1 = clean_code( df )

#============================================
# Barra lateral
#============================================

st.header('Marketplace - Visão Cliente')

#image_path = 'datasets/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=190 )

st.sidebar.markdown( '# Curry Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite')

date_slider = st.sidebar.slider( 'Até qual valor?', value= pd.datetime( 2022, 4, 13), min_value= pd.datetime( 2022, 2, 11), max_value= pd.datetime( 2022, 4, 6), format='DD-MM-YYYY' )

st.sidebar.markdown( """---""")

traffic_options = st.sidebar.multiselect( 'Quais as condições do trânsito', ['Low', 'Medium', 'High', 'Jam'], default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """---""")
st.sidebar.markdown( '### Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito

linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


#============================================
# Layout Streamlit
#============================================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
	with st.container():
		st.markdown( '# Orders by Day' )
		fig = order_metric( df1 )
		st.plotly_chart( fig, use_container_width=True )

	with st.container():
		col1, col2 = st.columns( 2 )
		
		with col1:
			st.markdown( '# Traffic Order Share' )
			fig = traffic_order_share( df1 )
			st.plotly_chart( fig, use_container_width=True )
			
		with col2:
			st.markdown( '# Traffic Order City' )
			fig = traffic_order_city( df1 )			
			st.plotly_chart( fig, use_container_width=True )
			
with tab2:
	with st.container():
		st.markdown( '# Orders by Week' )
		fig = order_by_week( df1 )
		st.plotly_chart( fig, use_container_width=True )
		
	with st.container():
		st.markdown( '# Orders Share by Week' )
		fig = order_share_week ( df1 )
		st.plotly_chart( fig, use_container_width=True )

with tab3:	
	st.markdown( '# Country Maps' )
	country_maps( df1 )