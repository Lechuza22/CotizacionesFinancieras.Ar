import streamlit as st
import pandas as pd
import http.client
import json

def obtener_precio_blue():
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", "/v1/dolares/blue")
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Configurar el icono y el título de la pestaña
st.set_page_config(page_title="Dólar Argentina", page_icon="💲")

st.title("Dólar en Argentina 🇦🇷")

st.subheader("Precio del Dólar Blue Hoy 💰")
precio_blue = obtener_precio_blue()
if precio_blue:
    compra = precio_blue.get("compra", "No disponible")
    venta = precio_blue.get("venta", "No disponible")
    
    st.markdown(
        f"""
        <div style='background-color:#4CAF50; padding:10px; border-radius:5px; color:white; font-size:18px; text-align:center;'>
            <strong>Compra:</strong> {compra} ARS
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style='background-color:#F44336; padding:10px; border-radius:5px; color:white; font-size:18px; text-align:center;'>
            <strong>Venta:</strong> {venta} ARS
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("No se pudieron obtener datos del dólar blue.")

st.caption("Fuente: DolarAPI")
