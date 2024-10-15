import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# image_path = 'delivery.png'
image = Image.open('delivery.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('## Cury Company')
st.sidebar.markdown('### Fastest delivery in town')
st.sidebar.markdown(""" --- """)

st.header('Curry Company - Growth Dashboard')

st.sidebar.markdown('###### Powered by William Cardoso')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão empresa:
        - Visão Gerencial: métricas gerais de comportamento
        - Visão Tática: indicadores semanais de crescimento
        - Visão Geográfica: insights de geolocalização
    - Visão Entregadores:
        - Indicadores semanais de crescimento
    - Visão Restaurantes:
        - Indicadores semanais de crescimento

    ### Ask for Help
    - [👩‍💻 Desenvolvedor](https://github.com/wcardosoecom) = William Cardoso
    
        
        """
)
# qual comando no terminal para alterar para python 3.8?
# !pip install -U python
