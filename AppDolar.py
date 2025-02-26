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
            fecha = item.find('time')
            fuente = "La Nación"
            if titulo and enlace:
                noticias.append({
                    'titulo': titulo.get_text(strip=True),
                    'enlace': enlace['href'],
                    'fecha': fecha.get_text(strip=True) if fecha else "Fecha no disponible",
                    'fuente': fuente
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
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias"])

    if menu_seleccionado == "Precios":
        mostrar_precios()
    elif menu_seleccionado == "Variación de Cotizaciones":
        mostrar_variacion()
    elif menu_seleccionado == "Convertir":
        convertir_monedas()
    elif menu_seleccionado == "Novedades y Noticias":
        mostrar_noticias()
