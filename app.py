# Importar librerías
import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv('vehicles_us.csv')

# Título de la aplicación
st.header('Análisis de anuncios de venta de coches')

# Botón para mostrar histograma
hist_button = st.button('Construir histograma')

if hist_button:
    # Escribir mensaje
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    
    # Crear histograma
    fig = px.histogram(df, x="odometer")
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)

# Botón para mostrar gráfico de dispersión
scatter_button = st.button('Construir gráfico de dispersión')

if scatter_button:
    # Escribir mensaje
    st.write('Creación de un gráfico de dispersión para el conjunto de datos de anuncios de venta de coches')
    
    # Crear gráfico de dispersión
    fig = px.scatter(df, x="odometer", y="price")
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)