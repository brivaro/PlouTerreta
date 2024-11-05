import streamlit as st
from datetime import datetime
from .visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data

def get_closest_data(df, column):
    """Encuentra el valor más cercano a la fecha actual en la columna especificada."""
    current_time = datetime.now()
    # Calcula la diferencia absoluta entre cada fecha y la fecha actual
    df['time_difference'] = abs(df['fecha_hora'] - current_time)
    # Encuentra el índice con la diferencia mínima
    closest_index = df['time_difference'].idxmin()
    return df.loc[closest_index, column]


def show_weather_data(weather_df):
    """Muestra los datos del clima organizados en la aplicación Streamlit."""
    if weather_df.empty:
        st.warning("No hay datos para mostrar.")
        return

    # Crear pestañas para cada tipo de gráfico
    tabs = st.tabs(["🌡️ Temperatura", "💧 Lluvia", "☁️ Condiciones del Cielo", "🍃 Viento"])
    
    # Temperatura (primera pestaña)
    with tabs[0]:
        st.subheader("Gráfico de Temperaturas")
        col1, col2 = st.columns([2, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            #st.write("Temperatura actual, mínima y máxima.")
            plot_temperature(weather_df)
        
        # Buscar las temperaturas más cercanas a la fecha actual
        temp_actual = get_closest_data(weather_df, 'temperature_value')
        temp_max = get_closest_data(weather_df, 'temperature_max')
        temp_min = get_closest_data(weather_df, 'temperature_min')

        # Mostrar métricas con emoticonos
        with col2:
            st.metric("🌡️ Temperatura Actual", f"{temp_actual}°C")
            st.metric("🔥 Temperatura Máxima", f"{temp_max}°C")
            st.metric("❄️ Temperatura Mínima", f"{temp_min}°C")

    # Probabilidad de Lluvia (segunda pestaña)
    with tabs[1]:
        st.subheader("Gráfico de Probabilidad de Precipitación")
        col1, col2 = st.columns([2, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            #st.write("Gráfico de probabilidad de lluvia.")
            plot_rain_chance(weather_df)
        
        # Obtener el dato de lluvia más cercano a la fecha actual
        lluvia_actual = get_closest_data(weather_df, 'precipitation_value')
        
        with col2:
            st.metric("☔ Lluvia Actual", f"{lluvia_actual}%")
            st.write("|-- ⚡ Alta probabilidad")
            st.write("|-- ☀️ Baja probabilidad")

    # Condiciones del Cielo (tercera pestaña)
    with tabs[2]:
        st.subheader("Gráfico de Condiciones del Cielo")
        
        # Crear dos columnas
        col1, col2 = st.columns([2, 1])  # Ajustar el ancho de las columnas
        
        # Columna 1: Gráfico de condiciones del cielo
        with col1:
            #st.write("Distribución de las condiciones del cielo.")
            plot_weather_conditions(weather_df)
        
        # Columna 2: Datos actuales de condiciones del cielo
        with col2:
            condicion_actual = get_closest_data(weather_df, "sky_description")
            st.metric("🌞 Condición Actual", condicion_actual)

    # Velocidad del Viento (cuarta pestaña)
    with tabs[3]:
        st.subheader("Gráfico de Velocidad del Viento")
        col1, col2 = st.columns([2, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            #st.write("Gráfico de velocidad del viento.")
            plot_wind_data(weather_df)
        
        # Obtener el dato de velocidad de viento más cercano a la fecha actual
        viento_actual = get_closest_data(weather_df, 'wind_speed')
        
        with col2:
            st.metric("🌀 Viento Actual", f"{viento_actual} km/h")
            st.write("|-- 🌪️ Fuerte")
            st.write("|-- 🍃 Suave")