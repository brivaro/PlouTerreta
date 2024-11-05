import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_temperature(data):
    """Genera un gráfico de temperatura máxima, mínima y actual por fecha y hora."""
    # Crear un gráfico de líneas para las temperaturas
    fig = px.line(data, 
                  x='fecha_hora', 
                  y=['temperature_value', 'temperature_max', 'temperature_min'],
                  title='Temperaturas por Fecha y Hora',
                  labels={'value': 'Temperatura (°C)', 'variable': 'Tipo'},
                  markers=True)

    # Cambiar las etiquetas de los tipos de temperatura
    fig.for_each_trace(lambda t: t.update(name=t.name.replace('temperature_value', 'Temperatura Actual')
                                            .replace('temperature_max', 'Temperatura Máxima')
                                            .replace('temperature_min', 'Temperatura Mínima')))
    
    fig.update_layout(yaxis_title='Temperatura (°C)', xaxis_title='Fecha y Hora')
    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit

def plot_rain_chance(data):
    """Genera un gráfico de probabilidad de precipitación por fecha y hora."""
    # Crear un gráfico de líneas para la probabilidad de precipitación
    fig = px.line(data,
                  x='fecha_hora',
                  y='precipitation_value',
                  title='Probabilidad de Precipitación por Fecha y Hora',
                  labels={'precipitation_value': 'Probabilidad (%)'},
                  markers=True)
    
    fig.update_layout(yaxis_title='Probabilidad de Precipitación (%)', xaxis_title='Fecha y Hora')
    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit

def plot_weather_conditions(data):
    """Genera un gráfico de condiciones del cielo por fecha y hora."""
    # Crear una figura de Plotly
    fig = go.Figure()

    # Añadir las barras para cada descripción del cielo
    for description in data['sky_description'].unique():
        filtered_data = data[data['sky_description'] == description]
        fig.add_trace(go.Bar(
            x=filtered_data['fecha_hora'],
            y=filtered_data['sky_value'],
            name=description,
        ))
    
    # Actualizar el diseño de la figura
    fig.update_layout(
        title='Frecuencia de Condiciones del Cielo por Fecha y Hora',
        xaxis_title='Fecha y Hora',
        yaxis_title='Número de Ocurrencias',
        barmode='group'  # Puedes cambiar a 'overlay' si deseas
    )

    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit

def plot_wind_data(data):
    """Genera un gráfico de velocidad del viento por fecha y hora."""
    # Crear un gráfico de líneas para la velocidad del viento
    fig = px.line(data,
                  x='fecha_hora',
                  y='wind_speed',
                  title='Velocidad del Viento por Fecha y Hora',
                  labels={'wind_speed': 'Velocidad del Viento (km/h)'},
                  markers=True)
    
    fig.update_layout(yaxis_title='Velocidad del Viento (km/h)', xaxis_title='Fecha y Hora')
    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit