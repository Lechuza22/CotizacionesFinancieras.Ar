import streamlit as st
import http.client
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configurar título de la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵")

# Archivo donde guardamos el historial
HISTORIAL_FILE = "historial_dolar.csv"

# Función para obtener el precio del dólar desde la API
def obtener_precio_dolar(tipo):
    conn = http.client.HTTPSConnection("dolarapi.com")
    conn.request("GET", f"/v1/dolares/{tipo}")
    res = conn.getresponse()
    data = res.read()
    conn.close()
    
    return json.loads(data.decode("utf-8"))

# Función para guardar el historial de precios en un CSV
def guardar_historial(tipo, compra, venta):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[now, tipo, compra, venta]], columns=["Fecha", "Tipo", "Compra", "Venta"])

    try:
        # Cargar historial previo si existe
        historial = pd.read_csv(HISTORIAL_FILE)
        historial = pd.concat([historial, new_data], ignore_index=True)
    except FileNotFoundError:
        # Si el archivo no existe, crearlo con los nuevos datos
        historial = new_data
    
    # Guardar de nuevo el historial
    historial.to_csv(HISTORIAL_FILE, index=False)

# Función para leer el historial guardado
def leer_historial(tipo):
    try:
        historial = pd.read_csv(HISTORIAL_FILE)
        return historial[historial["Tipo"] == tipo]
    except FileNotFoundError:
        return None

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

        # Guardar los datos en el historial
        guardar_historial(tipo_dolar, datos['compra'], datos['venta'])
    
    else:
        st.warning("⚠️ No se pudieron obtener los datos del dólar.")

# Mostrar el historial en un gráfico
historial_data = leer_historial(tipo_dolar)
if historial_data is not None and not historial_data.empty:
    st.subheader(f"📊 Evolución del dólar {tipo_dolar}")

    # Convertir la columna de fecha a tipo datetime
    historial_data["Fecha"] = pd.to_datetime(historial_data["Fecha"])
    
    # Graficar la evolución del dólar
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(historial_data["Fecha"], historial_data["Compra"], label="Compra", color="green", marker="o")
    ax.plot(historial_data["Fecha"], historial_data["Venta"], label="Venta", color="red", marker="o")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio ($)")
    ax.set_title(f"Evolución del dólar {tipo_dolar}")
    ax.legend()
    ax.grid(True)
    
    # Mostrar gráfico en Streamlit
    st.pyplot(fig)
else:
    st.info("📉 No hay datos históricos para mostrar. Consulta el precio para comenzar a registrar datos.")

