import streamlit as st
import http.client
import json
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵", layout="wide")

# Función para obtener los precios de los diferentes tipos de dólar
def obtener_precio_dolar(tipo):
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", f"/v1/dolares/{tipo}")
    res = conn.getresponse()
    data = res.read()
    conn.close()
    
    return json.loads(data.decode("utf-8"))

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

# Sidebar con opciones
st.sidebar.title("📌 Menú")
menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones"])

# =========================
# 🚀 OPCIÓN: MOSTRAR PRECIOS (CON TARJETAS COLORIDAS)
# =========================
if menu_seleccionado == "Precios":
    st.title("💵 Precios del dólar Hoy")

    col1, col2, col3 = st.columns(3)
    
    precios = {}

    colores = {
        "Mayorista": "#FF5733",
        "Oficial": "#33FF57",
        "MEP": "#3385FF",
        "CCL": "#FF33E3",
        "Cripto": "#FFC733",
        "Blue": "#33FFF3",
        "Tarjeta": "#FF9033"
    }

    for i, (nombre, tipo) in enumerate(tipos_dolar.items()):
        datos = obtener_precio_dolar(tipo)
        if "venta" in datos:
            precios[nombre] = datos["venta"]
            precio_str = f"💰 **${datos['venta']}**"
        else:
            precios[nombre] = None
            precio_str = "❌ No disponible"

        with (col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3):
            st.markdown(
                f"""
                <div style="
                    background-color: {colores[nombre]};
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: white;
                ">
                    {nombre}<br>{precio_str}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# 📊 OPCIÓN: VARIACIÓN RESPECTO AL OFICIAL (GRÁFICO SIMILAR AL DE LA IMAGEN)
# =========================
elif menu_seleccionado == "Variación de Cotizaciones":
    st.title("📊 Variación de Cotizaciones respecto al Oficial")

    precios = {}

    for nombre, tipo in tipos_dolar.items():
        datos = obtener_precio_dolar(tipo)
        if "venta" in datos:
            precios[nombre] = datos["venta"]
    
    if "Oficial" in precios:
        oficial = precios["Of
