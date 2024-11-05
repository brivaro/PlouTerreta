import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_temperature(data):
    """Genera un gráfico de temperatura máxima, mínima y actual por fecha y hora."""
    # Crear un gráfico de líneas para las temperaturas
    fig = px.line(data, 
                  x='fecha_hora', 
                  y=['temperature_value', 'temperature_max', 'temperature_min'],
                  #title='Temperaturas por Fecha y Hora',
                  labels={'value': 'Temperatura (°C)', 'variable': 'Temp.'},
                  markers=True)

    # Cambiar las etiquetas de los tipos de temperatura
    fig.for_each_trace(lambda t: t.update(name=t.name.replace('temperature_value', 'Actual')
                                            .replace('temperature_max', 'Máxima')
                                            .replace('temperature_min', 'Mínima')))
    
    fig.update_layout(yaxis_title='Temperatura (°C)', xaxis_title='Fecha y Hora')
    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit

def plot_rain_chance(data):
    """Genera un gráfico de probabilidad de precipitación por fecha y hora con anotaciones de emoticonos."""
    # Crear el gráfico principal de líneas para la probabilidad de precipitación
    fig = px.line(data,
                  x='fecha_hora',
                  y='precipitation_value',
                  labels={'precipitation_value': 'Probabilidad (%)'},
                  markers=True)

    # Definir los niveles de probabilidad con emoticonos correspondientes
    emoji_levels = {
        0: "☀️",  # Soleado, sin lluvia
        20: "🌤️",  # Baja probabilidad de lluvia
        40: "🌦️",  # Probabilidad moderada de lluvia
        60: "🌧️",  # Alta probabilidad de lluvia
        80: "⛈️",  # Muy alta probabilidad de lluvia o tormenta
        100: "⚡"   # Tormenta con truenos
    }

    # Añadir anotaciones con emoticonos según el nivel de probabilidad
    for level, emoji in emoji_levels.items():
        fig.add_annotation(
            xref="paper", yref="y",
            x=1.05, y=level,  # Ajustar posición de los emojis al lado derecho
            text=emoji,
            showarrow=False,
            font=dict(size=14)
        )

    # Configurar diseño del gráfico
    fig.update_layout(
        yaxis_title="Probabilidad de Precipitación (%)",
        xaxis_title="Fecha y Hora",
        margin=dict(r=100)  # Espacio adicional para las anotaciones
    )

    # Mostrar el gráfico en la aplicación Streamlit
    st.plotly_chart(fig)


def plot_storm_chance(data):
    """Genera un gráfico de probabilidad de tormenta por fecha y hora con anotaciones de emoticonos."""
    # Preparar los datos para el gráfico
    fig = px.line(data,
                  x='fecha_hora',
                  y='storm_probability',
                  labels={'precipitation_value': 'Probabilidad (%)'},
                  markers=True)

    # Definir los niveles de probabilidad de tormenta con emoticonos correspondientes
    emoji_levels = {
        0: "☀️",  # Soleado, sin tormenta
        20: "🌤️",  # Baja probabilidad de tormenta
        40: "⛈️",  # Probabilidad moderada de tormenta
        60: "🌩️",  # Alta probabilidad de tormenta
        80: "⚡",   # Muy alta probabilidad de tormenta
        100: "🌪️"  # Tormenta severa
    }

    # Añadir anotaciones con emoticonos según el nivel de probabilidad
    for level, emoji in emoji_levels.items():
        fig.add_annotation(
            xref="paper", yref="y",
            x=1.05, y=level,  # Ajustar posición de los emojis al lado derecho
            text=emoji,
            showarrow=False,
            font=dict(size=14)
        )

    # Configurar diseño del gráfico
    fig.update_layout(
        yaxis_title="Probabilidad de Tormenta (%)",
        xaxis_title="Fecha y Hora",
        margin=dict(r=100)  # Espacio adicional para las anotaciones
    )

    # Mostrar el gráfico en la aplicación Streamlit
    st.plotly_chart(fig)


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
        #title='Frecuencia de Condiciones del Cielo por Fecha y Hora',
        xaxis_title='Fecha y Hora',
        yaxis_title='Puntuación del Cielo',
        barmode='group'  # Puedes cambiar a 'overlay' si deseas
    )

    st.plotly_chart(fig)  # Mostrar el gráfico en la aplicación Streamlit

def plot_wind_data(data):
    """Genera un gráfico de velocidad del viento por fecha y hora con anotaciones de emoticonos."""
    # Crear el gráfico principal de líneas para la velocidad del viento
    fig = px.line(data,
                  x='fecha_hora',
                  y='wind_speed',
                  labels={'wind_speed': 'Velocidad del Viento (km/h)'},
                  markers=True)

    # Definir los niveles de velocidad del viento con emoticonos correspondientes
    emoji_levels = {
        0: "🍃",    # Brisa suave
        5: "🌬️",  # Viento moderado
        10: "💨",   # Viento fuerte
        15: "🌪️",  # Viento muy fuerte
    }

    # Añadir anotaciones con emoticonos según el nivel de velocidad del viento
    for level, emoji in emoji_levels.items():
        fig.add_annotation(
            xref="paper", yref="y",
            x=1.05, y=level,  # Posición al lado derecho del gráfico
            text=emoji,
            showarrow=False,
            font=dict(size=14)
        )

    # Configuración del diseño del gráfico
    fig.update_layout(
        yaxis_title="Velocidad del Viento (km/h)",
        xaxis_title="Fecha y Hora",
        margin=dict(r=100)  # Espacio adicional para las anotaciones
    )

    # Mostrar el gráfico en la aplicación Streamlit
    st.plotly_chart(fig)
