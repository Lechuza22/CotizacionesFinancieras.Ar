import streamlit as st
import http.client
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import feedparser
from sklearn.linear_model import LinearRegression
import numpy as np
import requests
from bs4 import BeautifulSoup
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import itertools
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from textblob import TextBlob
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Configurar la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵", layout="wide")

@st.cache_data
## Predicciones

def actualizar_datos_blue():
    """Actualiza el archivo Bluex12.csv con el precio más reciente del dólar blue."""
    try:
        df = pd.read_csv("Bluex12.csv", encoding="utf-8")
        df['category'] = pd.to_datetime(df['category'], errors='coerce')
        df.set_index('category', inplace=True)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['category', 'valor'])
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos: {e}")
        return
    
    # Obtener el precio actual del dólar blue
    datos = obtener_precio_dolar("blue")
    if "venta" in datos:
        nuevo_valor = datos["venta"]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verificar si ya se registró el valor del día
        if not df.empty and fecha_actual[:10] in df.index.strftime('%Y-%m-%d').values:
            st.info("Los datos ya están actualizados para hoy.")
        else:
            nuevo_registro = pd.DataFrame({"category": [fecha_actual], "valor": [nuevo_valor]})
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            df.to_csv("Bluex12.csv", index=False, encoding="utf-8")
            st.success("Datos del dólar blue actualizados correctamente.")
    else:
        st.warning("No se pudo obtener el precio del dólar blue.")

def cargar_datos():
    """Carga y procesa el archivo Bluex12.csv."""
    try:
        df = pd.read_csv("Bluex12.csv", encoding="utf-8")
        df['category'] = pd.to_datetime(df['category'], errors='coerce')
        df.set_index('category', inplace=True)
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

def predecir_dolar_blue(df, horas_prediccion):
    """Predice el valor del dólar blue usando ARIMA, tomando datos de la última semana."""
    df = df.sort_index()
    ultima_fecha = df.index[-1]
    df_reciente = df[df.index >= ultima_fecha - timedelta(days=7)]
    serie = df_reciente['valor']
    modelo = ARIMA(serie, order=(1,1,1))
    modelo_fit = modelo.fit()
    predicciones = modelo_fit.forecast(steps=horas_prediccion)
    fechas_prediccion = pd.date_range(start=ultima_fecha + timedelta(hours=1), periods=horas_prediccion, freq='H')
    df_predicciones = pd.DataFrame({'Fecha': fechas_prediccion, 'Predicción valor': predicciones})
    return df_predicciones

def mostrar_prediccion():
    st.title("📈 Predicción del Dólar Blue")
    df = cargar_datos()
    if df is not None and not df.empty:
        horas_prediccion = st.selectbox("Seleccione el horizonte de predicción (horas):", [3, 6, 12, 24, 36, 42, 72])
        df_predicciones = predecir_dolar_blue(df, horas_prediccion)
        st.subheader(f"Predicción para las próximas {horas_prediccion} horas")
        st.dataframe(df_predicciones)
        fig = px.line(df_predicciones, x='Fecha', y='Predicción valor', title=f"Predicción del Dólar Blue a {horas_prediccion} horas")
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudieron obtener los datos históricos para realizar la predicción.")

def obtener_precio_dolar(tipo):
    """Obtiene el precio del dólar desde la API con manejo de errores y caché."""
    try:
        conn = http.client.HTTPSConnection("dolarapi.com")
        conn.request("GET", f"/v1/dolares/{tipo}")
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": f"Error al obtener datos: {e}"}

# Diccionario con los tipos de dólar
tipos_dolar = {
    "Mayorista": "mayorista",
    "Oficial": "oficial",
    "MEP": "bolsa",
    "CCL": "contadoconliqui",
    "Cripto": "cripto",
    "Blue": "blue",
    "Tarjeta": "tarjeta"
}

