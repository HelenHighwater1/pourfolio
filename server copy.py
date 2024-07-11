from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage(): 
    return render_template('sign_in.html')

@app.route('/cellar')
def cellar():
    return render_template('cellar.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    user_email = request.form['email']
    password = request.form['password']
    user = crud.get_user_by_email(user_email)

    if user:
        if user.password == password:
            session['user'] = user.user_id
            flash('logged in!')
            return redirect('/cellar', user=user)
        else:
            flash('incorrect password')
    else:
        flash('no user with that username')
        return redirect('/')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    """Allows user to sign up, and logs them in"""
    print('in sign_up')

    email = request.form['email']
    user_name = request.form['user_name']
    password = request.form['password']
    user = crud.get_user_by_email(email)

    if user:
        flash("Looks like we already have an account with that email! Please sign in.")
        return redirect('/')
    else: 
        print('in else stmt')
        user = crud.create_user(user_name=user_name, email=email, password=password)
        session['user'] = user.user_id
        flash("Congratulations - you have an account and are logged in!")    
        return redirect('/cellar', user=user)
    

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)