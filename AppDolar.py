import streamlit as st
import http.client
import json

# Configurar título de la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵")

# Título de la app
st.title("💵 Precio del dólar Hoy")

# Función para obtener el precio del dólar
def obtener_precio_dolar(tipo):
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", f"/v1/dolares/{tipo}")
    res = conn.getresponse()
    data = res.read()
    conn.close()
    
    return json.loads(data.decode("utf-8"))

# Diccionario de tipos de dólar y sus valores en la API
tipos_dolar = {
    "Blue": "blue",
    "Oficial": "oficial",
    "Tarjeta": "tarjeta",
    "Cripto": "cripto",
    "Contado con Liqui (CCL)": "contadoconliqui",
    "Bolsa (MEP)": "bolsa"
}

# Selección del tipo de dólar
tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))

if st.button("Consultar precio"):
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        st.success(f"💰 **Compra:** ${datos['compra']}")
        st.error(f"📈 **Venta:** ${datos['venta']}")
    else:
        st.warning("⚠️ No se pudieron obtener los datos del dólar.")

