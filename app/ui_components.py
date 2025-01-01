import streamlit as st
from datetime import datetime, timedelta
from .visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data, plot_storm_chance
import pandas as pd

def get_closest_data(df, column):
    """Encuentra el valor más cercano a la fecha actual en la columna especificada."""
    current_time = datetime.now()
    # Calcula la diferencia absoluta entre cada fecha y la fecha actual
    df['time_difference'] = abs(df['fecha_hora'] - current_time)
    # Encuentra el índice con la diferencia mínima
    closest_index = df['time_difference'].idxmin()
    return df.loc[closest_index, column]

def get_today_precipitation_data(weather_df):
    """Obtiene la precipitación máxima del día actual."""
    today = datetime.now().date()
    today_data = weather_df[weather_df['fecha_hora'].dt.date == today]
    today_data['precipitation_value'] = pd.to_numeric(today_data['precipitation_value'], errors='coerce')

    if not today_data.empty:
        lluvia_max = today_data['precipitation_value'].max()
        if lluvia_max > 0:
            lluvia_max_time = today_data.loc[today_data['precipitation_value'].idxmax(), 'fecha_hora'].strftime("%H:%M")
            return lluvia_max, lluvia_max_time
    return 0, None

def get_today_storm_data(weather_df):
    """Obtiene la probabilidad de tormenta y la hora de inicio de la tormenta del día actual."""
    today = datetime.now().date()
    today_data = weather_df[weather_df['fecha_hora'].dt.date == today]
    today_data['storm_probability'] = pd.to_numeric(today_data['storm_probability'], errors='coerce')  # Suponiendo que hay una columna 'storm_chance'

    if not today_data.empty:
        tormenta_max = today_data['storm_probability'].max()
        if tormenta_max > 0:
            tormenta_max_time = today_data.loc[today_data['storm_probability'].idxmax(), 'fecha_hora'].strftime("%H:%M")
            return tormenta_max, tormenta_max_time
    return 0, None


def get_next_day_data(weather_df):
    """Obtiene los datos del día siguiente."""
    next_day = datetime.now() + timedelta(days=1)
    next_day_data = weather_df[weather_df['fecha_hora'].dt.date == next_day.date()]
    next_day_data['precipitation_value'] = pd.to_numeric(next_day_data['precipitation_value'], errors='coerce')
    next_day_data['storm_probability'] = pd.to_numeric(next_day_data['storm_probability'], errors='coerce')

    if not next_day_data.empty:
        temp_max_next = next_day_data['temperature_max'].max()
        temp_min_next = next_day_data['temperature_min'].min()
        lluvia_max_next = next_day_data['precipitation_value'].max()
        lluvia_max_time = next_day_data.loc[next_day_data['precipitation_value'].idxmax(), 'fecha_hora'].strftime("%H:%M")
        viento_max_next = next_day_data['wind_speed'].max()
        condicion_max_sky_value = next_day_data.loc[next_day_data['sky_value'].idxmax(), 'sky_description']
        tormenta_max_next = next_day_data['storm_probability'].max()
        tormenta_max_time_next = next_day_data.loc[next_day_data['storm_probability'].idxmax(), 'fecha_hora'].strftime("%H:%M")

        return temp_max_next, temp_min_next, lluvia_max_next, lluvia_max_time, condicion_max_sky_value, viento_max_next, tormenta_max_next, tormenta_max_time_next
    return None, None, None, None, None, None



def show_weather_data(weather_df):
    """Muestra los datos del clima organizados en la aplicación Streamlit."""
    if weather_df.empty:
        st.warning("No hay datos para mostrar.")
        return

    # Crear pestañas para cada tipo de gráfico
    tabs = st.tabs(["📊 Resumen", "🌡️ Temperatura", "💧 Lluvia y Tormenta", "☁️ Condiciones del Cielo", "🍃 Viento"])
    
    # Resumen (primera pestaña)
    with tabs[0]:
        col1, col2 = st.columns([2, 2])  # Ajustar el ancho de las columnas

        with col1:
            st.header("📝 Pronóstico para Hoy")

            # Datos actuales
            temp_actual = get_closest_data(weather_df, 'temperature_value')
            temp_max = get_closest_data(weather_df, 'temperature_max')
            temp_min = get_closest_data(weather_df, 'temperature_min')
            lluvia_actual = get_closest_data(weather_df, 'precipitation_value')
            viento_actual = get_closest_data(weather_df, 'wind_speed')  # Viento actual
            condicion_actual = get_closest_data(weather_df, "sky_description")
            tormenta_actual = get_closest_data(weather_df, "storm_probability")
            lluvia_actual_max, lluvia_hora_inicio = get_today_precipitation_data(weather_df)
            tormenta_actual_max, tormenta_hora_inicio = get_today_storm_data(weather_df)

            # Mostrar información actual
            st.metric("🌡️ Temperatura Actual", f"{temp_actual}°C")
            st.metric("🔥 Temperatura Máxima", f"{temp_max}°C")
            st.metric("❄️ Temperatura Mínima", f"{temp_min}°C")
            st.metric("☔ Lluvia Actual", f"{lluvia_actual}%")
            st.metric("⚡ Tormenta Actual", f"{tormenta_actual}%")
            st.metric("🌀 Viento Actual", f"{viento_actual} km/h")
            st.metric("🌞 Condición Actual", condicion_actual)
            #st.metric("☔ Máxima Probabilidad de Lluvia", f"{lluvia_actual_max}%")
            if lluvia_actual_max is not 0:
                st.metric("☔🕒 Inicio de Lluvia", lluvia_hora_inicio)
            #st.metric("⚡ Máxima Probabilidad de Tormenta", f"{tormenta_actual_max}%")
            if tormenta_actual_max is not 0:
                st.metric("⚡🕒 Inicio de Tormenta", tormenta_hora_inicio)
            

        with col2:
            # Datos del día siguiente
            temp_max_next, temp_min_next, lluvia_max_next, lluvia_hora_inicio, condicion_max_sky_value, viento_max_next, tormenta_max_next, tormenta_hora_inicio_next = get_next_day_data(weather_df)
            if temp_max_next is not None:
                st.header("📅 Pronóstico para Mañana")
                
                st.metric("🔥 Temperatura Máxima", f"{temp_max_next}°C")
                st.metric("❄️ Temperatura Mínima", f"{temp_min_next}°C")
                st.metric("☔ Máxima Probabilidad de Lluvia", f"{lluvia_max_next}%")
                if lluvia_max_next is not 0:
                    st.metric("🕒 Inicio de Lluvia", f"{lluvia_hora_inicio}")
                st.metric("⚡ Máxima Probabilidad de Tormenta", f"{tormenta_max_next}%")
                if tormenta_max_next is not 0:
                    st.metric("🕒 Inicio de Tormenta", f"{tormenta_hora_inicio_next}")
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
        col1, col2 = st.columns([3, 1])  # Ajustar el ancho de las columnas
        
        with col1:
            st.subheader("Gráfico de Probabilidad de Precipitación")
            plot_rain_chance(weather_df)
            st.subheader("Gráfico de Probabilidad de Tormenta")
            plot_storm_chance(weather_df)
        
        # Obtener el dato de lluvia y tormenta más cercano a la fecha actual
        lluvia_actual = get_closest_data(weather_df, 'precipitation_value')
        tormenta_actual = get_closest_data(weather_df, 'storm_probability')
        
        with col2:
            st.metric("☔ Lluvia Actual", f"{lluvia_actual}%")
            st.metric("⚡ Tormenta Actual", f"{tormenta_actual}%")

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
