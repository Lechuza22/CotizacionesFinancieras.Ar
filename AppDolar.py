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

# Función para obtener los precios de los diferentes tipos de dólar
def obtener_precio_dolar(tipo):
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", f"/v1/dolares/{tipo}")
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data.decode("utf-8"))

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
                    imagen = item.find('img')['src'] if item.find('img') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": enlace, "imagen": imagen})

            elif "clarin" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    imagen = item.find_parent('a').find('img')['src'] if item.find_parent('a') and item.find_parent('a').find('img') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": "https://www.clarin.com" + enlace, "imagen": imagen})

            elif "infobae" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    imagen = item.find_parent('a').find('img')['src'] if item.find_parent('a') and item.find_parent('a').find('img') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": enlace, "imagen": imagen})

            elif "ambito" in url:
                articles = soup.find_all('h2', limit=3)
                for item in articles:
                    titulo = item.get_text(strip=True)
                    enlace = item.find_parent('a')['href'] if item.find_parent('a') else None
                    imagen = item.find_parent('a').find('img')['src'] if item.find_parent('a') and item.find_parent('a').find('img') else None
                    if titulo and enlace:
                        noticias.append({"fuente": fuente, "titulo": titulo, "enlace": "https://www.ambito.com" + enlace, "imagen": imagen})

        except Exception as e:
            st.warning(f"⚠️ No se pudo obtener noticias de {fuente}. Error: {e}")

    return noticias[:10]  # Limitar a las 10 primeras noticias

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias"])

    if menu_seleccionado == "Precios":
        st.title("💵 Precio del dólar Hoy")

        tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list({
            "Mayorista": "mayorista",
            "Oficial": "oficial",
            "MEP": "bolsa",
            "CCL": "contadoconliqui",
            "Cripto": "cripto",
            "Blue": "blue",
            "Tarjeta": "tarjeta"
        }.keys()))

        datos = obtener_precio_dolar(tipo_dolar)

        if "compra" in datos and "venta" in datos:
            st.success(f"💰 **Compra:** ${datos['compra']}")
            st.error(f"📈 **Venta:** ${datos['venta']}")

    elif menu_seleccionado == "Variación de Cotizaciones":
        st.title("📊 Variación de Cotizaciones respecto al Oficial")

        precios = {nombre: obtener_precio_dolar(tipo)["venta"] for nombre, tipo in {
            "Mayorista": "mayorista",
            "Oficial": "oficial",
            "MEP": "bolsa",
            "CCL": "contadoconliqui",
            "Cripto": "cripto",
            "Blue": "blue",
            "Tarjeta": "tarjeta"
        }.items()}

        if "Oficial" in precios:
            df_variaciones = pd.DataFrame({
                "Tipo de Dólar": list(precios.keys()),
                "Variación %": [(precio / precios["Oficial"] - 1) * 100 for precio in precios.values()],
                "Precio": list(precios.values())
            })

            st.plotly_chart(px.scatter(df_variaciones, x="Precio", y="Tipo de Dólar", size="Precio", color="Variación %"))

    elif menu_seleccionado == "Convertir":
        st.title("💱 Convertidor de Moneda")

        tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list({
            "Mayorista": "mayorista",
            "Oficial": "oficial",
            "MEP": "bolsa",
            "CCL": "contadoconliqui",
            "Cripto": "cripto",
            "Blue": "blue",
            "Tarjeta": "tarjeta"
        }.keys()))

        datos = obtener_precio_dolar(tipo_dolar)

        if "compra" in datos and "venta" in datos:
            monto = st.number_input("Ingrese el monto a convertir:", min_value=0.0, format="%.2f")
            conversion = st.radio("Seleccione el tipo de conversión:", ["Pesos a Dólares", "Dólares a Pesos"])

            if conversion == "Pesos a Dólares":
                st.success(f"💵 {monto} ARS equivale a **{monto / datos['venta']:.2f} USD**")
            else:
                st.success(f"💵 {monto} USD equivale a **{monto * datos['compra']:.2f} ARS**")

    elif menu_seleccionado == "Novedades y Noticias":
        st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")

        for noticia in obtener_noticias():
            st.markdown(f"🔹 [**{noticia['titulo']}**]({noticia['enlace']}) _(Fuente: {noticia['fuente']})_")
