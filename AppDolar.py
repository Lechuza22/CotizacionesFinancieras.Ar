import streamlit as st
import http.client
import json
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵")

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
# 🚀 OPCIÓN: MOSTRAR PRECIOS
# =========================
if menu_seleccionado == "Precios":
    st.title("💵 Precios del dólar Hoy")

    precios = {}
    
    for nombre, tipo in tipos_dolar.items():
        datos = obtener_precio_dolar(tipo)
        if "venta" in datos:
            precios[nombre] = datos["venta"]
            st.write(f"**{nombre}:** ${datos['venta']}")
        else:
            precios[nombre] = None
            st.write(f"**{nombre}:** ❌ No disponible")

# =========================
# 📊 OPCIÓN: VARIACIÓN RESPECTO AL OFICIAL
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
        )

        fig.update_traces(textposition="middle right")
        fig.update_layout(xaxis_title="Precio en $", yaxis_title="Tipo de Dólar")

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudo obtener el precio del Dólar Oficial, por lo que no se puede calcular la variación.")

