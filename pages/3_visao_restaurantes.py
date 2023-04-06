# Libraries
from haversine import haversine, Unit
import plotly.express as px
import plotly.graph_objects as go

# Bibliotecas
import folium
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config ( page_title= 'Visão Restaurantes', layout = 'wide') #  funcao para distribuir o grafico na pagina

#============================================
# Funções
#============================================
def avg_std_time_by_order( df1 ):
	""" Esta função tem a responsabilidade de mostrar um DataFrame do tempo médio e o desvio padrão de entrega por tipo depedido.
		
		Input: DataFrame
		Output: DataFrame auxiliar
	"""
	df_aux = df1.loc[:, ['Time_taken(min)', 'Type_of_order', 'City']].groupby(['City', 'Type_of_order']).agg( {'Time_taken(min)':['mean', 'std']}).round(3)
	df_aux.columns = ['avg_time', 'std_time']
	df_aux = df_aux.reset_index()

	return df_aux

def avg_std_time_by_city( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico do tempo médio e o desvio padrão de entrega por cidade.
		
		Input: DataFrame
		Output: fig
	"""
	df_aux = df1.loc[:, ['Time_taken(min)', 'City']].groupby('City').agg( {'Time_taken(min)': ['mean', 'std']}).round(3)
	df_aux.columns = ['avg_time', 'std_time']
	df_aux = df_aux.reset_index()

	fig = go.Figure()
	fig.add_trace ( go.Bar ( name= 'Control', x= df_aux['City'], y= df_aux['avg_time'], error_y= dict( type= 'data', array= df_aux['std_time'] ) ) )
	fig.update_layout( barmode='group')

	return fig

def avg_std_time_city_traffic( df1 ):
	""" Esta função tem a responsabilidade de mostrar um grafico do tempo médio e o desvio padrão de entrega por cidade por trafego.
		
		Input: DataFrame
		Output: fig
	"""
	df_aux = df1.loc[:, ['Time_taken(min)', 'Road_traffic_density', 'City']].groupby(['City', 'Road_traffic_density']).agg( {'Time_taken(min)': ['mean', 'std']}).round(3)
	df_aux.columns = ['avg_time', 'std_time']
	df_aux = df_aux.reset_index()

	fig = px.sunburst( df_aux, path= ['City', 'Road_traffic_density'], values= 'avg_time', color= 'std_time', color_continuous_scale= 'ylorrd', color_continuous_midpoint= np.average( df_aux['std_time']))

	return fig

def avg_std_time_festival( df1, festival, op ):
	'''
		Esta função calcula o tempo médio de entrega durantes os Festivais.
		Parametros:
			Input:
				- df: DataFrame com os dados necessarios para o calculo
				- op: tipo de operaçao que precisa ser calculado
					'avg_time': calculao tempo medio
					'std_time': calcula o desvio padrao
			Output:
				- df: DataFrame com 2 colunas e 2 linhas
	'''
	df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
				  .groupby('Festival')
				  .agg( {'Time_taken(min)' : ['mean', 'std']} ) )
	df_aux.columns = ['avg_time', 'std_time']
	df_aux = df_aux.reset_index()
	df_aux = df_aux.loc [df_aux['Festival'] == festival, op ].round(2)

	return df_aux

def distance( df1, fig ):
	""" Esta função tem a responsabilidade de mostrar um DataFrame ou um grafico da distancia media das entregas.
	
		Input: DataFrame
		Output: DataFrame ou fig
	"""
	if fig == False:
		cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
		df1['distance'] = df1.loc[:, cols].apply( lambda x: haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'],x['Delivery_location_longitude']) ), axis=1 ) 
		avg_distance = df1['distance'].mean().round(2)
		return avg_distance
	
	else:
		cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
		df1['distance'] = df1.loc[:, cols].apply( lambda x: haversine( (x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'],x['Delivery_location_longitude']) ), axis=1 )
		avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
		fig = go.Figure( data= [ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0] ) ] )

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

df1 = clean_code( df )

#============================================
# Barra lateral
#============================================

st.header('Marketplace - Visão Restaurantes')

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

start_weather, end_weather = st.sidebar.select_slider( 'Seleciona as condições climáticas', options=['Cloudy', 'Fog', 'Sandstorms', 'Stormy', 'Sunny', 'Windy' ],value=(['Cloudy', 'Sunny']))
st.sidebar.write('Você selecionou os climas entre', start_weather, 'and', end_weather)

st.sidebar.markdown( """---""")
st.sidebar.markdown( '### Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito

linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de clima
# linhas_selecionadas = ( df1['Weatherconditions'] > start_weather ) & ( df1['Weatherconditions'] < end_weather )
# df1 = df1.loc[linhas_selecionadas, :]

#============================================
# Layout Streamlit
#============================================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
	
	with st.container():
		
		st.title( 'Overal Metrics' )
		
		col1, col2, col3, col4, col5, col6 = st.columns ( 6 )
		
		with col1:
			entregadores_unicos = len ( df1.loc[:, 'Delivery_person_ID'].unique() )
			col1.metric( 'Entregadores únicos', entregadores_unicos )
			
		with col2:
			avg_distance = distance( df1, fig=False )
			col2.metric( 'Distancia média das entregas', avg_distance)
			
		with col3:
			df_aux = avg_std_time_festival( df1, festival = 'Yes', op= 'avg_time' )
			col3.metric( 'Tempo medio de entrega com Festival', df_aux)
			
		with col4:
			df_aux = avg_std_time_festival( df1, festival = 'Yes', op= 'std_time' )
			col4.metric( 'Desvio padrao de entrega com Festival', df_aux)
			
		with col5:
			df_aux = avg_std_time_festival( df1, festival = 'No', op= 'avg_time' )
			col5.metric( 'Tempo medio de entrega sem Festival', df_aux)
			
		with col6:
			df_aux = avg_std_time_festival( df1, festival = 'No', op= 'std_time' )
			col6.metric( 'Desvio padrao de entrega sem Festival', df_aux)
			
	with st.container():
		st.markdown( """---""" )
		st.title( 'Tempo medio e desvio padrao de entrega por cidade e trafego' )
		fig = avg_std_time_city_traffic( df1 )
		st.plotly_chart( fig, use_container_width=True  )
		
	with st.container():
		st.markdown( """---""" )
		st.title( 'Distribuiçao do tempo' )
		
		col1, col2 = st.columns( 2 )
		
		with col1:
			st.markdown( '##### Por cidade' )
			fig = avg_std_time_by_city( df1 )
			st.plotly_chart( fig, use_container_width=True)
			
		with col2:
			st.markdown( '##### Por tipo de pedido' )
			df_aux = avg_std_time_by_order( df1 )
			st.dataframe ( df_aux )
			
	with st.container():
		st.markdown( """---""" )
		st.title( 'Distribuição da distancia' )
		fig = distance( df1, fig=True )
		st.plotly_chart( fig )