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

def obtener_datos_dolar_blue():
    url = "https://www.ambito.com/contenidos/dolar-informal-historico.html"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        st.error("⚠️ No se pudo obtener los datos del dólar blue. Verifique la conexión o si la página ha cambiado.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Prueba encontrar la tabla con diferentes métodos
    tabla = soup.find('table')
    if not tabla:
        tablas = soup.find_all('table')
        if tablas:
            tabla = tablas[0]  # Intenta con la primera tabla si hay más de una
    
    if not tabla:
        st.error("⚠️ No se encontró la tabla con datos históricos en la página. Puede haber cambiado el diseño del sitio.")
        return None
    
    headers = [header.text.strip() for header in tabla.find_all('th')]
    rows = []
    for row in tabla.find_all('tr')[1:]:
        cols = row.find_all('td')
        rows.append([col.text.strip() for col in cols])
    
    if not rows:
        st.error("⚠️ No se encontraron datos en la tabla de la página web.")
        return None
    
    df = pd.DataFrame(rows, columns=headers)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
    df['Venta'] = pd.to_numeric(df['Venta'].str.replace(',', ''), errors='coerce')
    
    df.dropna(inplace=True)
    return df

def predecir_dolar_blue(df, dias_prediccion):
    df = df.sort_values('Fecha')
    df.set_index('Fecha', inplace=True)
    serie = df['Venta']
    modelo = ARIMA(serie, order=(5, 1, 0))
    modelo_fit = modelo.fit()
    predicciones = modelo_fit.forecast(steps=dias_prediccion)
    fechas_prediccion = pd.date_range(start=serie.index[-1] + pd.Timedelta(days=1), periods=dias_prediccion)
    df_predicciones = pd.DataFrame({'Fecha': fechas_prediccion, 'Predicción Venta': predicciones})
    return df_predicciones

def mostrar_prediccion():
    st.title("📈 Predicción del Dólar Blue")
    df = obtener_datos_dolar_blue()
    if df is not None and not df.empty:
        dias_prediccion = st.selectbox("Seleccione el horizonte de predicción (días):", [5, 10, 15, 30])
        df_predicciones = predecir_dolar_blue(df, dias_prediccion)
        st.subheader(f"Predicción para los próximos {dias_prediccion} días")
        st.dataframe(df_predicciones)
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df['Venta'], label='Histórico')
        plt.plot(df_predicciones['Fecha'], df_predicciones['Predicción Venta'], label='Predicción', linestyle='--')
        plt.xlabel('Fecha')
        plt.ylabel('Precio de Venta')
        plt.title('Predicción del Dólar Blue')
        plt.legend()
        st.pyplot(plt)
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
