from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from wtforms import validators

app = Flask(__name__)
# conector a base de datos mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tienda_ssmk'
mysql = MySQL(app)

# configuraciones
app.secret_key = 'mysecretkey'

# route


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', clientes=data)


# agrega los usuarios a la tabla de clientes en la base de datos
@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        movil = request.form['movil']
        saldo = request.form['saldo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (nombre,movil,saldo) VALUES (%s, %s, %s)',
                    (nombre, movil, saldo))
        mysql.connection.commit()
        flash('Usuario agregado satisfactoriamente')

        return redirect(url_for('Index'))


# selecciona el usuario en la posicion para luego hacer la accion de actualizacion
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-clientes.html', clientes=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        movil = request.form['movil']
        saldo = request.form['saldo']
        print('*************************************')
        print(saldo)
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre = %s,
                movil = %s,
                saldo = %s
            WHERE id = %s
        """, (nombre, movil, saldo, id))
        flash('Usuario actualizado satisfactoriamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))


# se elimina directamente el usuario al darle click en el enlace delete, se elimina de la base de datos


@app.route('/delete/<string:id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario elminado satisfactoriamente')
    return redirect(url_for('Index'))

# Se busca un usuario con el parametro nombre

@app.route('/busqueda',methods=['POST'])
def busqueda_usuarios():
    return render_template('busqueda.html')

@app.route('/buscar', methods=['POST'])
def buscar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        msj = f"select * from clientes where nombre='{nombre}'"
        cur = mysql.connection.cursor()
        cur.execute(msj)
        datos = cur.fetchall()
        flash(f'El usuario encontrado es {nombre}')

        return render_template('busqueda.html', clientes=datos)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
