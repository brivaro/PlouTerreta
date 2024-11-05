import streamlit as st
from .visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data

def show_weather_data(weather_df):
    """Muestra los datos del clima en la aplicación Streamlit."""
    if weather_df.empty:
        st.warning("No hay datos para mostrar.")
        return

    # Muestra la tabla de datos meteorológicos
    st.subheader("Datos Meteorológicos")
    st.dataframe(weather_df)

    # Muestra gráficos adicionales si es necesario
    if 'temperature_value' in weather_df.columns:
        st.subheader("Gráfico de Temperaturas")
        plot_temperature(weather_df)

    if 'precipitation_value' in weather_df.columns:
        st.subheader("Gráfico de Probabilidad de Precipitación")
        plot_rain_chance(weather_df)

    if 'sky_value' in weather_df.columns:
        st.subheader("Gráfico de Condiciones del Cielo")
        plot_weather_conditions(weather_df)

    if 'wind_speed' in weather_df.columns:
        st.subheader("Gráfico de Velocidad del Viento")
        plot_wind_data(weather_df)
