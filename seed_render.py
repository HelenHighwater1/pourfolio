"""Seed script for Render deployment. Uses db.create_all() instead of shell commands."""

import json
from random import choice, randint, sample
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

connect_to_db(app, echo=False)
app.app_context().push()
db.create_all()

if crud.get_user_by_email("user0@test.com"):
    print("Database already seeded, skipping.")
else:
    print("Seeding database...")

    with open("data/vineyards.json") as f:
        vineyards_data = json.loads(f.read())

    with open("data/lots.json") as f:
        lots_data = json.loads(f.read())

    vineyards_in_db = []
    for vineyard in vineyards_data:
        vineyards_in_db.append(
            crud.create_vineyard(
                name=vineyard["name"],
                country=vineyard["country"],
                region=vineyard["region"],
            )
        )

    for n in range(4):
        email = f"user{n}@test.com"
        user_name = f"Name{n}"
        password = "password"

        user = crud.create_user(user_name, email, password)

        bottles_for_user = []

        for i in range(30):
            rand_lot_data = choice(lots_data)
            rand_vineyard = choice(vineyards_in_db)
            rand_year = randint(2000, 2020)
            rand_vintage = datetime(year=rand_year, month=1, day=2)

            lot = crud.create_lot(
                cellar=user.cellar,
                varietal=rand_lot_data["varietal"],
                vineyard=rand_vineyard,
                wine_name=rand_lot_data["wine_name"],
                vintage=rand_vintage,
                celebration=rand_lot_data["celebration"],
            )

            num_bottles = randint(1, 12)
            for j in range(num_bottles):
                rand_drinkable_year = randint(2024, 2050)
                drinkable_date = datetime(year=rand_drinkable_year, month=1, day=2)

                bottle = crud.create_bottle(
                    lot=lot,
                    drinkable_date=drinkable_date,
                    price=randint(20, 100),
                    purchase_date=datetime.today(),
                )
                bottles_for_user.append(bottle)

        tasting_note_bottles = sample(bottles_for_user, 40)

        for bottle in tasting_note_bottles:
            crud.create_tasting_note(
                bottle=bottle,
                user=user,
                note=f"I tasted this! {bottle.lot}! ",
                date=datetime.today(),
            )

    print("Seeding complete!")
