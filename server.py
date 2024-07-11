from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# ----------------------- USER ROUTES -----------------------

@app.route('/')
def homepage(): 
    if session.get('user', None) != None:
        return redirect('/cellar')
    return render_template('sign_in.html')


@app.route('/login', methods=['POST'])
def login():
    user_email = request.form['email']
    password = request.form['password']
    user = crud.get_user_by_email(user_email)

    if user:
        if user.password == password:
            session['user'] = user.user_id
            session['cellar']= user.cellar_id
            flash('logged in!')
            return redirect('/cellar')
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
        session['cellar']= user.cellar_id
        flash("Congratulations - you have an account and are logged in!")    
        return redirect('/cellar')
    

@app.route('/logout')
def logout():
    session.pop('user')
    session.pop('cellar')
    return redirect('/')


# ----------------------- CELLER / LOT ROUTES -----------------------

@app.route('/cellar')
def cellar():
    user = crud.get_user_by_id(session['user'])
    if user: 
        all_cellar_lots = crud.get_all_cellar_lots(session['cellar'])
        return render_template('cellar.html', user=user, all_cellar_lots=all_cellar_lots)
    else: 
        return redirect('/')
    

@app.route('/lots/<lot_id>')
def show_lot(lot_id):
    lot = crud.get_lot_by_id(lot_id)
    all_tasting_notes = crud.get_all_tasting_notes(lot_id)
    count_all_bottles = crud.get_count_all_bottles(lot_id)
    count_drinkable_bottles = crud.get_count_drinkable_bottles(lot_id)
    return render_template('lot.html', lot=lot, count_drinkable_bottles=count_drinkable_bottles, count_all_bottles=count_all_bottles, all_tasting_notes=all_tasting_notes)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)