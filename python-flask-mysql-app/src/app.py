from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM crudflaskkk")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def addUser():
    correo = request.form['correo']
    nombre = request.form['nombre']
    password = request.form['password']

    if correo and nombre and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO crudflaskkk (correo, nombre, password) VALUES (%s, %s, %s)"
        data = (correo, nombre, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:idcrud>')
def delete(idcrud):
    cursor = db.database.cursor()
    sql = "DELETE FROM crudflaskkk WHERE idcrud=%s"
    data = (idcrud,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:idcrud>', methods=['POST'])
def edit(idcrud):
    correo = request.form['correo']
    nombre = request.form['nombre']
    password = request.form['password']

    if correo and nombre and password:
        cursor = db.database.cursor()
        sql = "UPDATE crudflaskkk SET correo = %s, nombre = %s, password = %s WHERE idcrud = %s"
        data = (correo, nombre, password, idcrud)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)