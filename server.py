from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from datetime import datetime
from model import connect_to_db, db, VARIETALS

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# -----------------------
# ----------------------- USER ROUTES -----------------------
# -----------------------
@app.route('/')
def homepage(): 
    if session.get('user') != None:
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
            session['user_name'] = user.user_name
            session['cellar']= user.cellar_id
            session['current_year'] = datetime.today().year
            flash('logged in!')
            return redirect('/cellar')
        else:
  
            flash('incorrect username/password')
    else:
        flash('incorrect username/password')
        return redirect('/')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    """Allows user to sign up, and logs them in"""

    email = request.form['email']
    user_name = request.form['user_name']
    password = request.form['password']
    user = crud.get_user_by_email(email)

    if user:
        flash("Looks like we already have an account with that email! Please sign in.")
        return redirect('/')
    else: 
        user = crud.create_user(user_name=user_name, email=email, password=password)
        session.clear()
        flash("Congratulations - you have an account and are logged in!")    
        return redirect('/cellar')
    

@app.route('/logout')
def logout():
    """Logs User out- removes cellar and user from session."""
    session.clear()
    return redirect('/')


# -----------------------
# ----------------------- CELLER ROUTES ---------------------
# -----------------------

@app.route('/cellar')
def cellar():
    user = crud.get_user_by_id(session['user'])
    
    if user: 
        varietals = crud.get_all_cellar_varietals(session['cellar'])
        vintages = crud.get_all_cellar_vintages(session['cellar'])
        vineyards = crud.get_all_cellar_vineyards(session['cellar'])
        countries = crud.get_all_cellar_countries(session['cellar'])
        regions = crud.get_all_cellar_regions(session['cellar'])
        all_cellar_lots = crud.get_all_cellar_lots(session['cellar'])
        all_drinkable_cellar_lots = crud.get_all_drinkable_cellar_lots(session['cellar'])
        return render_template(
            'cellar.html', 
            user = user, 
            all_cellar_lots = all_cellar_lots,
            all_drinkable_cellar_lots= all_drinkable_cellar_lots,
            varietals = varietals,
            vintages = vintages, 
            vineyards = vineyards, 
            countries = countries, 
            regions = regions
            )
    
    else: 
        return redirect('/')
    

@app.route('/add_to_cellar')
def add_to_cellar():
    all_vineyards = crud.get_all_vineyards()
    return render_template('create_lot.html', all_vineyards=all_vineyards, VARIETALS=VARIETALS)



# -----------------------
# ----------------------- FILTER CELLAR ROUTES ---------------------
# -----------------------

@app.route('/filter_cellar')
def filter_cellar():
    filter_on = request.args.get('filter_on')
    filter_val = request.args.get('filter_val')
    cellar_id = session['cellar']

    if filter_on in ('vineyard', 'region', 'country'):
        filtered_lots = crud.filter_cellar_lots_on_vineyard_info(filter_on=filter_on, filter_val=filter_val, cellar_id=cellar_id)
    else:
        filtered_lots = crud.filter_cellar_lots(filter_on=filter_on, filter_val=filter_val, cellar_id=cellar_id)

    dict_lots = []
    for lot in filtered_lots:
        dict_lots.append(lot.make_dict())

    return jsonify(dict_lots)


@app.route('/search_cellar')
def search_cellar():
    search_term = request.args.get('search_term')
    cellar_id = session['cellar']
    search_results = crud.get_lots_by_search_term(cellar_id=cellar_id, search_term=search_term)

    dict_lots = []
    for lot in search_results:
        dict_lots.append(lot.make_dict())

    return jsonify(dict_lots)


# -----------------------
# ----------------------- LOT ROUTES ---------------------
# -----------------------

@app.route('/lots/<lot_id>')
def show_lot(lot_id):
    lot = crud.get_lot_by_id(lot_id)
    all_tasting_notes = crud.get_all_tasting_notes(lot_id)
    count_all_bottles = crud.get_count_all_bottles(lot_id)
    count_drinkable_bottles = crud.get_count_drinkable_bottles(lot_id)
    return render_template('lot.html', 
                           lot=lot, 
                           count_drinkable_bottles=count_drinkable_bottles, 
                           count_all_bottles=count_all_bottles, 
                           all_tasting_notes=all_tasting_notes, 
                           )


