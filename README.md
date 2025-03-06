# 📊 Cotizaciones financieras.Ar - Aplicación con Streamlit

Esta aplicación, desarrollada con Streamlit, proporciona una interfaz interactiva para consultar y analizar el comportamiento del dólar, la inflación y el riesgo país en Argentina. Permite obtener datos en tiempo real, analizar tendencias históricas, realizar comparaciones con gráficos interactivos y generar predicciones basadas en modelos de aprendizaje automático.

## 📌 Características principales

### 🔹 Consulta de datos en tiempo real

- Obtiene y visualiza datos actualizados sobre el precio del dólar, inflación y riesgo país en Argentina.
- Presenta la evolución de estos indicadores con gráficos dinámicos e interactivos.
- Extrae noticias en tiempo real sobre el mercado cambiario desde Google News RSS.

### 💵 Análisis del Precio del Dólar

- Consulta los valores de distintos tipos de dólar: Oficial, Blue, MEP, CCL, Cripto, Tarjeta, entre otros.
- Muestra la variación del precio del dólar respecto al dólar oficial.
- Permite realizar conversiones entre pesos y dólares según la cotización seleccionada.
- Integra un convertidor de moneda interactivo.

### 📊 Análisis de tendencias

- Compara el comportamiento de la inflación con el riesgo país utilizando gráficos de doble eje Y.
- Representa gráficamente la relación entre la inflación y el dólar blue.
- Incorpora análisis técnico con indicadores como RSI, medias móviles y Bandas de Bollinger.

### 📈 Predicciones basadas en Machine Learning

- Predice la evolución futura del precio del dólar blue, la inflación y el riesgo país a 15, 30 y 60 días.
- Utiliza modelos como **Regresión Lineal, Random Forest, ARIMA y Prophet** para realizar proyecciones basadas en datos históricos.
- Incorpora modelos de series temporales optimizados para predicciones confiables.

### 🌐 Análisis de Sentimiento

- Obtiene noticias recientes sobre el dólar en Argentina desde **Google News**.
- Analiza el sentimiento de los titulares utilizando **TextBlob y VADER**.
- Genera una **nube de palabras** con los términos más frecuentes en noticias sobre el dólar.

## 🛠️ Tecnologías utilizadas

- **Python**
- **Streamlit** (Interfaz gráfica interactiva)
- **Pandas** (Manejo y procesamiento de datos)
- **Plotly** (Visualización de datos interactiva)
- **Scikit-Learn** (Regresión Lineal y Random Forest para predicción)
- **Statsmodels (ARIMA)** (Modelado de series temporales)
- **Facebook Prophet** (Predicción de tendencias económicas)
- **Feedparser** (Extracción de noticias desde RSS)
- **BeautifulSoup** (Scraping web)
- **Requests & HTTP Client** (Manejo de APIs externas)

## 📊 Funcionamiento del modelo de predicción

- Se cargan los datos históricos desde archivos JSON o una API externa.
- Se convierten las fechas al formato **datetime** y se limpian datos inconsistentes.
- Se optimizan los hiperparámetros del modelo **ARIMA** en base al criterio AIC para la predicción del dólar.
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
3. En Streamlit https://cotizacionesfinancierasar.streamlit.app/ 

## 🌟 Posibles aplicaciones en un negocio de ventas 

Esta aplicación puede ser utilizada por emprendedores y comercios del sector gastronómico para tomar decisiones financieras más informadas. Algunas de sus aplicaciones incluyen:

- Planificación de compras: Si el dólar blue o la inflación muestran una tendencia alcista, se pueden adelantar compras de insumos importados para evitar sobrecostos.
- Fijación de precios: Un análisis de la inflación permite ajustar los precios de productos de manera estratégica para mantener la rentabilidad.
- Control de costos: La variación del dólar puede afectar el precio de utensilios de cocina importados, por lo que monitorear el mercado permite optimizar costos.
- Inversión en stock: Si las predicciones indican una suba del dólar, puede ser conveniente incrementar el stock de productos antes de futuros aumentos.
- Proyección de ventas: Si la economía muestra signos de inestabilidad, las ventas pueden verse afectadas. Tener estos datos a disposición permite ajustar estrategias comerciales.
