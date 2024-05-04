from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import mariadb
import os
from dbAccess import Db

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(12).hex()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
dbCursor = Db()

#region managed login
@app.route('/login', methods=['POST', 'GET'])
def login():
    err = ''
    if request.method == 'POST':
        username = request.form.get('usernameInput')
        password = request.form.get('passwordInput')
        try:
            user = dbCursor.getUser(username)
            if user and user.checkPass(password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                err = 'Invalid login attempt'
        except:
            err = 'Error while trying to log in, try again.'
    return render_template('login.html', message=err)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(username):
    return dbCursor.getUser(username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():  
    err = ''
    if request.method == 'POST':
        email = request.form.get('emailInput')
        username = request.form.get('usernameInput')
        password = request.form.get('passwordInput')
        try:
            dbCursor.saveUser(username, password, email)
            user = dbCursor.getUser(username)
            if user and user.checkPass(password):
                login_user(user)
                return redirect(url_for('home'))
        except mariadb.IntegrityError:
            err = 'Username already exists'
        
    return render_template('signup.html', message=err)
#endregion

@app.route('/')
@login_required
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True, port='5555')
