from flask import Flask, render_template, request, redirect, url_for, flash
from conn import conn
from flask_mysqldb import MySQL


# INIT FLASK
app = Flask(__name__)

# CONNECT MYSQL
conn(app)
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
    data = {
        'title': 'Contactos',
        'header':'Contactos'
    }
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data_contacts = cur.fetchall()
    print(data_contacts)
    return render_template('contact.html', data = data, contacts = data_contacts)


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
    data = {
        'title': 'Contacto',
        'header':'Editar contacto'
    }
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data_contact = cur.fetchall()

    return render_template('edit_contact.html', data = data, contact = data_contact[0])


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



# RUN APP
if __name__ == '__main__':
    app.run(debug=True, port=5000)
