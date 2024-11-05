import pandas as pd
import re

def extract_temperature(data):
    """Extrae las temperaturas máximas, mínimas y el valor específico de cada intervalo de tiempo por hora."""
    temperature_data = {}

    for day in data:
        day_data = {}
        periods = day["temperatura"]
        fecha = day["fecha"]  # Asigna la fecha como clave principal

        # Listas para almacenar los valores de temperatura
        values = []

        if periods:
            for i, period in enumerate(periods):
                # Obtiene el periodo directamente del dato
                period_key = period["periodo"]  # Usa la hora directamente como clave
                value = int(period["value"])  # Convierte el valor a entero
                values.append(value)  # Agrega el valor a la lista

                # Almacena el valor específico del periodo
                day_data[period_key] = {
                    "value": value
                }

                if i == len(periods)-1: # porque el septimo es el ultimo dia de datos de pronosticos
                    for key in day_data:
                        day_data[key]["min"] = min(values)  # Temperatura mínima del día
                        day_data[key]["max"] = max(values)  # Temperatura máxima del día

        # Agrega el diccionario del día completo usando la fecha como clave
        temperature_data[fecha] = day_data

    return temperature_data

def extract_precipitation(data):
    """Extrae la probabilidad de precipitación por periodo de cada hora, dividiendo los periodos en horas individuales."""
    precipitation_data = {}

    for day in data:
        day_data = {}
        periods = day.get("probPrecipitacion", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                if "periodo" in period:
                    period_key = period["periodo"]
                    # Extrae las horas de la clave del periodo
                    start_hour = int(period_key[:2])
                    end_hour = int(period_key[2:])  # Suponiendo que el periodo tiene formato HHMM

                    # Itera sobre cada hora en el rango y asigna el valor
                    for hour in range(start_hour, end_hour + 1):  # +1 para incluir la última hora
                        hour_key = f"{hour:02d}"  # Formato de dos dígitos
                        day_data[hour_key] = {"value": period.get("value", None)}

        # Agrega el diccionario del día completo usando la fecha como clave
        precipitation_data[fecha] = day_data

    return precipitation_data

def extract_weather_conditions(data):
    """Extrae la descripción de las condiciones del cielo por periodo de cada hora."""
    weather_conditions_data = {}

    for day in data:
        day_data = {}
        periods = day.get("estadoCielo", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                # Usa el periodo directamente del dato
                if "periodo" in period:
                    period_key = period["periodo"]
                    # Extrae solo los dígitos del campo "value"
                    value = period.get("value", None)
                    if value:
                        value = re.search(r'\d+', value).group() if re.search(r'\d+', value) else None
                    
                    day_data[period_key] = {
                        "value": value,
                        "descripcion": period.get("descripcion", None)
                    }

        # Agrega el diccionario del día completo usando la fecha como clave
        weather_conditions_data[fecha] = day_data

    return weather_conditions_data

def extract_wind_data(data):
    """Extrae la velocidad y dirección del viento por periodo de cada hora."""
    wind_data = {}

    for day in data:
        day_data = {}
        periods = day.get("vientoAndRachaMax", [])
        fecha = day["fecha"]  # Usa la fecha como clave principal

        # Si hay periodos, procesa cada uno
        if periods:
            for period in periods:
                # Usa el periodo directamente del dato
                if "periodo" in period and "direccion" in period:
                    period_key = period["periodo"]
                    day_data[period_key] = {
                        "direccion": period["direccion"][0],
                        "velocidad": int(period["velocidad"][0])
                    }
                else:
                    # Si el periodo ya existe, agrega la velocidad máxima al diccionario existente
                    day_data[period_key]["vel_max"] = int(period.get("value", 0))

        # Agrega el diccionario del día completo usando la fecha como clave
        wind_data[fecha] = day_data

    return wind_data

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
                "precipitation_value": precipitation_data.get(fecha, {}).get(period_key, {}).get("value", 0),
                "sky_value": weather_conditions_data.get(fecha, {}).get(period_key, {}).get("value", "N/A"),
                "sky_description": weather_conditions_data.get(fecha, {}).get(period_key, {}).get("descripcion", "N/A"),
                "wind_direction": wind_data.get(fecha, {}).get(period_key, {}).get("direccion", "N/A"),
                "wind_speed": wind_data.get(fecha, {}).get(period_key, {}).get("velocidad", 0),
                # Crear una columna de fecha y hora combinada
                "fecha_hora": pd.to_datetime(fecha + ' ' + period_key + ':00')
            }
            rows.append(row)

    # Convertir la lista de filas a un DataFrame
    weather_df = pd.DataFrame(rows)

    return weather_df

