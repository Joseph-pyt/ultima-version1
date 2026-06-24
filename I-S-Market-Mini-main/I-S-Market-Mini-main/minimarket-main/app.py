from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def inicio():
    productos = []
    try:
        with open(os.path.join(BASE_DIR, "productos.txt"), "r") as archivo:
            for linea in archivo:
                nombre, precio = linea.strip().split(",")
                productos.append({"nombre": nombre, "precio": precio})
    except:
        pass
    return render_template("index.html", productos=productos)

@app.route("/dashboard")
def dashboard():

    productos = []
    usuarios = []

    try:
        with open(os.path.join(BASE_DIR, "productos.txt"), "r") as archivo:
            for linea in archivo:
                nombre, precio = linea.strip().split(",")

                productos.append({
                    "nombre": nombre,
                    "precio": precio
                })
    except:
        pass

    try:
        with open(os.path.join(BASE_DIR, "usuarios.txt"), "r") as archivo:
            for linea in archivo:
                correo, password = linea.strip().split(",")

                usuarios.append({
                    "correo": correo
                })
    except:
        pass

    return render_template(
        "dashboard.html",
        productos=productos,
        usuarios=usuarios
    )
@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    with open(os.path.join(BASE_DIR, "usuarios.txt"), "r") as archivo:
        for linea in archivo:
            u, p = linea.strip().split(",")

            if usuario == u and password == p:
                return redirect("/dashboard")

    return """
<script>
    alert('Usuario o contraseña incorrectos');
    history.back();
</script>
"""

@app.route("/registro", methods=["POST"])
def registro():

    correo = request.form["correo"]
    password = request.form["password"]

    with open(os.path.join(BASE_DIR, "usuarios.txt"), "a") as archivo:
        archivo.write(f"{correo},{password}\n")

    return redirect("/")

@app.route("/agregar_producto", methods=["POST"])
def agregar_producto():

    nombre = request.form["nombre"]
    precio = request.form["precio"]

    with open(os.path.join(BASE_DIR, "productos.txt"), "a") as archivo:
        archivo.write(f"{nombre},{precio}\n")

    return redirect("/dashboard")

@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):

    with open(os.path.join(BASE_DIR, "productos.txt"), "r") as archivo:
        lineas = archivo.readlines()

    lineas.pop(id)

    with open(os.path.join(BASE_DIR, "productos.txt"), "w") as archivo:
        archivo.writelines(lineas)

    return redirect("/dashboard")
@app.route("/eliminar_usuario/<int:id>")
def eliminar_usuario(id):

    with open(os.path.join(BASE_DIR, "usuarios.txt"), "r") as archivo:
        lineas = archivo.readlines()

    lineas.pop(id)

    with open(os.path.join(BASE_DIR, "usuarios.txt"), "w") as archivo:
        archivo.writelines(lineas)

    return redirect("/dashboard")

@app.route("/actualizar_producto/<int:id>", methods=["POST"])
def actualizar_producto(id):

    nombre = request.form["nombre"]
    precio = request.form["precio"]

    with open(os.path.join(BASE_DIR, "productos.txt"), "r") as archivo:
        lineas = archivo.readlines()

    lineas[id] = f"{nombre},{precio}\n"

    with open(os.path.join(BASE_DIR, "productos.txt"), "w") as archivo:
        archivo.writelines(lineas)

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)