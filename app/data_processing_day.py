import pandas as pd
import re

def extract_temperature(data):
    """Extrae las temperaturas máximas, mínimas y el valor específico de cada intervalo de tiempo por día."""
    temperature_data = {}

    # Lista de periodos predeterminados
    default_periods = ['00-06', '06-12', '12-18', '18-24']

    for day in data:
        day_data = {}
        periods = day["temperatura"]["dato"]
        fecha = day["fecha"]  # Asigna la fecha como clave principal

        if periods:
            for i, period in enumerate(periods):
                # Define el periodo en formato de rango
                if i == 0:
                    period_key = "00-06"
                else:
                    start_hour = periods[i-1]["hora"]
                    end_hour = period["hora"]
                    period_key = f"{start_hour:02d}-{end_hour:02d}"

                # Crea la entrada del periodo en el diccionario del día
                if period_key not in day_data:
                    day_data[period_key] = {
                        "max": day["temperatura"]["maxima"],
                        "min": day["temperatura"]["minima"],
                        "value": period["value"]
                    }
        else:
            # Si `periods` está vacío, crea los periodos predeterminados
            for period_key in default_periods:
                day_data[period_key] = {
                    "max": day["temperatura"]["maxima"],
                    "min": day["temperatura"]["minima"],
                    "value": None
                }

        # Agrega el diccionario del día completo usando la fecha como clave
        temperature_data[fecha] = day_data

    return temperature_data


def extract_precipitation(data):
    """Extrae la probabilidad de precipitación por periodo de cada día."""
    precipitation_data = {}

    # Lista de periodos predeterminados
    default_periods = ['00-24', '00-12', '12-24', '00-06', '06-12', '12-18', '18-24']

    for day in data:
        day_data = {}
        periods = day.get("probPrecipitacion", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                # Verifica si el campo "periodo" está en el diccionario "period"
                if "periodo" in period:
                    period_key = period["periodo"]
                    # Añade el valor de precipitación para el periodo si existe
                    day_data[period_key] = {"value": period.get("value", None)}
        
        # Si algún periodo no está, agrega los periodos predeterminados
        for period_key in default_periods:
            # Añade periodos predeterminados si están ausentes en day_data
            if period_key not in day_data:
                day_data[period_key] = {"value": None}

        # Agrega el diccionario del día completo usando la fecha como clave
        precipitation_data[fecha] = day_data

    return precipitation_data


def extract_weather_conditions(data):
    """Extrae la descripción de las condiciones del cielo por periodo de cada día."""
    weather_conditions_data = {}

    # Lista de periodos predeterminados
    default_periods = ['00-24', '00-12', '12-24', '00-06', '06-12', '12-18', '18-24']

    for day in data:
        day_data = {}
        periods = day.get("estadoCielo", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                # Verifica si el campo "periodo" está en el diccionario "period"
                if "periodo" in period:
                    period_key = period["periodo"]
                    # Extrae solo los dígitos del campo "value"
                    value = period.get("value", None)
                    if value:
                        value = re.search(r'\d+', value).group() if re.search(r'\d+', value) else None
                    
                    # Añade la descripción y el valor para el periodo si existen
                    day_data[period_key] = {
                        "value": value,
                        "descripcion": period.get("descripcion", None)
                    }
        
        # Si algún periodo predeterminado falta, agrégalo con valores None
        for period_key in default_periods:
            if period_key not in day_data:
                day_data[period_key] = {
                    "value": None,
                    "descripcion": None
                }

        # Agrega el diccionario del día completo usando la fecha como clave
        weather_conditions_data[fecha] = day_data

    return weather_conditions_data


def extract_wind_data(data):
    """Extrae la velocidad y dirección del viento por periodo de cada día."""
    wind_data = {}

    # Lista de periodos predeterminados
    default_periods = ['00-24', '00-12', '12-24', '00-06', '06-12', '12-18', '18-24']

    for day in data:
        day_data = {}
        periods = day.get("viento", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                # Verifica si el campo "periodo" está en el diccionario "period"
                period_key = period.get("periodo")
                if period_key:
                    # Añade la dirección y velocidad del viento para el periodo si existen
                    day_data[period_key] = {
                        "direccion": period.get("direccion", None),
                        "velocidad": period.get("velocidad", None)
                    }

        # Si algún periodo predeterminado falta, agrégalo con valores None
        for period_key in default_periods:
            if period_key not in day_data:
                day_data[period_key] = {
                    "direccion": None,
                    "velocidad": None
                }

        # Agrega el diccionario del día completo usando la fecha como clave
        wind_data[fecha] = day_data

    return wind_data

def extract_uv_index(data):
    """Extrae el índice UV máximo por periodo de cada día."""


def process_weather_data(data):
    """
    Procesa los datos completos del tiempo, llamando a cada función de extracción
    y organizando la información en un DataFrame para facilitar el análisis.
    """
    # Extrae datos individuales de cada aspecto del clima
    temperature_data = extract_temperature(data)
    precipitation_data = extract_precipitation(data)
    weather_conditions_data = extract_weather_conditions(data)
    wind_data = extract_wind_data(data)

    # Lista para almacenar todas las filas antes de convertir a DataFrame
    rows = []

    # Itera sobre las fechas y periodos para organizar los datos en filas
    for fecha in temperature_data:
        for period_key in temperature_data[fecha]:
            row = {
                "fecha": fecha,
                "periodo": period_key,
                "temperature_max": temperature_data[fecha][period_key].get("max"),
                "temperature_min": temperature_data[fecha][period_key].get("min"),
                "temperature_value": temperature_data[fecha][period_key].get("value"),
                "precipitation_value": precipitation_data[fecha].get(period_key, {}).get("value"),
                "sky_value": weather_conditions_data[fecha].get(period_key, {}).get("value"),
                "sky_description": weather_conditions_data[fecha].get(period_key, {}).get("descripcion"),
                "wind_direction": wind_data[fecha].get(period_key, {}).get("direccion"),
                "wind_speed": wind_data[fecha].get(period_key, {}).get("velocidad")
            }
            rows.append(row)

    # Convertir la lista de filas a un DataFrame
    weather_df = pd.DataFrame(rows)

    return weather_df
