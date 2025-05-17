# Paso 1: Instalar dependencias (si no están)
!pip install -q scikit-learn pandas openpyxl

# Paso 2: Si ya subiste el archivo desde la pestaña lateral de archivos (o Drive), lee con pandas
import pandas as pd

# Cambia este nombre si subiste un archivo distinto
nombre_archivo = "consumo_clientes_demo_con_fecha_hora.xlsx"

# Leer Excel
df = pd.read_excel(nombre_archivo)

# Validar columnas
columnas_requeridas = {"Cliente", "Fecha", "Volumen", "Temperatura", "Presion"}
if not columnas_requeridas.issubset(df.columns):
    raise ValueError(f"El archivo debe tener las columnas: {columnas_requeridas}")

# Paso 3: Entrenar modelos por cliente
from sklearn.ensemble import IsolationForest
import os
import pickle

os.makedirs("modelos", exist_ok=True)
clientes_entrenados = []

for cliente in df["Cliente"].unique():
    df_cliente = df[df["Cliente"] == cliente]
    X = df_cliente[["Volumen", "Temperatura", "Presion"]]
    
    modelo = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    modelo.fit(X)
    
    with open(f"modelos/{cliente}.pkl", "wb") as f:
        pickle.dump(modelo, f)
    
    clientes_entrenados.append(cliente)

print("✅ Modelos entrenados para clientes:", clientes_entrenados)

# Paso 4: Comprimir la carpeta de modelos
import shutil
shutil.make_archive("modelos_entrenados", 'zip', "modelos")

# Paso 5: Descargar el ZIP de modelos
from google.colab import files
files.download("modelos_entrenados.zip")