def mostrar_precios():
    st.title("💵 Precio del dólar Hoy")
    
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))
    
    if st.button("🔄 Actualizar Precio"):
        datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])
        st.session_state[f"precio_{tipo_dolar}"] = datos  # Guardar en la sesión
    
    datos = st.session_state.get(f"precio_{tipo_dolar}", obtener_precio_dolar(tipos_dolar[tipo_dolar]))
    
    if "compra" in datos and "venta" in datos:
        compra = datos["compra"]
        venta = datos["venta"]
        
        st.markdown(
            f"""
            <div style="
                background-color: #222831;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: white;
            ">
                <span style="color: #33FF57;">💰 Compra: ${compra}</span><br>
                <span style="color: #FF5733;">📈 Venta: ${venta}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            📅 **Última actualización:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  
            📌 **Fuente:** [DolarAPI](https://dolarapi.com)
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"⚠️ No se pudo obtener el precio del dólar {tipo_dolar}.")

## VARIACIONESSSSSSS
def mostrar_variacion():
    st.title("📊 Variación de Cotizaciones respecto al Oficial")

    precios = {}

    for nombre, tipo in tipos_dolar.items():
        datos = obtener_precio_dolar(tipo)
        if "venta" in datos:
            precios[nombre] = datos["venta"]
    
    if "Oficial" in precios:
        oficial = precios["Oficial"]
        variaciones = {nombre: ((precio / oficial) - 1) * 100 for nombre, precio in precios.items() if precio}

        df_variaciones = pd.DataFrame({
            "Tipo de Dólar": list(variaciones.keys()),
            "Variación %": list(variaciones.values()),
            "Precio": [precios[nombre] for nombre in variaciones.keys()]
        })

        # Crear el gráfico
        fig = px.scatter(
            df_variaciones,
            x="Precio",
            y="Tipo de Dólar",
            size="Precio",
            color="Variación %",
            text="Precio",
            hover_data=["Variación %"],
            title="Variación de Cotizaciones respecto al Dólar Oficial",
            size_max=15,
            color_continuous_scale=px.colors.sequential.Viridis
        )

        fig.update_layout(
            xaxis_title="Precio en $", 
            yaxis_title="Tipo de Dólar"
        )

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudo obtener el precio del Dólar Oficial.")


def convertir_monedas():
    st.title("💱 Convertidor de Moneda")
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        compra, venta = datos["compra"], datos["venta"]
        monto = st.number_input("Ingrese el monto a convertir:", min_value=0.0, format="%.2f")
        conversion = st.radio("Seleccione el tipo de conversión:", ["Pesos a Dólares", "Dólares a Pesos"])

        if st.button("Convertir"):
            if conversion == "Pesos a Dólares":
                resultado = monto / venta
                st.success(f"💵 {monto} ARS equivale a **{resultado:.2f} USD**")
            else:
                resultado = monto * compra
                st.success(f"💵 {monto} USD equivale a **{resultado:.2f} ARS**")
                
def obtener_noticias():
    """Obtiene noticias sobre el dólar en Argentina desde Google News RSS."""
    try:
        feed_url = "https://news.google.com/rss/search?q=dólar+Argentina&hl=es-419&gl=AR&ceid=AR:es"
        feed = feedparser.parse(feed_url)
        noticias = []

        for entry in feed.entries[:10]:
            noticias.append({
                'titulo': entry.title,
                'enlace': entry.link,
                'fecha': entry.published if 'published' in entry else "Fecha no disponible",
                'fuente': entry.source.title if 'source' in entry else "Fuente desconocida"
            })

        return noticias if noticias else [{"titulo": "No hay noticias disponibles", "enlace": "#", "fecha": "", "fuente": ""}]
    except Exception as e:
        return [{"titulo": f"Error al obtener noticias: {e}", "enlace": "#", "fecha": "", "fuente": ""}]

def mostrar_noticias():
    st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")
    if st.button("🔄 Actualizar Noticias"):
        noticias = obtener_noticias()
    else:
        noticias = obtener_noticias()
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    st.write(f"📅 **Última actualización:** {fecha_hoy}")
    
    for noticia in noticias:
        st.write(f"**{noticia['titulo']}**")
        st.write(f"📅 {noticia['fecha']} | 📰 {noticia['fuente']}")
        st.markdown(f"[Ver noticia completa]({noticia['enlace']})")
        st.markdown("---")
# =========================
# 📊 ANÁLISIS TÉCNICO
# =========================

def calcular_indicadores(df):
    df['SMA_7'] = df['valor'].rolling(window=7).mean()
    df['EMA_7'] = df['valor'].ewm(span=7, adjust=False).mean()
    df['RSI'] = calcular_rsi(df['valor'], 14)
    df['Upper_BB'], df['Lower_BB'] = calcular_bollinger_bands(df['valor'])
    return df

def calcular_rsi(series, window=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calcular_bollinger_bands(series, window=20, num_std=2):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, lower_band

def mostrar_analisis_tecnico():
    st.title("📊 Análisis Técnico del Dólar Blue")
    df = cargar_datos()
    if df is not None and not df.empty:
        df = calcular_indicadores(df)
        st.subheader("Indicadores Técnicos Clásicos")
        fig = px.line(df, x=df.index, y=['valor', 'SMA_7', 'EMA_7'], title="Media Móvil Simple y Exponencial")
        st.plotly_chart(fig)

        fig_bb = px.line(df, x=df.index, y=['valor', 'Upper_BB', 'Lower_BB'], title="Bandas de Bollinger")
        st.plotly_chart(fig_bb)

        fig_rsi = px.line(df, x=df.index, y=['RSI'], title="Índice de Fuerza Relativa (RSI)")
        st.plotly_chart(fig_rsi)

        st.write("El RSI por debajo de 30 indica sobreventa y por encima de 70 indica sobrecompra.")
        
        st.subheader("📈 Modelos de Machine Learning para Predicción")
        modelo_seleccionado = st.selectbox("Seleccione un modelo:", ["Regresión Lineal", "Random Forest", "LSTM"])
        
        if modelo_seleccionado == "Regresión Lineal":
            predicciones = predecir_regresion_lineal(df)
        elif modelo_seleccionado == "Random Forest":
            predicciones = predecir_random_forest(df)
        elif modelo_seleccionado == "LSTM":
            predicciones = predecir_lstm(df)

        st.subheader("Predicción del Precio del Dólar Blue")
        st.dataframe(predicciones)
        fig_pred = px.line(predicciones, x='Fecha', y='Predicción valor', title=f"Predicción con {modelo_seleccionado}")
        st.plotly_chart(fig_pred)
    else:
        st.warning("⚠️ No se pudieron obtener los datos históricos para realizar el análisis técnico.")

# Modelos de ML

def predecir_regresion_lineal(df):
    df['timestamp'] = df.index.astype(int) / 10**9
    X = df[['timestamp']].values.reshape(-1, 1)
    y = df['valor'].values
    modelo = LinearRegression()
    modelo.fit(X, y)
    futuro = pd.date_range(df.index[-1] + timedelta(hours=1), periods=24, freq='H')
    X_futuro = np.array(futuro.astype(int) / 10**9).reshape(-1, 1)
    y_pred = modelo.predict(X_futuro)
    return pd.DataFrame({'Fecha': futuro, 'Predicción valor': y_pred})

def predecir_random_forest(df):
    df['timestamp'] = df.index.astype(int) / 10**9
    X = df[['timestamp']].values.reshape(-1, 1)
    y = df['valor'].values
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X, y)
    futuro = pd.date_range(df.index[-1] + timedelta(hours=1), periods=24, freq='H')
    X_futuro = np.array(futuro.astype(int) / 10**9).reshape(-1, 1)
    y_pred = modelo.predict(X_futuro)
    return pd.DataFrame({'Fecha': futuro, 'Predicción valor': y_pred})

def predecir_lstm(df):
    df['timestamp'] = df.index.astype(int) / 10**9
    X = df[['timestamp']].values.reshape(-1, 1)
    y = df['valor'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    y_scaled = scaler.fit_transform(y)
    modelo = Sequential([
        LSTM(50, return_sequences=True, input_shape=(1, 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    modelo.compile(optimizer='adam', loss='mean_squared_error')
    modelo.fit(X, y_scaled, epochs=10, batch_size=1, verbose=0)
    futuro = pd.date_range(df.index[-1] + timedelta(hours=1), periods=24, freq='H')
    X_futuro = np.array(futuro.astype(int) / 10**9).reshape(-1, 1)
    y_pred_scaled = modelo.predict(X_futuro)
    y_pred = scaler.inverse_transform(y_pred_scaled)
    return pd.DataFrame({'Fecha': futuro, 'Predicción valor': y_pred.flatten()})

# =========================
# 📊 ANÁLISIS DE SENTIMIENTO
# =========================

def obtener_noticias():
    """Obtiene noticias sobre el dólar en Argentina desde Google News RSS."""
    try:
        feed_url = "https://news.google.com/rss/search?q=dólar+Argentina&hl=es-419&gl=AR&ceid=AR:es"
        feed = feedparser.parse(feed_url)
        noticias = []
        for entry in feed.entries[:10]:
            noticias.append({
                'titulo': entry.title,
                'enlace': entry.link,
                'fecha': entry.published if 'published' in entry else "Fecha no disponible",
                'fuente': entry.source.title if 'source' in entry else "Fuente desconocida"
            })
        return noticias if noticias else [{"titulo": "No hay noticias disponibles", "enlace": "#", "fecha": "", "fuente": ""}]
    except Exception as e:
        return [{"titulo": f"Error al obtener noticias: {e}", "enlace": "#", "fecha": "", "fuente": ""}]

def analizar_sentimiento(texto):
    """Analiza el sentimiento de un texto usando TextBlob y VADER."""
    sia = SentimentIntensityAnalyzer()
    blob = TextBlob(texto)
    polaridad_textblob = blob.sentiment.polarity
    vader_score = sia.polarity_scores(texto)['compound']
    promedio = (polaridad_textblob + vader_score) / 2
    if promedio > 0.1:
        return "Positivo"
    elif promedio < -0.1:
        return "Negativo"
    else:
        return "Neutro"

def mostrar_analisis_sentimiento():
    st.title("📰 Análisis de Sentimiento sobre el Dólar")
    noticias = obtener_noticias()
    for noticia in noticias:
        sentimiento = analizar_sentimiento(noticia['titulo'])
        st.write(f"**{noticia['titulo']}** ({sentimiento})")
        st.write(f"📅 {noticia['fecha']} | 📰 {noticia['fuente']}")
        st.markdown(f"[Ver noticia completa]({noticia['enlace']})")
        st.markdown("---")

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias", "Predicción del Dólar Blue", "Análisis Técnico", "Análisis de Sentimiento"])
    if menu_seleccionado == "Precios":
        mostrar_precios()
    elif menu_seleccionado == "Variación de Cotizaciones":
        mostrar_variacion()
    elif menu_seleccionado == "Convertir":
        convertir_monedas()
    elif menu_seleccionado == "Novedades y Noticias":
        mostrar_noticias()
    elif menu_seleccionado == "Predicción del Dólar Blue":
        mostrar_prediccion()
    elif menu_seleccionado == "Análisis Técnico":
        mostrar_analisis_tecnico()
    elif menu_seleccionado == "Análisis de Sentimiento":
        mostrar_analisis_sentimiento()
    
