# Instalar dependencias (si no están)
!pip install -q scikit-learn pandas openpyxl

import pandas as pd
nombre_archivo = "consumo_clientes_demo_con_fecha_hora.xlsx"
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

# Paso 6: para fines practicos el modelo anterior sencillo fue el que se llevo a producción y despliegue sin embargo el modelo usado en productivo fue este:
# import pandas as pd
# from sklearn.ensemble import IsolationForest

# 1. Leer todas las hojas y concatenarlas en un solo DataFrame
# file_path = 'DatosContugas.xlsx'
# sheets = pd.read_excel(file_path, sheet_name=None)
# for nombre, df in sheets.items():
#     df['Cliente'] = nombre
# df_all = pd.concat(sheets.values(), ignore_index=True)

# 2. Función para detectar outliers univariantes (IQR)
# def detectar_outliers(df, col):
#     Q1 = df[col].quantile(0.25)
#     Q3 = df[col].quantile(0.75)
#     IQR = Q3 - Q1
#     return df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]

# variables = ['Presion', 'Temperatura', 'Volumen']

# 3. Calcular proporción de outliers univariantes por cliente
# resultados = []
# for cliente, df_cli in df_all.groupby('Cliente'):
#     total = len(df_cli)
#     fila = {'Cliente': cliente}
#     for var in variables:
#         cnt = len(detectar_outliers(df_cli, var))
#         pct = max(cnt / total, 0.001)  # mínimo 0.1%
#         fila[f'proporcion_{var}'] = pct
#     resultados.append(fila)

# df_resultados = pd.DataFrame(resultados)

# 4. Calcular contamination multivariante (promedio de proporciones)
# df_resultados['contamination'] = (
#     df_resultados[[f'proporcion_{v}' for v in variables]]
#     .mean(axis=1)
# )

# 5. Construir dict cliente → contamination
# contamination_dict = dict(zip(
#     df_resultados['Cliente'],
#     df_resultados['contamination']
# ))

# 6. Aplicar Isolation Forest multivariante por cliente
# out_rows = []
# for cliente, df_cli in df_all.groupby('Cliente'):
#     X = df_cli[variables]
#     cont = contamination_dict[cliente]
#     iso = IsolationForest(contamination=cont, random_state=42)
#     iso.fit(X)
#     df_tmp = df_cli.copy()
#     df_tmp['anomaly'] = iso.predict(X)                #  1 = normal, -1 = anomalía
#     df_tmp['is_anomalo'] = df_tmp['anomaly'] == -1
#     # Columna legible
#     df_tmp['Estado_Anomalia'] = df_tmp['is_anomalo'].map({
#         True: 'Anómalo', False: 'No anómalo'
#     })
#     out_rows.append(df_tmp)

# df_final = pd.concat(out_rows, ignore_index=True)

# 7. Ejemplo: ver las primeras filas con el nuevo campo
# print(df_final[['Cliente', *variables, 'Estado_Anomalia']].tail())

# Contar anomalías por cliente
# df_counts = (
#     df_final
#     .groupby('Cliente')['is_anomalo']
#     .sum()
#     .reset_index(name='Cantidad_Anomalias')
# )

# print(df_counts)

# Total de observaciones por cliente
# totales = (
#     df_final
#     .groupby('Cliente')
#     .size()
#     .reset_index(name='Total_Obs')
# )

# Unir totales y conteo de anomalías
# df_counts = df_counts.merge(totales, on='Cliente')
# df_counts['Proporción (%)'] = (df_counts['Cantidad_Anomalias'] / df_counts['Total_Obs'] * 100).round(2)

# print(df_counts)
