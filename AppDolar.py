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

# Configurar la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵", layout="wide")

# =========================
# 🚀 FUNCIONES MEJORADAS
# =========================
@st.cache_data
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

@st.cache_data
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

# Obtener la fecha y hora actual
fecha_actualizacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

## Predicciones

@st.cache_data
def cargar_datos():
    """Carga el archivo CSV con los datos del dólar blue y ajusta el índice temporal."""
    try:
        df = pd.read_csv("Bluex12.csv", encoding="utf-8")
        st.write("### Vista previa de los datos:")
        st.write(df.head())
        
        # Verificar columnas disponibles
        st.write("### Columnas en el archivo CSV:")
        st.write(list(df.columns))
        
        if 'category' not in df.columns:
            raise ValueError("La columna 'category' no se encuentra en el archivo CSV.")
        if 'valor' not in df.columns:
            raise ValueError("La columna 'valor' no se encuentra en el archivo CSV. Verifique los nombres de las columnas.")
        
        # Convertir las columnas necesarias
        df['category'] = pd.to_numeric(df['category'], errors='coerce')
        df = df.dropna(subset=['category'])
        df['category'] = df['category'].astype(int)
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df.set_index('category', inplace=True)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

@st.cache_data
def encontrar_mejores_hiperparametros(serie):
    """Encuentra los mejores hiperparámetros para el modelo ARIMA usando una búsqueda de cuadrícula."""
    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))
    mejor_aic = float("inf")
    mejor_pdq = None
    for param in pdq:
        try:
            modelo = ARIMA(serie, order=param)
            modelo_fit = modelo.fit()
            if modelo_fit.aic < mejor_aic:
                mejor_aic = modelo_fit.aic
                mejor_pdq = param
        except:
            continue
    return mejor_pdq

def predecir_dolar_blue(df, dias_prediccion):
    """Realiza la predicción del dólar blue usando el mejor modelo ARIMA."""
    df = df.sort_index()
    serie = df['valor']
    mejores_parametros = encontrar_mejores_hiperparametros(serie)
    modelo = ARIMA(serie, order=mejores_parametros)
    modelo_fit = modelo.fit()
    predicciones = modelo_fit.forecast(steps=dias_prediccion)
    ultimo_indice = df.index[-1]
    if pd.isna(ultimo_indice):
        raise ValueError("El índice 'category' contiene valores NaN o no es válido.")
    categorias_prediccion = list(range(int(ultimo_indice) + 1, int(ultimo_indice) + 1 + dias_prediccion))
    df_predicciones = pd.DataFrame({'category': categorias_prediccion, 'Predicción valor': predicciones})
    df_predicciones['Variación %'] = (df_predicciones['Predicción valor'].pct_change()) * 100
    return df_predicciones

def mostrar_prediccion():
    st.title("📈 Predicción del Dólar Blue")
    df = cargar_datos()
    if df is not None:
        dias_prediccion = st.selectbox("Seleccione el horizonte de predicción (días):", [3, 5, 10, 15, 30])
        df_predicciones = predecir_dolar_blue(df, dias_prediccion)
        st.subheader(f"Predicción para los próximos {dias_prediccion} días")
        
        # Mostrar tabla con variación en color
        def resaltar_variacion(val):
            color = 'green' if val > 0 else 'red' if val < 0 else 'black'
            return f'color: {color}'
        df_predicciones_styled = df_predicciones.style.applymap(resaltar_variacion, subset=['Variación %'])
        st.dataframe(df_predicciones_styled)
        
        # Graficar los datos históricos y las predicciones
        fig = px.line(df_predicciones, x='category', y='Predicción Venta', title=f"Predicción del Dólar Blue a {dias_prediccion} días")
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudieron obtener los datos históricos para realizar la predicción.")



# =========================
# 💵 MOSTRAR PRECIOS
# =========================
def mostrar_precios():
    st.title("💵 Precio del dólar Hoy")

    # Selector para elegir el tipo de dólar a mostrar
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))

    # Obtener el precio del tipo de dólar seleccionado
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        compra = datos["compra"]
        venta = datos["venta"]

        # Mostrar cuadro con compra y venta en colores
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

        # Mostrar fecha de actualización y fuente
        st.markdown(
            f"""
            📅 **Última actualización:** {fecha_actualizacion}  
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

# =========================
# 💱 CONVERTIR MONEDAS
# =========================
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

# =========================
# 📰 MOSTRAR NOTICIAS
# =========================
def mostrar_noticias():
    st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")
    noticias = obtener_noticias()
    
    for noticia in noticias:
        st.write(f"**{noticia['titulo']}**")
        st.write(f"📅 {noticia['fecha']} | 📰 {noticia['fuente']}")
        st.markdown(f"[Ver noticia completa]({noticia['enlace']})")
        st.markdown("---")

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias", "Predicción del Dólar Blue"])
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
