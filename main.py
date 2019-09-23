# session para el encrptacion
from flask import Flask, request, make_response, redirect, render_template, session, url_for
#url for funciona directamente en jinja pero no en pyhton, en python tenemso que traerla
from flask_bootstrap import Bootstrap

# login

from flask_wtf import FlaskForm #es la clase que utilizamos para poder renderizar los formularios
from wtforms.fields import StringField, IntegerField, SubmitField
# Validacion dle logion
from wtforms.validators import DataRequired #para decir los requerimientos que recoge el formulario

app = Flask(__name__)
boostrap = Bootstrap(app)


# login
class LoginForm(FlaskForm): # Metemos una clase dentro de una clase, esto tiene un nombre pero no recuerdo cual es
    fecha = StringField('Fecha (dd/mm/yyyy)', validators=[DataRequired()])
    importe = IntegerField('Importe', validators=[DataRequired()])
    enviar = SubmitField('enviar')


algunos = ['este', 'el tro', 'nuevo']

# ENCRIPTAR COOKIE
app.config['SECRET_KEY'] = 'SUPER_SECRETO'


@app.route('/')
def hola_mundo():
    # Robar la ip del usuario. Es una práctica muy habitual, para ponerla en una cookie con request
    respuesta = make_response(redirect('/home'))
    return respuesta


# hay que decirle a home los methods que puede usar, con get y post
@app.route('/home', methods=['GET', 'POST'])
def home():

    # Creamos la variable login y la psasmos en el diccionario
    login_form = LoginForm()
    fecha = login_form.fecha.data
    importe = login_form.importe.data
    contenido = {
        'hola': {1,2,3},
        'alguno': algunos,
        'login_form': login_form
         }

    if login_form.validate_on_submit():
        import csv
        
        csvData = [[fecha, importe]]

        with open('listaPagos.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()

        return render_template('listado.html', **contenido, fecha= fecha, importe =importe)
       
    else:
        return render_template('formulari.html', **contenido)


class Entrada():
    def __init__(self, fecha , importe):
        self.fecha = fecha
        self.importe = importe
class Todo():
    def __init__(self):
        self._todo = []

    def add(self, fecha, importe):
        entrada = Entrada(fecha, importe)
        self._todo.append(entrada)
        # self._save()

@app.route('/registro_final')
def registro_final():
    import csv
    diccionario ={
        'listado':{}
    }
    # diccionario= {
    #     '4': 4,
    #     '5': 5
    #     }

    with open('listaPagos.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
       
        for row in csv_reader:
            diccionario['listado'][row[0]] = row[1]    


    return render_template('registro_final.html', **diccionario)

if __name__ == "__main__":
    app.run('0.0.0.0', '5000', debug=True)
