# Libraries
import plotly.express as px

# Bibliotecas
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config ( page_title= 'Visão Entregadores', layout = 'wide') #  funcao para distribuir o grafico na pagina

#============================================
# Funções
#============================================
def top_delivers( df1, top_asc ):
	df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
				.groupby(['City', 'Delivery_person_ID'])
				.mean().round(2).sort_values(['Time_taken(min)'], ascending = top_asc).reset_index() )
	df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
	df_aux02 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
	df_aux03 = df2.loc[df2['City'] == 'Urban', :].head(10)
	df3 = pd.concat( [df_aux01, df_aux02, df_aux03] )

	return df3

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

st.header('Marketplace - Visão Entregadores')

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
		col1, col2, col3, col4 = st.columns ( 4, gap= 'large' )
		with col1:
			# A maior idade dos entregadores
			maior_idade =  df1.loc[:, 'Delivery_person_Age'].max()
			col1.metric( 'Maior idade', maior_idade)
			
		with col2:
			# A menor idade dos entregadores
			menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
			col2.metric( 'Menor idade', menor_idade)
			
		with col3:
			# A melhor condição de veiculos
			melhor_cond = df1.loc[:, 'Vehicle_condition'].max()
			col3.metric( 'Melhor condição de veículo', melhor_cond)
			
		with col4:
			# A pior condição de veiculos
			pior_cond = df1.loc[:, 'Vehicle_condition'].min()
			col4.metric( 'Pior condição de veículo', pior_cond)
			
	with st.container():
		st.markdown( """---""")
		st.title( 'Avaliações' )
		
		col1, col2 = st.columns( 2 )
		
		with col1:
			st.markdown('##### Avaliação media por entregador')
			df_avg_rating_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby(['Delivery_person_ID']).mean().round(2).reset_index()
			st.dataframe( df_avg_rating_per_deliver )
			
		with col2:
			st.markdown('##### Avaliação media por transito')
			df_avg_std_by_traffic = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby(['Road_traffic_density']).agg(['mean', 'std']).round(3)
			df_avg_std_by_traffic.columns = ['delivery_mean', 'delivery_std']
			df_avg_std_by_traffic = df_avg_std_by_traffic.reset_index()
			st.dataframe( df_avg_std_by_traffic )

			st.markdown('##### Avaliação media por clima')
			df_avg_std_weather = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby(['Weatherconditions']).agg(['mean', 'std']).round(3)
			df_avg_std_weather.columns = ['delivery_mean', 'delivery_std']
			df_avg_std_weather = df_avg_std_weather.reset_index()
			st.dataframe( df_avg_std_weather )
			
	with st.container():
		st.markdown( """---""")
		st.title( 'Velocidade de entrega' )
		
		col1, col2 = st.columns( 2 )
		
		with col1:
			st.markdown('##### Top entregadores mais rápidos')
			df3 = top_delivers( df1, top_asc=True )
			st.dataframe( df3 )
			
		with col2:
			st.markdown('##### Top entregadores mais lentos')
			df3 = top_delivers( df1, top_asc=False )
			st.dataframe( df3 )