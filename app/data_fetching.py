import requests, os, json
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