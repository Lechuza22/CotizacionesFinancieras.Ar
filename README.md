# 📊 Índice de Inflación, Riesgo País y Precio del Dólar - Aplicación con Streamlit

Esta aplicación, desarrollada con **Streamlit**, proporciona una interfaz interactiva para consultar y analizar el comportamiento del **dólar**, la **inflación** y el **riesgo país** en Argentina. Permite obtener datos históricos, realizar comparaciones con gráficos dinámicos y generar predicciones con modelos de aprendizaje automático.

## 📌 Características principales

### 🔹 Consulta de datos en tiempo real
- Obtiene y visualiza datos del **precio del dólar**, **inflación** y **riesgo país** en Argentina.
- Presenta la evolución de estos indicadores con gráficos interactivos.

### 💵 Análisis del Precio del Dólar
- Consulta los valores de distintos tipos de dólar: **Oficial, Blue, MEP, CCL, Cripto, Tarjeta**, entre otros.
- Muestra la variación del precio del dólar con respecto al dólar oficial.
- Permite realizar conversiones entre **pesos y dólares** según la cotización seleccionada.
- Extrae **noticias en tiempo real** sobre el mercado cambiario desde **Google News RSS**.

### 📊 Análisis de tendencias
- Compara el comportamiento de la **inflación** con el **riesgo país** utilizando gráficos de **doble eje Y**.
- Representa gráficamente la relación entre la inflación y el dólar.

### 📈 Predicciones basadas en Machine Learning
- Predice la evolución futura del **precio del dólar blue**, **inflación** y **riesgo país** a **15, 30 y 60 días**.
- Utiliza modelos de **Regresión Lineal y ARIMA** para realizar proyecciones basadas en datos históricos.

## 🛠️ Tecnologías utilizadas

- **Python**
- **Streamlit** (Interfaz gráfica interactiva)
- **Pandas** (Manejo y procesamiento de datos)
- **Plotly** (Visualización de datos interactiva)
- **Scikit-Learn** (Regresión Lineal para predicción)
- **Statsmodels (ARIMA)** (Modelado de series temporales)
- **Feedparser** (Extracción de noticias desde RSS)
- **BeautifulSoup** (Scraping web)
- **Requests & HTTP Client** (Manejo de APIs externas)

## 📈 Funcionamiento del modelo de predicción

Para predecir la evolución del **dólar blue, la inflación y el riesgo país**:
- Se cargan los datos históricos desde archivos **JSON** o API externa.
- Se convierten las fechas al formato **datetime** y se limpian datos inconsistentes.
- Se optimizan los hiperparámetros del modelo ARIMA en base al **criterio AIC** para la predicción del dólar.
- Se entrena un modelo de **Regresión Lineal** para generar predicciones de inflación y riesgo país.
- Se muestran los resultados en gráficos interactivos con tendencias a corto, mediano y largo plazo.

## 🚀 Cómo ejecutar el proyecto

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación con Streamlit:
   ```bash
   streamlit run app.py
3. En Streamlit https://app-dolarbluehoy-cj6qwlmqwwgtkpkyzdkvz7.streamlit.app/ 
