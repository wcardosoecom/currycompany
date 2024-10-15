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

def order_metric(df1):
    df_aux = (df1.loc[:, ['ID', 'Order_Date']].groupby(
        ['Order_Date']).count().reset_index())
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig
###


def traffic_order_share(df1):
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby(
        ['Road_traffic_density']).count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum() * 100
    fig = px.pie(df_aux, values='entregas_perc',
                 names='Road_traffic_density')
    return fig
###


def traffic_order_city(df1):
    """ Essa função cria um grafico interativo com base nos dados do dataframe
    Input = Dataframe
    Output = Grafico interativo """
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(
        ['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x='City',
                     y='Road_traffic_density', size='ID', color='City')
    return fig

###


def order_week(df1):
    """ Essa função cria um grafico interativo com base nos dados do dataframe
    Input = Dataframe
    Output = Grafico interativo """
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'Week_of_year']].groupby(
        ['Week_of_year']).count().reset_index()
    fig = px.line(df_aux, x='Week_of_year', y='ID')
    return fig
###


def order_share_week(df1):
    """ Essa função cria um grafico interativo com base nos dados do dataframe
    Input = Dataframe
    Output = Grafico interativo """
    df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby(
        ['Week_of_year']).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby(
        ['Week_of_year']).nunique().reset_index()
    # juntar dois dataframes
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / \
        df_aux['Delivery_person_ID'].round(2)
    fig = px.line(df_aux, x='Week_of_year', y='order_by_deliver')
    return fig
###


def map_plot(df1):
    """ Essa função cria um mapa interativo com base nos dados do dataframe
    Input = Dataframe
    Output = Mapa interativo """
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude',
                          'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index())
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    return map
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


### =================================================== ###
#                   Index                         #
### =================================================== ###

st.set_page_config(page_title='Visão empresa', page_icon='🏢', layout='wide')

# colocando a imagem:
# image_path = 'delivery.png'
image = Image.open('delivery.png')
st.sidebar.image(image, width=120)

st.header('Marketplace - Visão Cliente')

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


tab1, tab2, tab3 = st.tabs(
    ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:  # Visao gerencial
    with st.container():
        st.markdown('#### Ordens por dia')  # gráfico de barra
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Ordens por tráfego')
        fig = traffic_order_share(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Tráfego por cidade')
        fig = traffic_order_city(df1)
        st.plotly_chart(fig, use_container_width=True)


with tab2:  # visão tática
    with st.container():
        st.markdown('#### Ordens por semana')
        fig = order_week(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('#### Order Share by Week')
        fig = order_share_week(df1)
        st.plotly_chart(fig, use_container_width=True)

with tab3:  # visão geográfica
    st.markdown('#### Mapa da cidade')
    map = map_plot(df1)
    folium_static(map, width=1024, height=600)
