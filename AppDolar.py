import streamlit as st
import requests

def obtener_dolar(tipo):
    url = f"https://dolarapi.com/v1/dolares/{tipo}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Configurar el icono y el título de la pestaña
st.set_page_config(page_title="Dólar Argentina", page_icon="💲")

st.title("Dólar en Argentina 🇦🇷")

def mostrar_dolar(tipo, nombre):
    st.subheader(f"Dólar {nombre} 💰")
    precio = obtener_dolar(tipo)
    if precio and "compra" in precio and "venta" in precio:
        compra = precio["compra"]
        venta = precio["venta"]
        
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
        st.error(f"No se pudieron obtener datos para el dólar {nombre}.")

# Crear botones para cada tipo de dólar
if st.button("Dólar Oficial 💰"):
    mostrar_dolar("oficial", "Oficial")

if st.button("Dólar Blue 💰"):
    mostrar_dolar("blue", "Blue")

if st.button("Dólar CCL 💰"):
    mostrar_dolar("contadoconliqui", "CCL")

if st.button("Dólar Tarjeta 💳"):
    mostrar_dolar("tarjeta", "Tarjeta")

if st.button("Dólar Cripto 🪙"):
    mostrar_dolar("cripto", "Cripto")

st.caption("Fuente: DolarAPI")

