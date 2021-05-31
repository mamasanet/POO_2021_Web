from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
#import config	

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(config)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)    
    post = db.relationship('Post', backref='user', cascade="all, delete-orphan" , lazy='dynamic')
    
    def __init__(self, nombre, email, password):
       self.nombre = nombre
       self.email = email
       self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    
    def __init__(self, contenido, user_id):
        self.contenido = contenido
        self.user_id = user_id

@app.route('/')
def inicio():
	return render_template("inicio.html")	

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404
    
@app.route('/listar_usuarios')
def listar_usuarios():
   return render_template('listar_usuarios.html', users = User.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
         flash('Please enter all the fields', 'error')
      else:
         user = User(request.form['nombre'], request.form['email'], request.form['password'])
         
         db.session.add(user)
         db.session.commit()
         flash('El usuario se registró existosamente')
        
   return render_template('nuevo_usuario.html')

@app.route('/nuevo_post', methods = ['GET', 'POST'])
def nuevo_post():
   if request.method == 'POST':
      if not request.form['email']:
         flash('Por favor ingrese el correo', 'error')
      else:
         
         user_actual= User.query.filter_by(email=request.form['email']).first()
         if user_actual is None:
            return render_template('error.html', error="Usuario no encontrado..."), 1
         else:
            return render_template('ingresar_post.html', user= user_actual)
   return render_template('nuevo_post.html')

@app.route('/ingresar_post', methods = ['GET', 'POST'])
def ingresar_post():
    if request.method == 'POST':
        if not request.form['contenido']:
            return render_template('error.html', error="contenido no ingresado..."), 2
        else:            
            post= Post(request.form['contenido'], request.form['userId'])    
            db.session.add(post)
            db.session.commit()
            return render_template('inicio.html') 
    return render_template('inicio.html') 

@app.route('/listar_post')
def listar_post():
   return render_template('listar_post.html', posts = Post.query.all() )

@app.route('/listar_post_user', methods = ['GET', 'POST'])
def listar_post_user():     
    if request.method == 'POST':
        if not request.form['usuarios']:
            return render_template('listar_post_user.html', users = User.query.all(), user_seleccionado = None )
        else:
            return render_template('listar_post_user.html', users= None, user_seleccionado = User.query.get(request.form['usuarios'])) 
    else:
        return render_template('listar_post_user.html', users = User.query.all(), user_seleccionado = None  )    
@app.route("/post_user/<int:user_id>")
def post_user(user_id):
  user = User.query.get_or_404(user_id)
  print(user.nombre) 
  return render_template('post_user.html', user_post=user.post)
  
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)