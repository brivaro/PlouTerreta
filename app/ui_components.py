import streamlit as st
from datetime import datetime, timedelta
from .visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data
import pandas as pd

def get_closest_data(df, column):
    """Encuentra el valor más cercano a la fecha actual en la columna especificada."""
    current_time = datetime.now()
    # Calcula la diferencia absoluta entre cada fecha y la fecha actual
    df['time_difference'] = abs(df['fecha_hora'] - current_time)
    # Encuentra el índice con la diferencia mínima
    closest_index = df['time_difference'].idxmin()
    return df.loc[closest_index, column]

def get_next_day_data(weather_df):
    """Obtiene los datos del día siguiente."""
    next_day = datetime.now() + timedelta(days=1)
    # Filtrar el DataFrame para el día siguiente
    next_day_data = weather_df[weather_df['fecha_hora'].dt.date == next_day.date()]

    # Asegurarse de que los valores sean numéricos
    next_day_data['precipitation_value'] = pd.to_numeric(next_day_data['precipitation_value'], errors='coerce')
    
    # Obtener las temperaturas máximas y mínimas y la máxima probabilidad de precipitación
    if not next_day_data.empty:
        temp_max_next = next_day_data['temperature_max'].max()
        temp_min_next = next_day_data['temperature_min'].min()
        lluvia_max_next = next_day_data['precipitation_value'].max()
        viento_max_next = next_day_data['wind_speed'].max()
        
        # Obtener la condición del cielo con el mayor sky_value
        condicion_max_sky_value = next_day_data.loc[next_day_data['sky_value'].idxmax(), 'sky_description']
        
        return temp_max_next, temp_min_next, lluvia_max_next, condicion_max_sky_value, viento_max_next
    else:
        return None, None, None, None  # Devolver None si no hay datos

def show_weather_data(weather_df):
    """Muestra los datos del clima organizados en la aplicación Streamlit."""
    if weather_df.empty:
        st.warning("No hay datos para mostrar.")
        return

    # Crear pestañas para cada tipo de gráfico
    tabs = st.tabs(["📊 Resumen", "🌡️ Temperatura", "💧 Lluvia", "☁️ Condiciones del Cielo", "🍃 Viento"])
    
    # Resumen (primera pestaña)
    with tabs[0]:
        col1, col2 = st.columns([2, 2])  # Ajustar el ancho de las columnas

        with col1:
            st.subheader("📝 Pronóstico para Hoy")

            # Datos actuales
            temp_actual = get_closest_data(weather_df, 'temperature_value')
            temp_max = get_closest_data(weather_df, 'temperature_max')
            temp_min = get_closest_data(weather_df, 'temperature_min')
            lluvia_actual = get_closest_data(weather_df, 'precipitation_value')
            viento_actual = get_closest_data(weather_df, 'wind_speed')  # Viento actual
            condicion_actual = get_closest_data(weather_df, "sky_description")

            # Mostrar información actual
            st.metric("🌡️ Temperatura Actual", f"{temp_actual}°C")
            st.metric("🔥 Temperatura Máxima", f"{temp_max}°C")
            st.metric("❄️ Temperatura Mínima", f"{temp_min}°C")
            st.metric("☔ Lluvia Actual", f"{lluvia_actual}%")
            st.metric("🌀 Viento Actual", f"{viento_actual} km/h")  # Añadir viento actual
            st.metric("🌞 Condición Actual", condicion_actual)

        with col2:
            # Datos del día siguiente
            temp_max_next, temp_min_next, lluvia_max_next, condicion_max_sky_value, viento_max_next = get_next_day_data(weather_df)
            if temp_max_next is not None:
                st.subheader("📅 Pronóstico para Mañana")
                st.metric("🔥 Temperatura Máxima", f"{temp_max_next}°C")
                st.metric("❄️ Temperatura Mínima", f"{temp_min_next}°C")
                st.metric("☔ Máxima Probabilidad de Lluvia", f"{lluvia_max_next}%")
                st.metric("🌀 Viento Máximo", f"{viento_max_next} km/h") 
                st.metric("🌞 Condición Máxima", condicion_max_sky_value)  # Condición del cielo con mayor sky_value
            else:
                st.warning("No hay datos disponibles para el día siguiente.")

    # Temperatura (segunda pestaña)
    with tabs[1]:
        st.subheader("Gráfico de Temperaturas")
        col1, col2 = st.columns([3, 1])  # Ajustar el ancho de las columnas
        
        with col1:
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

    # Probabilidad de Lluvia (tercera pestaña)
    with tabs[2]:
        st.subheader("Gráfico de Probabilidad de Precipitación")
        col1, col2 = st.columns([3, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            plot_rain_chance(weather_df)
        
        # Obtener el dato de lluvia más cercano a la fecha actual
        lluvia_actual = get_closest_data(weather_df, 'precipitation_value')
        
        with col2:
            st.metric("☔ Lluvia Actual", f"{lluvia_actual}%")
            st.write("|-- ⚡ Alta probabilidad")
            st.write("|-- ☀️ Baja probabilidad")

    # Condiciones del Cielo (cuarta pestaña)
    with tabs[3]:
        st.subheader("Gráfico de Condiciones del Cielo")
        
        # Crear dos columnas
        col1, col2 = st.columns([3, 1])  # Ajustar el ancho de las columnas
        
        # Columna 1: Gráfico de condiciones del cielo
        with col1:
            plot_weather_conditions(weather_df)
        
        # Columna 2: Datos actuales de condiciones del cielo
        with col2:
            condicion_actual = get_closest_data(weather_df, "sky_description")
            st.metric("🌞 Condición Actual", condicion_actual)

    # Velocidad del Viento (quinta pestaña)
    with tabs[4]:
        st.subheader("Gráfico de Velocidad del Viento")
        col1, col2 = st.columns([3, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            plot_wind_data(weather_df)
        
        # Obtener el dato de velocidad de viento más cercano a la fecha actual
        viento_actual = get_closest_data(weather_df, 'wind_speed')
        
        with col2:
            st.metric("🌀 Viento Actual", f"{viento_actual} km/h")
            st.write("|-- 🌪️ Fuerte")
            st.write("|-- 🍃 Suave")
