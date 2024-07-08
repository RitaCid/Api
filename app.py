from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import mysql.connector

app = Flask(__name__)

# Parámetros de la base de datos
class Base_de_datos():
    def __init__(self):
        # Configura la conexión
        self.conexion = mysql.connector.connect(
            #host="189.197.187.187",
            #user="alumnos",
            #password="Alumnos1010$",
            #database="controlescolar"
            
            #La base de datos el atributo id esto como autoincrementable
            host="localhost",
            user="root",
            password="",
            database="controlescolar"
        )

    def test_db(self):
        # Prueba la conexión a la base de datos
        if self.conexion.is_connected():
            print("Conexión exitosa a la base de datos")

            # Ejecutar consultas
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM profesores")

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)

            # Cerrar el cursor y la conexión al terminar
            #cursor.close()
            #self.conexion.close()
        else:
            print("Error al conectar a la base de datos")

    def obtener_profesores(self):
        profesores = []
        try:
            if self.conexion.is_connected():
                cursor = self.conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM profesores")
                profesores = cursor.fetchall()
                #cursor.close()
        except mysql.connector.Error as error:
            print("Error al obtener datos de la base de datos:", error)
        finally:
            if self.conexion.is_connected():
                None
                #self.conexion.close()
        return profesores

    def borrar_profesor(self, id):
        #print(23456)
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM profesores WHERE id = %s", (id,))
        self.conexion.commit()
        #print(f"Profesor con id {id} eliminado.")
        #cursor.close()
        #self.conexion.close()
        """
        try:
            if self.conexion.is_connected():
                cursor = self.conexion.cursor()
                cursor.execute("DELETE FROM profesores WHERE id = %s", (id,))
                self.conexion.commit()
                print(f"Profesor con id {id} eliminado.")
                cursor.close()
        except mysql.connector.Error as error:
            print("Error al borrar datos de la base de datos:", error)
        finally:
            if self.conexion.is_connected():
                self.conexion.close()
        """

    def regitrar_profesor(self, nombre, correo, direccion):
        cursor = self.conexion.cursor()
        cursor.execute("INSERT INTO profesores (id, nombre, correo, direccion) VALUES ('',%s, %s, %s)", (nombre,correo,direccion,))
        self.conexion.commit()
        #print(f"Profesor se registro exitosamente")

    def consulta_edicion_profesor(self, id):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM profesores WHERE id = %s", (id,))
        profesores = cursor.fetchall()
        return profesores
    
    def consulta_obtener_profesores(self,tipo,caracteres):
        cursor = self.conexion.cursor(dictionary=True)
        if tipo =="va":
            query = "SELECT * FROM profesores WHERE id LIKE %s"
            cursor.execute(query, ("%" + caracteres + "%",))
        else:
            query = "SELECT * FROM profesores WHERE {} LIKE %s".format(tipo)
            cursor.execute(query, ("%" + caracteres + "%",))
            #cursor.execute("SELECT * FROM profesores WHERE %s LIKE %s",(tipo,caracteres))
        profesores = cursor.fetchall()
        return profesores

    def modificar_edicion_profesor(self, id,nombre,correo,direccion):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE profesores SET nombre = %s, correo = %s, direccion = %s WHERE id = %s", (nombre,correo,direccion,id,))
        self.conexion.commit()
        
           
try:
    # Instancia de la clase de conexión a la base de datos
    db_instance = Base_de_datos()
except:
    print("Error 500")

#Paginas proyectadas
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        return "<h1>Error 500</h1>"
    
@app.route('/register')
def register():
    try:
        return render_template("register.html")
    except:
        return "<h1>Error 500</h1>"

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    try:
        id = request.form['id']
        #print(id)
        profesores = db_instance.consulta_edicion_profesor(id)
        #print(profesores)
        #print(profesores[0]['id'])
        return render_template("modify.html", profesor=profesores)
    except:
        return "<h1>Error 500</h1>"

@app.route('/get_all')
def get_all():
    try:
        profesores = db_instance.obtener_profesores()
        return render_template("consult.html", profesores=profesores)
    except:
        return "<h1>Error 500</h1>"

@app.route('/consult',methods=['GET', 'POST'])
def consult():
    try:
        tipo = request.form['type']
        caracteres = request.form['busqueda']
        profesores = db_instance.consulta_obtener_profesores(tipo,caracteres)
        #print (profesores)
        #return "fddfghdf"
        return render_template("consult.html", profesores=profesores)
    except:
        return "<h1>Error 500</h1>"

#Paginas con procesos pero no se ven
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    try:    
        if request.method == 'POST':
            id = request.form['id']
            db_instance.borrar_profesor(id)
            #print(id)
            return redirect(url_for('get_all'))
            #return render_template("index.html")
            #return redirect(url_for('/get_all'))
        return "<h1>Error 400</h1>"
    except:
        return "<h1>Error 500</h1>"

@app.route('/funcion_registrar', methods=['GET', 'POST'])
def proceso_registrar():
    try:    
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            direccion = request.form['direccion']
            db_instance.regitrar_profesor(nombre,correo,direccion)
            return redirect(url_for('get_all'))
        return render_template("delete.html")
    except:
        return "<h1>Error 500</h1>"

@app.route('/modify_action', methods=['GET', 'POST'])
def modificar_profesor():
    try:    
        if request.method == 'POST':
            id = request.form['id']
            nombre = request.form['nombre']
            correo = request.form['correo']
            direccion = request.form['direccion']
            #print(id)
            #print(nombre)
            #print(correo)
            #print(direccion)
            db_instance.modificar_edicion_profesor(id,nombre,correo,direccion)
            return redirect(url_for('get_all'))
        return "<h1>Error 400</h1>"
    except:
        return "<h1>Error 500</h1>"

#Ruta css
@app.route('/templates/css/<path:filename>')
def custom_static(filename):
    try:    
        return send_from_directory('templates/css', filename)
    except:
        return "<h1>Error 500</h1>"

#Ruta imagenes
# Ruta para servir imágenes desde templates/imagenes
@app.route('/templates/imagenes/<path:filename>')
def custom_static_imagenes(filename):
    try:    
        return send_from_directory('templates/imagenes', filename)
    except:
        return "<h1>Error 500</h1>"

if __name__ == '__main__':
    app.run(debug=True)




