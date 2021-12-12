from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('reg_and_login.html')

@app.route('/register', methods = ["POST"])
def register():
    if not User.registrationValidation(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.register(data)
    session['user_id'] = user_id 
    return redirect("/dashboard")

@app.route('/login', methods = ['POST'])
def login():
    if not User.loginValidation(request.form):
        return redirect('/')
    data = {
        'email' : request.form['email']
    }
    user = User.getByEmail(data)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

