from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# INIT FLASK
app = Flask(__name__)

# CONNECT MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flaskcontactapp'
mysql = MySQL(app)

# INIT SESSION - memory app
app.secret_key = 'mi_llave_secreta'


# CALLBACKS
@app.before_request
def defore_request():
    print('Antes de la peticion ...')


@app.after_request
def after_request(response):
    print('Despues de la peticion ...')
    return response

"""

# DEFINIR RUTAS

@app.route('/')

or

app.add_url_rule('/',view_func=index)


# EJEMPLOS DE RUTAS


@app.route('/holaMundo')
def hola_mundo():
    return 'holaMundo'


# Uso de un parametro al crear la ruta -- Contenido dinamico

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return 'Hola, {0}!'.format(nombre)


@app.route('/suma/<int:valor1>/<int:valor2>')
def suma(valor1,valor2):
    return 'La suma es: {0}'.format(valor1+valor2)


@app.route('/perfil/<nombre>/<int:edad>')
def perfil(nombre,edad):
    return 'Hola {0} tu edad es: {1}'.format(nombre,edad)



# Obtener un valor usando Query String
metodos >>> GET
            POST
            PUT
            DELETE

@app.route('/datos')
def datos():
    # ejm request >>> /datos?valor1=Python
    # ejm request >>> /datos?valor1=Python&valor2=20
    # print(request.args)
    valor1 = request.args.get('valor1')
    valor2 = int(request.args.get('valor2'))
    return 'Estos son los datos: {0}, {1}'.format(valor1,(valor2+200))

"""


@app.route('/')
def index():
    print('Estamos accediendo a Index... ')
    data = {
        'title': 'Pagina principal',
        'header':'Bienvenido(a)'
    }
    return render_template('index.html', data=data)


@app.route('/contact')
def contact():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('contact.html', contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        print(fullname,phone,email)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES(%s, %s, %s)', 
                    (fullname, phone, email))
        mysql.connection.commit()

        flash('Contact added successfully')

        #redirecciona a una ruta determinada, usando el nombre de la funcion
        return redirect(url_for('contact'))


@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id = {id}')
    data = cur.fetchall()
    print(data[0])

    return render_template('edit_contact.html', contact = data[0])


@app.route('/update_contact/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE contacts
                    SET fullname = %s,
                        email = %s,
                        phone = %s
                    WHERE id = %s
                    """, (fullname,email,phone,id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('contact'))


@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id}')
    mysql.connection.commit()
    flash('Contact removed successfully')

    return redirect(url_for('contact'))


@app.route('/lenguajes')
def lenguages():
    data={
        'hay_lenguajes':True,
        'lenguajes':['PHP','Python','JavaScript']
    }
    return render_template('lenguajes.html',data=data)


# RUN APP
if __name__ == '__main__':
    app.run(debug=True, port=5000)
