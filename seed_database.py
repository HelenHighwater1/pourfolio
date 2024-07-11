"""Script to seed database."""

import os
import json
from random import choice, randint, sample
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system("dropdb pourfolio")
os.system('createdb pourfolio')

connect_to_db(app)
app.app_context().push()
db.create_all()

with open('data/vineyards.json') as f:
    vineyards_data = json.loads(f.read())

with open('data/lots.json') as f:
    lots_data = json.loads(f.read())



vineyards_in_db = []
for vineyard in vineyards_data:
    name = vineyard['name']
    country = vineyard['country']
    region = vineyard['region']

    vineyards_in_db.append(crud.create_vineyard(name=name, 
                              country=country,
                              region=region,
                              ))



for n in range(4):
    email = f'user{n}@test.com'
    user_name = f'name{n}'
    password = 'password'

    user = crud.create_user(user_name, email, password)

    bottles_for_user =[]

    for n in range(30):
        rand_lot_data = choice(lots_data)
        rand_vineyard = choice(vineyards_in_db)
        rand_year = randint(2000, 2020)
        # TODO - do I want to save these as integers or years? 
        rand_vintage = datetime(year=rand_year, month=1, day=1)
        
        lot = crud.create_lot(cellar=user.cellar, 
                              varietal=rand_lot_data['varietal'], 
                              vineyard=rand_vineyard,
                              wine_name=rand_lot_data['wine_name'],
                              vintage=rand_vintage, 
                              celebration=rand_lot_data['celebration']
                              )
  
        num_bottles = randint(1, 12)
        for n in range(num_bottles):
            rand_drinkable_year = randint(2024, 2050)
            drinkable_date = datetime(year=rand_drinkable_year, month=1, day=1)
            
            bottle = crud.create_bottle(lot=lot,
                                        drinkable_date=drinkable_date,
                                        price = randint(20, 100),
                                        purchase_date=datetime.today()
                                        )
            bottles_for_user.append(bottle)


    tasting_note_bottles = sample(bottles_for_user, 40)

    for bottle in tasting_note_bottles:  
        tasting_note = crud.create_tasting_note(bottle=bottle, user=user, note=f"I tasted this! {bottle.lot}! ", date=datetime.today())