@app.route('/create_lot', methods=['POST'])
def create_lot():
    vineyard_id = request.form['vineyard']
    vineyard = crud.get_vineyard_by_id(vineyard_id)

    celebration_val = request.form['celebration']
    if celebration_val == 'true':
        celebration = True
    else: 
        celebration = False
    
    varietal= request.form['varietal']
    wine_name= request.form['wine_name']
    vintage= request.form['vintage']
    bottle_qty = request.form['bottle_qty']
    cellar = crud.get_cellar_by_id(session['cellar'])

    lot = crud.create_lot(cellar=cellar,
              vineyard=vineyard,
              varietal=varietal,  
              wine_name = wine_name,
              vintage=vintage,
              celebration=celebration
              )
    if bottle_qty:
        return redirect(url_for('create_aging_lot', lot_id=lot.lot_id, bottle_qty=bottle_qty))
    else: 
        return redirect(f'/lots/{lot.lot_id}')

# -----------------------
# ----------------------- BOTTLE ROUTES -----------------------
# -----------------------

@app.route('/drink/<lot_id>')
def drink_bottle(lot_id): 
    """Takes the bottle with earliest "drinkable" date and sets it to drunk= True """
    bottle = crud.drink_earliest_drinkable_date_bottle(lot_id)

    return render_template('create_tasting_note.html', bottle=bottle)


@app.route('/create_aging_schedule/<lot_id>')
def create_aging_lot(lot_id):
    if not request.args['bottle_qty'] or not request.args['bottle_qty'].isdigit():
        flash('Invalid or missing bottle quantity parameter.')
        return redirect(f'/lots/{lot_id}')
    lot_aging_schedule = crud.get_lot_aging_schedule(lot_id)
    lot = crud.get_lot_by_id(lot_id) 
    bottle_qty = int(request.args['bottle_qty'])
    return render_template('create_aging_schedule.html', lot=lot, bottle_qty=bottle_qty, lot_aging_schedule=lot_aging_schedule)


@app.route('/add_bottles/<lot_id>', methods=["POST"])
def add_bottles_to_lot(lot_id):
    lot = crud.get_lot_by_id(lot_id)
    all_years = request.form.getlist('year')
    for year in all_years:
        drinkable_date = datetime(year=int(year), month=1, day=2)
        bottle = crud.create_bottle(lot=lot, drinkable_date=drinkable_date, purchase_date = datetime.today(), price=0)
    return redirect(f'/lots/{lot_id}')




# -----------------------
# ----------------------- TASTING N0TE ROUTES -----------------------
# -----------------------


@app.route('/create_tasting_note/<bottle_id>', methods=["POST"])
def create_tasting_note(bottle_id):
    bottle = crud.get_bottle_by_id(bottle_id)
    note = request.form['note']
    date = crud.datetime.today()
    user = crud.get_user_by_id(session['user'])

    tasting_note = crud.create_tasting_note(
        bottle=bottle, 
        note=note,
        date=date,
        user=user
        )
    return redirect(f'/lots/{bottle.lot_id}')


# -----------------------
# ----------------------- Vineyard ROUTES -----------------------
# -----------------------

@app.route('/add_vineyard')
def add_vineyard():
    return render_template('create_vineyard.html')


@app.route('/create_vineyard', methods=['POST'])
def create_vineyard():
    name = request.form['vineyard_name'].strip().capitalize()
    if crud.get_vineyard_by_name(name):
        flash('Vineyard already exists.')
        return redirect('/add_to_cellar')
    region = request.form['region'].strip().capitalize()
    country = request.form['country'].strip().capitalize()


    lot = crud.create_vineyard(
              name=name,
              region=region,
              country=country
              )
    
    return redirect('/add_to_cellar')



# ----------------------------------------------------------------
# -----------------------------------------------------------------

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)