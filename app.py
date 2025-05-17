import streamlit as st
import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest

st.title("🔍 Detección de Anomalías de Consumo - Contugas")

# Cargar archivo Excel/CSV
archivo = st.file_uploader("Sube archivo de consumo (Excel o CSV)", type=["xlsx", "csv"])
cliente_id = st.text_input("ID del Cliente (Ej: EMP001)")

if archivo and cliente_id:
    try:
        if archivo.name.endswith(".csv"):
            df = pd.read_csv(archivo)
        else:
            df = pd.read_excel(archivo)

        # Cargar modelo
        try:
            with open(f"modelos/{cliente_id}.pkl", "rb") as f:
                modelo = pickle.load(f)

            # Ejecutar predicción
            pred = modelo.predict(df[["Volumen", "Temperatura", "Presion"]])
            df["Anomalía"] = ["✅ Normal" if p == 1 else "⚠️ Atípico" for p in pred]
            st.success("Modelo ejecutado correctamente.")
            st.dataframe(df)

        except FileNotFoundError:
            st.error(f"🚫 Cliente {cliente_id} no tiene un modelo entrenado.")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
