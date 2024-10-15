### libraries ###
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import date
import datetime
from datetime import time
from datetime import datetime
from numpy import inner
from pandas.core.internals import concat
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np
######################################################################

### FUNÇÕES ###


def tempo_festival(df1, operation, true):
    """ Essa função cria um int com a média e 
    desvião padrão das entregas com ou sem festival.
    operation = 'media' ou 'desvio'
    true = 'Yes' ou 'No'
    Input = Dataframe
    Output = int """
    df_df = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']}))
    df_df.columns = ['media', 'desvio']
    df_df = df_df.reset_index()
    df_df = df_df.loc[df_df['Festival'] ==
                      true, operation].round(2)
    return df_df
###


def distancia_media(df1):
    """ Essa função cria um int com a distancia media em km
    Input = Dataframe
    Output = int """
    distance_cols = ['Delivery_location_latitude', 'Delivery_location_longitude',
                     'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = (df1.loc[:, distance_cols].apply
                       (lambda x: haversine((x['Delivery_location_latitude'], x['Delivery_location_longitude']),
                                            (x['Restaurant_latitude'], x['Restaurant_longitude'])), axis=1))
    distancia_media = df1['distance'].mean().round(2)
    col1.metric('Distância média (km)', distancia_media)
###


def time_cidade(df1):
    """ Essa função cria um grafico de pizza pie com base nos dados do dataframe
    Input = Dataframe
    Output = Gráfico Pizza Pie """
    df_tc = df1.loc[:, ['City', 'Time_taken(min)']].groupby(
        'City').agg({'Time_taken(min)': ['mean', 'std']})
    df_tc.columns = ['Tempo_medio', 'Desvio']
    df_tc = df_tc.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_tc['City'],
                         y=df_tc['Tempo_medio'], error_y=dict(type='data', array=df_tc['Desvio'])))
    return fig
###


def time_cidade_df(df1):
    """ Essa função cria um dataframe com o tempo medio das entregas por cidade
    Input = Dataframe
    Output = Dataframe """
    df_dt = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                .groupby(['City', 'Type_of_order'])
                .agg({'Time_taken(min)': ['mean', 'std']}))
    df_dt.columns = ['Tempo_medio', 'Desvio']
    df_dt = df_dt.reset_index()
    return df_dt
###


def ddm_cidade(df1):
    """ Essa função cria um grafico de barras com a distancia media das entregas, 
    por cidade com sobreposição do desvio padrao
    Input = Dataframe
    Output = Gráfico de barras """
    distancia_media = df1.loc[:, ['City', 'distance']].groupby(
        'City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=distancia_media['City'],
                    values=distancia_media['distance'], pull=[0, 0.1, 0])])
    return fig
###


def tm_cidade_tipo(df1):
    """ Essa função cria um grafico sunburst com a media e desvio padrao (burst) das entregas,
    por cidade e por tipo de trânsito
    Input = Dataframe
    Output = Gráfico Sunburst """
    df_te = (df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                .groupby(['City', 'Road_traffic_density'])
                .agg({'Time_taken(min)': ['mean', 'std']}))
    df_te.columns = ['Tempo_medio', 'Desvio']
    df_te = df_te.reset_index()
    fig = px.sunburst(df_te, path=['City', 'Road_traffic_density'],
                      values='Tempo_medio',
                      color='Desvio',
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_te['Desvio']))
    return fig
###


