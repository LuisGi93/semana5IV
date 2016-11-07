# -*- coding: utf-8 -*-
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, json

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RecipeForm, RegisterForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Receta

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    """
    Permite a un usuario registrado en el sistema iniciar sesion.

        Returns:
            En caso de que los datos introducidos por el usuario en el formulario de login sean correctos
            redirige al usuario a una ventana de bienvenida.
            En caso de que los datos introducidos sean incorrectos redirige al usuario de nuevo al página del formulario
            de login
        """
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):

            session['user_id'] = user.email
            flash('Welcome %s' % user.name)
            return render_template("auth/show.html", name=session['user_id'])
        else:
            return render_template("auth/signin.html", form=form)
    return render_template("auth/signin.html", form=form)


@mod_auth.route('/sigup/', methods=['GET', 'POST'])
def signup():
    """
    Permite a un usuario registrarse en el sistema

        Returns:
            Si no existe un usuario con los datos introducidos en el sistema lo añade al sistema y le redirige a la página de inicio de sesión.
            Si existe entonces lo redirige a la página de inicio de sesión.
        """

    # If sign in form is submitted
    form = RegisterForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user :
            flash('Usuario ya existe', 'error-message')
            form = LoginForm(request.form)
            return render_template("auth/signin.html", form=form)
        else :
            a=User(form.username.data,form.email.data,form.password.data, 'user', '0')
            db.session.add(a)
            db.session.commit()
            form = LoginForm(request.form)
            return redirect(url_for('auth.signin'))


    return render_template("sigup.html", form=form)


@mod_auth.route('/show/', methods=['GET', 'POST'])
def show():
        user = User.query.filter_by(email=session['user_id']).first()

        if user:
            flash('Welcome %s' % user.name)
        else:
            flash('Wrong email or password', 'error-message')
        return render_template("auth/show.html", name=user.email)


@mod_auth.route('/misrecetas/', methods=['GET', 'POST'])
def show_recetas_propias():
        if session['user_id'] != "":
            user = User.query.filter_by(email=session['user_id']).first()
            receta = Receta.query.filter_by(usuario=user.email).order_by(Receta.date_created).all()
            if receta :
                return render_template("recetas_usuario.html", receta=receta, aux=receta[0].usuario)
            else:
                return render_template("recetas_usuario.html", name="")
        else:
            return redirect(url_for('auth.signin'))


@mod_auth.route('/recetas/<username>', methods=['GET', 'POST'])
def show_recetas_usuario(username):
        if session['user_id'] != "":
            user = User.query.all()
            #return render_template("auth/show.html", array=user)
            user = User.query.filter_by(name=username).first()
            receta = Receta.query.filter_by(usuario=user.email).order_by(Receta.date_created).all()
            if receta :
                return render_template("recetas_usuario.html", receta=receta, aux=receta[0].usuario)
            else:
                return render_template("recetas_usuario.html", name="")
        else:
            return redirect(url_for('auth.signin'))



@mod_auth.route('/todas_recetas/', methods=['GET', 'POST'])
def show_recetas():

        #    receta = Receta('Spaguettis', 'cocinero_vasco@arguinanogabilondourdangarin.com','Spaguettis, carne  y tomate')
        #    db.session.add(receta)
        #db.session.commit()
            receta = Receta.query.order_by(Receta.date_created).all()
            list = []
            for i in receta:
                list.append({ 'Titulo' : i.titulo })
                list.append({ 'Descripcion' : i.descripcion })
                list.append({  'Usuario' : i.usuario })
            #for num in range(0,receta):
            #    list.append(receta.usuario)
            return json.dumps(list)
            if receta :
                return render_template("recetas_usuario.html", receta=receta, aux=receta[0].usuario)
            else:
                return render_template("recetas_usuario.html", name="")

@mod_auth.route('/todas_recetas/<titulo>', methods=['GET', 'POST'])
def show_receta(titulo):

                receta = Receta.query.filter_by(titulo=titulo).first()
                list = []
                #list.append({ 'Titulo' : receta.titulo, 'Descripcion' : receta.descripcion, 'Usuario' : receta.usuario })
                list.append({ 'Titulo' : receta.titulo })
                list.append({ 'Descripcion' : receta.descripcion })
                list.append({  'Usuario' : receta.usuario })
                return json.dumps(list)

@mod_auth.route('/introducir_receta/', methods=['GET', 'POST'])
def introducir_receta():
    form = RecipeForm(request.form)
    if form.validate_on_submit():
        if session['user_id'] != "":
            receta = Receta.query.filter_by(titulo=form.titulo.data).first()
            if receta :
                return render_template("auth/show.html", name=receta.titulo)
            else :
                user = User.query.filter_by(email=session['user_id']).first()
                if user:
                    a=Receta(form.titulo.data,user.email, form.descripcion.data)
                    db.session.add(a)
                    db.session.commit()
                    receta = Receta.query.filter_by(usuario=user.email).order_by(Receta.date_created).all()
                    return render_template("recetas_usuario.html", receta=receta, name=user.name)
    return render_template("anadir_receta.html",form=form)


@mod_auth.route('/')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@mod_auth.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)
