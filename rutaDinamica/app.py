from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db 
from models import Usuario
		
@app.route('/')
def inicio():
	return render_template('inicio.html')
	
@app.route('/registrarse', methods = ['GET','POST'])
def registrarse():   
	if request.method == 'POST':
		if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
			return render_template('error.html', error="Los datos ingresados no son correctos...")
		else:
			nuevo_usuario = Usuario(nombre=request.form['nombre'], correo = request.form['email'], clave=generate_password_hash(request.form['password']), lenguaje= request.form['lenguaje'])       
			db.session.add(nuevo_usuario)
			db.session.commit()
			return render_template('aviso.html', mensaje="El usuario se registró exitosamente")
	return render_template('nuevo_usuario.html')

@app.route('/ingresar', methods = ['GET','POST'])
def ingresar():
    if request.method == 'POST':
        if  not request.form['email'] or not request.form['password']:
            return render_template('error.html', error="Por favor ingrese los datos requeridos")
        else:
            usuario_actual= Usuario.query.filter_by(correo= request.form['email']).first()
            if usuario_actual is None:
                return render_template('error.html', error="El correo no está registrado")
            else:
                verificacion = check_password_hash(usuario_actual.clave, request.form['password'])
                if (verificacion):                    
                    return redirect(url_for('bienvenida',leng = usuario_actual.lenguaje))
                else:
                    return render_template('error.html', error="La contraseña no es válida")
    else:
        return render_template('ingresar.html')
 
@app.route('/bienvenida/<leng>')
def bienvenida(leng):
	if leng == 'es':
		return render_template('bienvenida.html', saludo='Hola!')
	else:
		return render_template('bienvenida.html', saludo='Hello')
		
	

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)	