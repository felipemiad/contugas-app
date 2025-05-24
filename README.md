# Contugas App

Aplicación web para detección de anomalías en consumo de clientes usando Isolation Forest y Streamlit, empaquetada en Docker y desplegada en azure en el siguiente link https://contugas-app.wittyplant-faffb88c.eastus.azurecontainerapps.io/.

---

## Descripción

Este repositorio contiene:

* `app.py`: interfaz web construida en Streamlit para cargar datos y visualizar resultados.
* `empaquetadoModelos.py`: script que entrena, empaqueta y guarda modelos de Isolation Forest por cliente.
* `modelos/`: carpeta donde se almacenan los pickles de los modelos entrenados.
* `Dockerfile`: configuración para construir la imagen Docker de la aplicación.
* `requirements.txt`: dependencias de Python.

Los profesores pueden levantar la aplicación localmente usando Docker o directamente con Python.

---

## Requisitos

* [Docker](https://www.docker.com/) instalado y en ejecución.
* (Opcional) Python 3.8+ para ejecución sin contenedor.

---

## Ejecución con Docker

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/felipemiad/contugas-app.git
   cd contugas-app
   ```

2. **Construir la imagen**

   ```bash
   docker build -t contugas-app .
   ```

3. **Ejecutar el contenedor**

   ```bash
   docker run -d --name contugas-app -p 8501:8501 contugas-app
   ```

4. **Abrir la aplicación**

   * Navegar a `http://localhost:8501` en tu navegador.

5. **Detener y eliminar (opcional)**

   ```bash
   docker stop contugas-app && docker rm contugas-app
   ```

---

## Ejecución local (sin Docker)

1. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

2. **Entrenar o cargar modelos**

   ```bash
   python empaquetadoModelos.py
   ```

3. **Iniciar la aplicación Streamlit**

   ```bash
   streamlit run app.py
   ```

4. **Abrir la aplicación**

   * Navegar a `http://localhost:8501`.

---

## Estructura de carpetas

```
contugas-app/
├── Dockerfile
├── app.py
├── empaquetadoModelos.py
├── modelos/       # Modelos pickle generados
├── requirements.txt
└── README.md
```

---

## Soporte

Para dudas o problemas, contactar a Felipe (*[felipemiad@gmail.com](mailto:jf.cortesc1@uniandes.edu.co)*).
