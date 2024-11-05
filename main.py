import streamlit as st
from app.data_fetching import get_weather_data2
from app.data_processing_hour import process_weather_data
from app.visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data
from app.ui_components import show_weather_data

def main():
    st.sidebar.title("Parámetros")
    st.sidebar.text("Selección de opciones")

    # Obtener datos y procesarlos
    data = get_weather_data2()
    if data:
        # Procesar los datos del clima
        weather_df = process_weather_data(data[0]["prediccion"]["dia"])

        # Mostrar los datos procesados en la aplicación
        show_weather_data(weather_df)

        # Graficar las temperaturas
        st.subheader("Gráfico de Temperaturas")
        plot_temperature(weather_df)

        # Graficar la probabilidad de precipitación
        st.subheader("Gráfico de Probabilidad de Precipitación")
        plot_rain_chance(weather_df)

        # Graficar las condiciones del cielo
        st.subheader("Gráfico de Condiciones del Cielo")
        plot_weather_conditions(weather_df)

        # Graficar los datos del viento
        st.subheader("Gráfico de Velocidad del Viento")
        plot_wind_data(weather_df)

    else:
        st.error("No se pudieron cargar los datos")

if __name__ == "__main__":
    main()
