# 💵 Precio del Dólar Hoy - Aplicación con Streamlit

Esta aplicación desarrollada con Streamlit proporciona una experiencia interactiva para consultar y analizar el comportamiento del dólar en Argentina. Permite obtener los valores de diferentes tipos de cambio, visualizar variaciones respecto al dólar oficial, realizar conversiones de moneda y analizar tendencias mediante modelos de predicción.

📌 Características principales
Consulta de precios en tiempo real

Obtiene el valor de distintos tipos de dólar (Oficial, Blue, MEP, CCL, Cripto, Tarjeta, etc.) utilizando la API de DolarAPI.
Presenta la cotización en una interfaz clara y visualmente atractiva.
Análisis de variaciones

Compara el precio de cada tipo de dólar con el valor oficial.
Representa gráficamente las diferencias en porcentaje.
Conversión de moneda

Calcula equivalencias entre pesos argentinos y dólares según la cotización seleccionada.
Soporta conversiones bidireccionales: de pesos a dólares y de dólares a pesos.
Noticias sobre el dólar en Argentina

Extrae noticias relevantes en tiempo real desde Google News RSS para mantenerse informado sobre cambios y regulaciones.
Predicción del Dólar Blue

Utiliza datos históricos para predecir la cotización futura del dólar blue.
Implementa un modelo ARIMA con selección automática de hiperparámetros.
Visualiza la tendencia con gráficos interactivos.
🛠️ Tecnologías utilizadas
Python
Streamlit (Interfaz gráfica)
Pandas (Manejo y procesamiento de datos)
Plotly (Visualización de datos interactiva)
Statsmodels (ARIMA) (Modelado de series temporales)
Scikit-Learn (Regresión lineal)
Feedparser (Extracción de noticias desde RSS)
BeautifulSoup (Scraping web)
Requests & HTTP Client (Manejo de APIs externas)
📈 Funcionamiento del modelo de predicción
Para la predicción del dólar blue:

Se carga un archivo CSV con el historial de cotizaciones.
Se convierten las fechas a formato datetime y se limpian datos inconsistentes.
Se optimizan los hiperparámetros (p, d, q) del modelo ARIMA con base en el criterio AIC.
Se entrena el modelo y se generan predicciones a corto, mediano y largo plazo.
Se muestran los resultados en una tabla con variaciones porcentuales y un gráfico de evolución.
🚀 Cómo ejecutar el proyecto
Instalar dependencias:
bash
Copiar
Editar
pip install -r requirements.txt
Ejecutar la aplicación:
bash
Copiar
Editar
streamlit run app.py
📄 Notas adicionales
Se implementó caché con st.cache_data para optimizar el rendimiento al obtener cotizaciones y noticias.
Se manejan excepciones en todas las solicitudes API para evitar interrupciones en la ejecución.
Se emplea diseño responsivo con Streamlit y gráficos interactivos.
Este resumen fundamenta el código explicando qué hace, cómo lo hace y por qué se eligieron ciertas herramientas. Si quieres que agregue algo más o haga cambios, dime.

