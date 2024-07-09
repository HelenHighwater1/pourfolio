"""CRUD operations."""

from model import db, User, Cellar, Lot, Bottle, TastingNote, Vineyard, connect_to_db


def create_user(name, email, password):
    """Create and return a new user."""

    user = User(name=name,
                email=email, 
                password=password, 
                cellar= create_cellar()
                )

    return user

def create_cellar():
    """Create and return a new Cellar"""

    cellar = Cellar()

    return cellar


def create_lot(cellar_id, vineyard_id, varietal, wine_name, vintage, celebration=False):
    """Creates a new lot.  A lot is a batch of a specific wine with a specific year"""

    lot = Lot(cellar_id=cellar_id,
              vineyard_id=vineyard_id,
              varietal=varietal,  
              wine_name = wine_name,
              vintage=vintage,
              celebration=celebration
              )
    
    return lot


def create_bottle(lot_id, drinkable_date, purchase_date, price, drunk=False):
    """Creates a new bottle from a given lot"""

    bottle = Bottle(lot_id=lot_id,
                    # drinkable_date=, 
                    # purchase_date=,
                    price=price, 
                    drunk=drunk
                    )
    return bottle


def create_tasting_notes(bottle_id, user_id, note, date):
    """Creates a new tasting note"""

    tasting_note = TastingNote(bottle_id=bottle_id,
                               user_id=user_id,
                               note=note,
                                # TODO date=datetime
                               )
    return tasting_note


def create_vineyard(name, country, region):
    """Creates new vineyard"""

    vineyard = Vineyard(name=name, country=country, region=region)

    return vineyard



if __name__ == '__main__':
    from server import app
    connect_to_db(app)