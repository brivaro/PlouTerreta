import requests, os, json 
import pandas as pd
from dotenv import load_dotenv  # Importa la función para cargar el .env

load_dotenv()  # Carga las variables de entorno desde el archivo .env
AEMET_API_KEY = os.getenv("AEMET_API_KEY") 

# PETICIÓN DE DATOS DIARIA
def get_weather_data():
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/46102"  # es quart de poblet DIARIA
    querystring = {"api_key": AEMET_API_KEY}
    headers = {
        'cache-control': "no-cache"
    }

    # Realiza la primera solicitud para obtener el enlace de los datos
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data_url = response.json()["datos"]

        # Realiza la segunda solicitud para obtener los datos meteorológicos
        weather_response = requests.get(data_url)
        if weather_response.status_code == 200:
            data = weather_response.text  # Guarda el texto del contenido
            data = json.loads(data)  # Convertir el string JSON a un objeto JSON
            return data
        else:
            print("Error al acceder a los datos:", weather_response.status_code)
            return None
    else:
        print("Error en la solicitud inicial:", response.status_code)
        return None
    

# PETICIÓN DE DATOS HORARIA
def get_weather_data2():
    url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/46102"  # es quart de poblet HORARIA
    querystring = {"api_key": AEMET_API_KEY}
    headers = {
        'cache-control': "no-cache"
    }

    # Realiza la primera solicitud para obtener el enlace de los datos
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data_url = response.json()["datos"]

        # Realiza la segunda solicitud para obtener los datos meteorológicos
        weather_response = requests.get(data_url)
        if weather_response.status_code == 200:
            data = weather_response.text  # Guarda el texto del contenido
            data = json.loads(data)  # Convertir el string JSON a un objeto JSON
            return data
        else:
            print("Error al acceder a los datos:", weather_response.status_code)
            return None
    else:
        print("Error en la solicitud inicial:", response.status_code)
        return None


# PETICIÓN DE DATOS USUARIO
def get_weather_data3(codigo_municipio):
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{codigo_municipio}"  # es el municipio pedido HORARIA 
    querystring = {"api_key": AEMET_API_KEY}
    headers = {
        'cache-control': "no-cache"
    }

    # Realiza la primera solicitud para obtener el enlace de los datos
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data_url = response.json()["datos"]

        # Realiza la segunda solicitud para obtener los datos meteorológicos
        weather_response = requests.get(data_url)
        if weather_response.status_code == 200:
            data = weather_response.text  # Guarda el texto del contenido
            data = json.loads(data)  # Convertir el string JSON a un objeto JSON
            return data
        else:
            print("Error al acceder a los datos:", weather_response.status_code)
            return None
    else:
        print("Error en la solicitud inicial:", response.status_code)
        return None


def get_codigo_municipio(selected_municipio):
    # Cargar el Excel desde la URL
    url = "https://www.ine.es/daco/daco42/codmun/diccionario24.xlsx"
    response = requests.get(url)

    if response.status_code == 200:
        # Guardar el archivo localmente o leerlo directamente en un DataFrame
        with open('municipios.xlsx', 'wb') as f:
            f.write(response.content)

        # Leer el archivo Excel
        df = pd.read_excel('municipios.xlsx', header=1)  # La fila 2 tiene los nombres de las columnas
        print(selected_municipio)

        # Buscar el municipio en el DataFrame
        municipio_data = df[df['NOMBRE'] == selected_municipio]
        print(municipio_data)

        if not municipio_data.empty:
            # Retornar el código del municipio, asegurándose de que CPRO y CMUN son strings
            cpro = str(municipio_data['CPRO'].values[0]).zfill(2)  # Asegurarse de que CPRO tiene al menos 2 dígitos
            cmun = str(municipio_data['CMUN'].values[0]).zfill(3)  # Asegurarse de que CMUN tiene al menos 3 dígitos
            print(cpro)
            print(cmun)
            return f"{cpro}{cmun}"  # Combinar CPRO y CMUN
        else:
            return None
    else:
        print("Error al cargar el archivo Excel.")
        return None