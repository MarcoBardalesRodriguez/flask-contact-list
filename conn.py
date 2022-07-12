
def conn(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = 'admin'
    app.config['MYSQL_DB'] = 'flaskcontactapp'