def clean_code(df1):
    """ Essa função faz a limpeza do dataframe
        Tipos de limpeza:
        1. Remocão dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remocão dos espacos das strings
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável)

        Input = Dataframe
        Output = Dataframe
    """
    ### LIMPEZA ###
    df1 = df.copy()
    # eliminar nan idade do entregador + transformar de object para int
    lista_eliminar = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[lista_eliminar, :]
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    # transformar avaliação do entregador de object para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(
        float)
    # transformar Order_Date de object em data
    df1['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
    # eliminar nan da multiple_deliveries + transformar de object em int
    lista_eliminar = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[lista_eliminar, :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    lista_eliminar = df1['City'] != 'NaN '
    df1 = df1.loc[lista_eliminar, :]
    # resetar index e limpar os espaços vazios
    df1 = df1.reset_index(drop=True)
    # for i in range(len(df1)):
    #  df1.loc[i,'ID'] = df1.loc[i,'ID'].strip( )
    # df1.loc[i,'Type_of_order'] = df1.loc[i,'Type_of_order'].strip( )
    # df1.loc[i,'Type_of_vehicle'] = df1.loc[i,'Type_of_vehicle'].strip( )
    # df1.loc[i,'Festival'] = df1.loc[i,'Festival'].strip( )
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,
                                                 'Road_traffic_density'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(
        lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

######################################################################
### ESTRUTURA LÓGICA DO CÓDIGO ###


### IMPORTAÇÃO DOS DADOS ###
df = pd.read_csv('dataset/train.csv')
### LIMPEZA DOS DADOS ###
df1 = clean_code(df)

################################################################################

### =================================================== ###
#                   Index                         #
### =================================================== ###

st.set_page_config(page_title='Visão Restaurantes',
                   page_icon='🍽', layout='wide')

# colocando a imagem:
# image_path = 'delivery.png'
image = Image.open('delivery.png')
st.sidebar.image(image, width=120)

st.header('Marketplace - Visão Restaurantes')


### =================================================== ###
#                   Barra lateral                         #
### =================================================== ###

# informações da barra lateral
st.sidebar.markdown('## Cury Company')
st.sidebar.markdown('### Fastest delivery in town')
st.sidebar.markdown(""" --- """)

# filtro para seleção de data limite.
st.sidebar.markdown('#### Selecione uma data limite:')

date_slider = st.sidebar.slider(
    'A partir de qual data deseja analisar?',
    value=datetime(2022, 1, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

date_slider2 = st.sidebar.slider(
    'Até qual data deseja analisar?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown(""" --- """)

# multipla seleção das condições de trânsito:
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown('#### Powered by William Cardoso')

# filtro de datas
linhas_selecionadas = df1['Order_Date'] > date_slider
df1 = df1.loc[linhas_selecionadas, :]
linhas_selecionadas = df1['Order_Date'] < date_slider2
df1 = df1.loc[linhas_selecionadas, :]

# filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# testar se o filtro funcionou
# st.dataframe(df1.head())

### =================================================== ###
#                   layout streamlit                      #
### =================================================== ###


with st.container():
    # primeira linha - 6 informações divididas em 3 colunas
    st.markdown('#### Métricas gerais')
    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        # st.markdown('###### Entregadores únicos')
        q_entregadores_unicos = len(df1['Delivery_person_ID'].unique())
        col1.metric('Entregadores únicos', q_entregadores_unicos)

        # st.markdown('###### Distância média')
        distancia_media(df1)

    with col2:
        # st.markdown('###### Tempo médio das entregas no Festival')
        col2.metric('Tempo médio das entregas no Festival',
                    tempo_festival(df1, operation='media', true='Yes'))

        # st.markdown('###### Desvio padrão das entregas no Festival')
        col2.metric('Desvio padrão das entregas no Festival',
                    tempo_festival(df1, operation='desvio', true='Yes'))

    with col3:
        # st.markdown('###### Tempo médio das entregas sem Festival')
        col3.metric('Tempo médio das entregas sem Festival',
                    tempo_festival(df1, operation='media', true='No'))

        # st.markdown('###### Desvio padrão das entregas sem Festival')
        col3.metric('Desvio padrão das entregas sem Festival',
                    tempo_festival(df1, operation='desvio', true='No'))

with st.container():
    # segunda linha, duas colunas
    col1, col2 = st.columns(2)
    with col1:  # grafico de barras
        st.markdown('##### Distribuição do tempo por cidade')
        fig = time_cidade(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # dataframe
        st.markdown('##### Tempo médio por cidade')
        df_dt = time_cidade_df(df1)
        st.dataframe(df_dt)

with st.container():
    # terceira linha - 2 colunas
    col1, col2 = st.columns(2)
    with col1:
        # Gráfico de pizza pie
        st.markdown(
            '##### Distribuição da distância média de entrega por cidade')
        fig = ddm_cidade(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Gráfico Sunburst
        st.markdown('##### Tempo médio por cidade e tipo de entrega')
        fig = tm_cidade_tipo(df1)
        st.plotly_chart(fig, use_container_width=True)
