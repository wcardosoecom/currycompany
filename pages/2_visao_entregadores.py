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


def avaliacao_entregador(df1):
    """ Essa função cria um dataframe com a média
    das avaliações de cada entregador
    Input = Dataframe
    Output = dataframe """
    df_rd = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
             .groupby('Delivery_person_ID')
             .mean().
             reset_index())
    df_rd.columns = ['ID do entregador', 'Avaliação']
    df_rd['Avaliação'] = df_rd['Avaliação'].round(2)
    return df_rd
###


def avaliacao_transito(df1):
    """ Essa função cria um dataframe com a média e
    desvião padrão das avaliações por cada tipo de trânsito
    Input = Dataframe
    Output = dataframe """
    df_av = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
             .groupby('Road_traffic_density')
             .agg({'Delivery_person_Ratings': ['mean', 'std']})
             .reset_index())
    df_av.columns = ['Condição do trânsito', 'Avaliação', 'Desvio']
    df_av['Avaliação'] = df_av['Avaliação'].round(2)
    df_av['Desvio'] = df_av['Desvio'].round(2)
    return df_av
###


def avaliacao_clima(df1):
    """ Essa função cria um dataframe com a média e 
    desvião padrão das avaliações por cada tipo de clima
    Input = Dataframe
    Output = dataframe """
    df_rc = (df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']]
             .groupby('Weatherconditions')
             .agg({'Delivery_person_Ratings': ['mean', 'std']})
             .reset_index())
    df_rc.columns = ['Clima', 'Avaliação', 'Desvio']
    df_rc['Avaliação'] = df_rc['Avaliação'].round(2)
    df_rc['Desvio'] = df_rc['Desvio'].round(2)
    return df_rc
###


def entregador_rapido(df1):
    """ Essa função cria um dataframe com os 10 entregadores
    mais rapidos de cada cidade e seu tempo médio de entrega
    Input = Dataframe
    Output = dataframe """
    df10r = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
             .groupby(['City', 'Delivery_person_ID'])
             .mean()
             .sort_values(['City', 'Time_taken(min)'], ascending=False)
             .reset_index())
    df_aux1 = df10r.loc[df10r['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df10r.loc[df10r['City'] == 'Urban', :].head(10)
    df_aux3 = df10r.loc[df10r['City'] == 'Semi-Urban', :].head(10)
    df10r = pd.concat([df_aux1, df_aux2, df_aux3]
                      ).reset_index(drop=True)
    df10r.columns = ['Entregador', 'Cidade', 'Tempo médio de entrega']
    return df10r
###


def top_entregadores(df1, top_asc):
    """ Essa função cria um dataframe com os entregadores e o
    tempo médio de entrega por cada cidade 
    (top_asc define 10 mais rapidos(False) ou lentos(True))
    Input = Dataframe
    Output = dataframe """
    df10l = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
             .groupby(['City', 'Delivery_person_ID'])
             .mean()
             .sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
             .reset_index())
    df_aux1 = df10l.loc[df10l['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df10l.loc[df10l['City'] == 'Urban', :].head(10)
    df_aux3 = df10l.loc[df10l['City'] == 'Semi-Urban', :].head(10)
    df10l = pd.concat([df_aux1, df_aux2, df_aux3]
                      ).reset_index(drop=True)
    df10l.columns = ['Entregador', 'Cidade', 'Tempo médio de entrega']
    return df10l
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

st.set_page_config(page_title='Visão Entregadores',
                   page_icon='🪂', layout='wide')

# colocando a imagem:
# image_path = 'delivery.png'
image = Image.open('delivery.png')
st.sidebar.image(image, width=120)

st.header('Marketplace - Visão Entregadores')


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
    st.markdown('#### Métricas gerais')
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        # A maior idade dos entregadores
        maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Maior idade', maior_idade)
    with col2:
        # A menor idade dos entregadores
        menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric('Menor idade', menor_idade)
    with col3:
        # A melhor condição de veículo
        melhor_veiculo = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric('Melhor condição de veículo', melhor_veiculo)
    with col4:
        # A pior condição de veículo
        pior_veiculo = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric('Pior condição de veículo', pior_veiculo)

st.markdown("""---""")
with st.container():
    st.markdown('#### Avaliações')
    col1, col2, = st.columns(2)
    with col1:
        # Avaliação média por entregador
        st.markdown('#### Avaliação média por entregador')
        df_rd = avaliacao_entregador(df1)
        st.dataframe(df_rd)

    with col2:
        # Avaliação média por trânsito
        st.markdown('###### Avaliação média por trânsito')
        df_av = avaliacao_transito(df1)
        st.dataframe(df_av)

    # Avaliação média por clima
        st.markdown('###### Avaliação média por clima')
        df_rc = avaliacao_clima(df1)
        st.dataframe(df_rc)

st.markdown("""---""")
with st.container():
    st.markdown('#### Velocidade de entrega')
    col1, col2, = st.columns(2)
    with col1:
        st.markdown('###### Entregadores mais rápidos')
        df10r = top_entregadores(df1, top_asc=False)
        st.dataframe(df10r)

    with col2:
        st.markdown('###### Entregadores mais lentos')
        df10l = top_entregadores(df1, top_asc=True)
        st.dataframe(df10l)
