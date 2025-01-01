# 🌦️ PlouTerreta - Comunidad Valenciana

Bienvenido a **PlouTerreta App** 🌞, tu herramienta para estar siempre al tanto del tiempo en la Comunidad Valenciana, España. Consulta información meteorológica en tiempo real y recibe alertas sobre posibles fenómenos climáticos adversos.

## 📋 Funcionalidades

Con esta app, podrás consultar:
- 📉 **Gráficas** de precipitaciones y otros parámetros climatológicos.
- 🌡️ **Temperaturas** mínimas y máximas diarias.
- ☔ **Probabilidades de lluvia** actualizadas.
- ⚠️ **Alertas** sobre posibles fenómenos climáticos adversos.

## 🛠️ Tecnologías Usadas

- **Streamlit** para la interfaz de usuario.
- **API de AEMET OpenData** para los datos meteorológicos.
- **Plotly** para las gráficas y visualización de datos.
- **Python** como lenguaje principal.

## 🚀 Cómo ejecutar el proyecto

1. **Crea tu cuenta en AEMET OpenData** para obtener una **API Key**. Puedes hacerlo desde [este enlace](https://opendata.aemet.es/).
   
2. **Clona el repositorio**:
   ```bash
   git clone https://github.com/brivaro/PlouTerreta
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la API Key**: 
   - Crea un archivo `.env` dentro de la carpeta **app** y agrega el parámetro `AEMET_API_KEY` con el valor de tu clave de API obtenida.
   - Ejemplo de archivo `.env`:
     ```env
     AEMET_API_KEY=tu_api_key_aqui
     ```

5. **Ejecuta la app**:
   ```bash
   streamlit run main.py
   ```


## 🌐 Estructura del Repositorio

- **📁 app**: Contiene scripts para obtener y procesar datos de la API, visualización de los datos obtenidos y componentes de interfaz en Streamlit.
- **📁 municipios**: Archivos de prueba y municipios registrados en AEMET.
- **main.py**: Archivo principal para ejecutar la aplicación.
- **README.md**: Archivo de presentación del proyecto.
- **requirements.txt**: Dependencias necesarias para ejecutar el proyecto.

## 🖥️ Contribuciones

🙌 La aplicación está construida en **Streamlit** y obtiene sus datos de la **API de AEMET OpenData**. ¡Nos encantaría recibir tus sugerencias! 💡


## 📝 Licencia

Este proyecto se distribuye bajo la Licencia MIT. 📄

---

Gracias por visitar **PlouTerreta App** 🌍☁️. ¡Esperamos que te sea de utilidad para estar al tanto del clima en la Comunidad Valenciana!