import streamlit as st
import http.client
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
from bs4 import BeautifulSoup
import requests

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
    """Scrapea noticias sobre el dólar en Argentina con manejo de errores."""
    try:
        url = "https://www.lanacion.com.ar/economia/dolar/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        noticias = []

        for item in soup.find_all('article', limit=10):
            titulo = item.find('h2')
            enlace = item.find('a')
            if titulo and enlace:
                noticias.append({'titulo': titulo.get_text(strip=True), 'enlace': enlace['href']})

        return noticias if noticias else [{"titulo": "No hay noticias disponibles", "enlace": "#"}]
    except Exception as e:
        return [{"titulo": f"Error al obtener noticias: {e}", "enlace": "#"}]

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

# =========================
# 💵 MOSTRAR PRECIOS CON DISEÑO MEJORADO
# =========================
def mostrar_precios():
    st.title("💵 Precio del dólar Hoy")
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])
    
    if "compra" in datos and "venta" in datos:
        compra, venta = datos["compra"], datos["venta"]
        variacion = datos.get("variacion", 0)
        tendencia = "🔼" if variacion > 0 else "🔽"
        
        st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; font-size: 22px; font-weight: bold;">
                💰 Compra: <span style="color: #28a745;">${compra}</span><br>
                📈 Venta: <span style="color: #dc3545;">${venta}</span><br>
                🔄 Variación: {tendencia} {variacion:.2f}%
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"📅 **Última actualización:** {fecha_actualizacion}<br>📌 **Fuente:** [DolarAPI](https://dolarapi.com)", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ No se pudo obtener el precio del dólar {tipo_dolar}.")

# =========================
# 📰 MOSTRAR NOTICIAS
# =========================
def mostrar_noticias():
    st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")
    noticias = obtener_noticias()
    
    for noticia in noticias:
        st.markdown(f"🔹 [{noticia['titulo']}]({noticia['enlace']})")

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Novedades y Noticias"])

    if menu_seleccionado == "Precios":
        mostrar_precios()
    elif menu_seleccionado == "Novedades y Noticias":
        mostrar_noticias()
