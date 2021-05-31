from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Usuario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), nullable=False)
	correo = db.Column(db.String(120), unique=True, nullable=False)
	clave = db.Column(db.String(120), nullable=False)    
	lenguaje = db.Column(db.String(5), nullable=True)    
	
