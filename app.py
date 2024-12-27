import os
import shutil
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request
from threading import Timer

app = Flask(__name__)

# Función para obtener la fecha de creación del archivo
def obtener_fecha_creacion(archivo):
    timestamp = os.path.getctime(archivo)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

# Función para mover el archivo a la carpeta correspondiente
def mover_archivo(archivo, destino):
    if not os.path.exists(destino):
        os.makedirs(destino)
    shutil.move(archivo, destino)

# Función para organizar los archivos
def organizar_archivos(ruta_archivos, ruta_salida):
    archivos_movidos = []
    for archivo in os.listdir(ruta_archivos):
        ruta_archivo = os.path.join(ruta_archivos, archivo)

        # Asegurarse de que solo se procesen archivos reales
        if os.path.isfile(ruta_archivo):
            # Obtener la fecha de creación del archivo
            fecha_creacion = obtener_fecha_creacion(ruta_archivo)
            destino = os.path.join(ruta_salida, fecha_creacion)
            
            # Mover el archivo
            mover_archivo(ruta_archivo, destino)
            archivos_movidos.append(archivo)
        else:
            print(f"Advertencia: '{archivo}' no es un archivo, se omitirá.")
    
    return archivos_movidos

# Función para abrir automáticamente el navegador
def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")  # Dirección donde se ejecuta tu Flask

# Ruta principal que renderiza el formulario
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ruta_archivos = request.form["ruta_archivos"]
        ruta_salida = request.form["ruta_salida"]
        
        try:
            archivos_movidos = organizar_archivos(ruta_archivos, ruta_salida)
            return render_template("index.html", archivos_movidos=archivos_movidos, error=None)
        except Exception as e:
            return render_template("index.html", archivos_movidos=None, error=str(e))
    
    return render_template("index.html", archivos_movidos=None, error=None)

if __name__ == "__main__":
    Timer(1, abrir_navegador).start()  # Abre el navegador después de 1 segundo
    app.run(debug=True)
