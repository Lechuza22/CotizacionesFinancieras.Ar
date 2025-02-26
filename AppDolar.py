import streamlit as st
import pandas as pd
import http.client
import json
import plotly.express as px

def obtener_dolar(tipo):
    try:
        conn = http.client.HTTPSConnection("dolarapi.com")
        conn.request("GET", f"/v1/dolares/{tipo}")
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        return None

# Configurar el icono y el título de la pestaña
st.set_page_config(page_title="Dólar Argentina", page_icon="💲")

st.title("Dólar en Argentina 🇦🇷")

# Crear menú con botones
def mostrar_precio():
    st.subheader("Precios del Dólar 💰")
    opciones = ["Oficial", "Blue", "CCL", "Tarjeta", "Cripto", "Comparaciones"]
    seleccion = st.selectbox("Seleccione un tipo de dólar:", opciones)
    
    tipo_api = {
        "Oficial": "oficial",
        "Blue": "blue",
        "CCL": "contadoconliqui",
        "Tarjeta": "tarjeta",
        "Cripto": "cripto"
    }
    
    if seleccion != "Comparaciones":
        precio = obtener_dolar(tipo_api.get(seleccion, ""))
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
            st.error(f"No se pudieron obtener datos para el dólar {seleccion}.")
    else:
        st.subheader("Comparación de Precios del Dólar 📊")
        tipos = {"Oficial": "oficial", "Blue": "blue", "CCL": "contadoconliqui", "Tarjeta": "tarjeta", "Cripto": "cripto"}
        datos = []
        for nombre, tipo in tipos.items():
            precio = obtener_dolar(tipo)
            if precio and "compra" in precio and "venta" in precio:
                datos.append({"Tipo": nombre, "Compra": precio["compra"], "Venta": precio["venta"]})
        df = pd.DataFrame(datos)
        
        if not df.empty:
            fig = px.bar(df, x="Tipo", y=["Compra", "Venta"], barmode="group", title="Comparación de Precios del Dólar")
            st.plotly_chart(fig)
        else:
            st.error("No se pudieron obtener datos para la comparación.")

def mostrar_prediccion():
    st.subheader("Predicción del Dólar 📈")
    st.write("Aquí se mostrará la predicción del valor del dólar basada en análisis de datos.")

# Botones de navegación
col1, col2 = st.columns(2)

with col1:
    if st.button("Precio 💰"):
        mostrar_precio()

with col2:
    if st.button("Predicción 📈"):
        mostrar_prediccion()

st.caption("Fuente: DolarAPI")
