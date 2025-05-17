import streamlit as st
import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
from io import BytesIO

st.set_page_config(page_title="Contugas - Análisis de Anomalías", layout="wide")
st.title("Detección de Anomalías - Contugas")

# Menú de navegación
modo = st.radio("Selecciona el modo de uso:", ["📄 Subir archivo", "✍️ Ingreso manual"])

def cargar_modelo(cliente_id):
    try:
        with open(f"modelos/{cliente_id}.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# MODO 1: SUBIR ARCHIVO
if modo == "📄 Subir archivo":
    archivo = st.file_uploader("Sube archivo Excel o CSV con columnas: Cliente, Fecha, Volumen, Temperatura, Presion", type=["xlsx", "csv"])

    if archivo:
        try:
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
            else:
                df = pd.read_excel(archivo)

            columnas_esperadas = {"Cliente", "Fecha", "Volumen", "Temperatura", "Presion"}
            if not columnas_esperadas.issubset(df.columns):
                st.error(f"❌ El archivo debe tener las columnas: {', '.join(columnas_esperadas)}")
            else:
                resultados = []
                clientes = df["Cliente"].unique()
                st.info(f"🔎 Analizando {len(clientes)} clientes...")

                for cliente_id in clientes:
                    df_cliente = df[df["Cliente"] == cliente_id].copy()
                    modelo = cargar_modelo(cliente_id)

                    if modelo:
                        datos = df_cliente[["Volumen", "Temperatura", "Presion"]]
                        df_cliente["Resultado"] = modelo.predict(datos)
                        df_cliente["Anomalía"] = df_cliente["Resultado"].apply(lambda x: "⚠️ Atípico" if x == -1 else "✅ Normal")
                    else:
                        df_cliente["Resultado"] = "Sin modelo"
                        df_cliente["Anomalía"] = "🚫 Cliente no entrenado"

                    resultados.append(df_cliente)

                df_resultado = pd.concat(resultados, ignore_index=True)
                st.success("✅ Análisis completado.")
                st.dataframe(df_resultado)

                def descargar_excel(df):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name="Resultados")
                        writer.save()
                    return output.getvalue()

                excel_bytes = descargar_excel(df_resultado)
                st.download_button(
                    label="⬇️ Descargar resultados en Excel",
                    data=excel_bytes,
                    file_name="resultados_anomalias.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"🚨 Error al procesar el archivo: {e}")

# MODO 2: INGRESO MANUAL
else:
    with st.form("formulario_manual"):
        cliente = st.text_input("ID del Cliente (ej. EMP001)")
        fecha = st.date_input("Fecha de la medición")
        volumen = st.number_input("Volumen", min_value=0.0, step=0.1)
        temperatura = st.number_input("Temperatura", step=0.1)
        presion = st.number_input("Presión", step=0.1)
        enviar = st.form_submit_button("🔍 Analizar registro")

    if enviar:
        modelo = cargar_modelo(cliente)

        if modelo:
            try:
                entrada = pd.DataFrame([{
                    "Volumen": volumen,
                    "Temperatura": temperatura,
                    "Presion": presion
                }])

                resultado = modelo.predict(entrada)[0]
                etiqueta = "✅ Normal" if resultado == 1 else "⚠️ Atípico"

                st.success(f"Resultado para el cliente **{cliente}**:")
                st.markdown(f"📅 Fecha: `{fecha}`  \n📊 Resultado: **{etiqueta}**")

            except Exception as e:
                st.error(f"Error al ejecutar el modelo: {e}")
        else:
            st.warning(f"🚫 Cliente `{cliente}` no tiene un modelo entrenado.")
