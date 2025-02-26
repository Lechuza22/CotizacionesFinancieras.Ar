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

st.title("Dólar en Argentina 🇦🇷")

menu = st.sidebar.selectbox("Menú", ["Precio Blue Hoy"])

if menu == "Precio Blue Hoy":
    st.subheader("Precio del Dólar Blue Hoy 💰")
    precio_blue = obtener_precio_blue()
    if precio_blue:
        compra = precio_blue.get("compra", "No disponible")
        venta = precio_blue.get("venta", "No disponible")
        st.write(f"**Compra:** {compra} ARS")
        st.write(f"**Venta:** {venta} ARS")
    else:
        st.error("No se pudieron obtener datos del dólar blue.")

st.caption("Fuente: DolarAPI")
