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

# Función para obtener los precios de los diferentes tipos de dólar
def obtener_precio_dolar(tipo):
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", f"/v1/dolares/{tipo}")
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data.decode("utf-8"))

# Función para obtener las noticias más recientes sobre el dólar en Argentina
def obtener_noticias():
    url = "https://www.lanacion.com.ar/economia/dolar/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for item in soup.find_all('article', limit=10):
        titulo = item.find('h2').get_text(strip=True)
        descripcion = item.find('p').get_text(strip=True) if item.find('p') else "Sin descripción disponible."
        enlace = item.find('a')['href']
        noticias.append({'titulo': titulo, 'descripcion': descripcion, 'enlace': enlace})
    return noticias

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

# Sidebar con opciones
st.sidebar.title("📌 Menú")
menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias"])

# =========================
# 🚀 OPCIÓN: MOSTRAR PRECIOS (CON SELECCIÓN DE TIPO, FECHA Y COLORES)
# =========================
if menu_seleccionado == "Precios":
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

        fig.update_traces(textposition="middle right")
        fig.update_layout(
            xaxis_title="Precio en $", 
            yaxis_title="Tipo de Dólar",
            annotations=[
                dict(
                    text=f"📅 Última actualización: {fecha_actualizacion}<br>📌 Fuente: <a href='https://dolarapi.com' target='_blank'>DolarAPI</a>",
                    xref="paper", yref="paper",
                    x=0.95, y=-0.2, 
                    showarrow=False,
                    font=dict(size=12, color="gray")
                )
            ]
        )

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudo obtener el precio del Dólar Oficial, por lo que no se puede calcular la variación.")

# =========================
# 🔄 OPCIÓN: CONVERTIR PESOS ↔ DÓLARES
# =========================
elif menu_seleccionado == "Convertir":
    st.title("💱 Convertidor de Moneda")

    # Selección del tipo de dólar para la conversión
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))

    # Obtener el precio del tipo de dólar seleccionado
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        compra = datos["compra"]
        venta = datos["venta"]

        # Entrada del usuario
        monto = st.number_input("Ingrese el monto a convertir:", min_value=0.0, format="%.2f")

        # Sele
::contentReference[oaicite:0]{index=0}
 
