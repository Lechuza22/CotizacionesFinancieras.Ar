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
# 🚀 FUNCIONES PRINCIPALES
# =========================

# Función para obtener las noticias sobre el dólar en Argentina desde varios medios
def obtener_noticias():
    fuentes = {
        "La Nación": "https://www.lanacion.com.ar/economia/dolar/",
        "Clarín": "https://www.clarin.com/tema/dolar.html",
        "Infobae": "https://www.infobae.com/economia/dolar/",
        "Ámbito Financiero": "https://www.ambito.com/contenidos/dolar.html"
    }

    noticias = []

    for fuente, url in fuentes.items():
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')

            if "lanacion" in url:
                articles = soup.find_all('article', limit=3)
                for item in articles:
                    titulo = item.find('h2').get_text(strip=True) if item.find('h2') else None
                    enlace = item.find('a')['href'] if item.find('a') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": enlace})

            elif "clarin" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": "https://www.clarin.com" + enlace})

            elif "infobae" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": enlace})

            elif "ambito" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": "https://www.ambito.com" + enlace})

        except Exception as e:
            st.warning(f"⚠️ No se pudo obtener noticias de {fuente}. Error: {e}")

    return noticias[:10]  # Limitar a las 10 primeras noticias

def mostrar_noticias():
    st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")

    noticias = obtener_noticias()

    if noticias:
        for noticia in noticias:
            st.markdown(f"🔹 **[{noticia['titulo']}]({noticia['enlace']})** _(Fuente: {noticia['fuente']})_")
    else:
        st.warning("⚠️ No se encontraron noticias recientes.")

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias"])

    if menu_seleccionado == "Novedades y Noticias":
        mostrar_noticias()
