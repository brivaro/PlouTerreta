import streamlit as st
from app.data_fetching import get_weather_data3, get_codigo_municipio
from app.data_processing_hour import process_weather_data
from app.visualization import plot_temperature, plot_rain_chance, plot_weather_conditions, plot_wind_data
from app.ui_components import show_weather_data

# Lista de municipios disponibles
municipios = [
    "Alaquàs", "Aldaia", "Algemesí", "Alzira", "Burjassot", "Catarroja", 
    "Gandia", "Manises", "Mislata", "Oliva", "Ontinyent", "Paiporta", 
    "Paterna", "Quart de Poblet", "Sagunto/Sagunt", "Sueca", "Torrent", 
    "València", "Xàtiva", "Xirivella"
]

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="PlouTerreta",
        page_icon="🌦️",
        layout="wide",  # Opciones: "centered" o "wide"
        initial_sidebar_state="expanded"  # Opciones: "auto", "expanded", "collapsed"
    )

    st.sidebar.title("Parámetros")
    
    # Establecer 'Quart de Poblet' como municipio predeterminado
    selected_municipio = st.sidebar.selectbox("Selecciona un municipio:", municipios, index=13)  # Índice 13 corresponde a Quart de Poblet

    # Mostrar el nombre del municipio seleccionado
    st.header(f"Municipio: {selected_municipio}")

    # Obtener el código del municipio (CPRO y CMUN) mediante la nueva función
    codigo_municipio = get_codigo_municipio(selected_municipio)

    if codigo_municipio:
        # Obtener datos y procesarlos
        data = get_weather_data3(codigo_municipio)
        if data:
            # Procesar los datos del clima
            weather_df = process_weather_data(data[0]["prediccion"]["dia"])

            # Mostrar los datos procesados en la aplicación
            show_weather_data(weather_df)
        else:
            st.error("No se pudieron cargar los datos")
    else:
        st.error("Código de municipio no encontrado")

if __name__ == "__main__":
    main()
