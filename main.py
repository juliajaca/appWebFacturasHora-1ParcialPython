
from flask import Flask, request, make_response, redirect, render_template, session, url_for

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm 

from wtforms.fields import StringField, IntegerField, SubmitField

from wtforms.validators import DataRequired #para decir los requerimientos que recoge el formulario

app = Flask(__name__)

boostrap = Bootstrap(app)

# formulario
class LoginForm(FlaskForm): # Metemos una clase dentro de una clase, esto tiene un nombre pero no recuerdo cual es
    fecha = StringField('Fecha', validators=[DataRequired()])
    importe = IntegerField('Importe', validators=[DataRequired()])
    enviar = SubmitField('Registrar')


# A secret key is required to use CSRF
app.config['SECRET_KEY'] = 'SUPER_SECRETO'

@app.route('/')
def hola_mundo():
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




@app.route('/registro_final')
def registro_final():
    import csv
    diccionario ={
        'listado':{}
    }

    with open('listaPagos.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
       
        for row in csv_reader:
            diccionario['listado'][row[0]] = row[1]    

    return render_template('registro_final.html', **diccionario)





if __name__ == "__main__":
    app.run('0.0.0.0', '5000', debug=True)
