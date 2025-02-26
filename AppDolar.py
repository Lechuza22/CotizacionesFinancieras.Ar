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

# Botones para seleccionar el tipo de dólar
tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", ["Blue", "Oficial"])

# Mapeo de tipos de dólar a los valores de la API
tipo_dolar_api = {"Blue": "blue", "Oficial": "oficial"}

if st.button("Consultar precio"):
    datos = obtener_precio_dolar(tipo_dolar_api[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        st.success(f"💰 **Compra:** ${datos['compra']}")
        st.error(f"📈 **Venta:** ${datos['venta']}")
    else:
        st.warning("⚠️ No se pudieron obtener los datos del dólar.")

