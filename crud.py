"""CRUD operations."""

from model import db, User, Cellar, Lot, Bottle, TastingNote, Vineyard, connect_to_db

from datetime import datetime

# -----------------------
# ----------------------- USER OPERATIONS -----------------------
# -----------------------

def create_user(user_name, email, password):
    """Create and return a new user."""

    user = User(user_name=user_name,
                email=email, 
                password=password, 
                cellar= create_cellar()
                )
    
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_id(id): 
    user = User.query.get(id)
    return user


def get_user_by_email(email): 

    user = User.query.filter(User.email == email).first()
    return user

# -----------------------
# ----------------------- CELLAR OPERATIONS -----------------------
# -----------------------
def create_cellar():
    """Create and return a new Cellar"""

    cellar = Cellar()

    db.session.add(cellar)
    db.session.commit()

    return cellar


def get_all_cellar_lots(cellar_id):
    all_lots = db.session.query(Lot).filter(Lot.cellar_id == cellar_id).all()
    
    return all_lots

# -----------------------
# ----------------------- LOT OPERATIONS -----------------------
# -----------------------

def create_lot(cellar, vineyard, varietal, wine_name, vintage, celebration=False):
    """Creates a new lot.  A lot is a batch of a specific wine with a specific year"""

    lot = Lot(cellar=cellar,
              vineyard=vineyard,
              varietal=varietal,  
              wine_name = wine_name,
              vintage=vintage,
              celebration=celebration
              )
    
    db.session.add(lot)
    db.session.commit()

    return lot


def get_lot_by_id(lot_id): 
    lot = Lot.query.get(lot_id)
    return lot


# -----------------------
# ----------------------- BOTTLE OPERATIONS -----------------------
# -----------------------

def create_bottle(lot, drinkable_date, purchase_date, price, drunk=False):
    """Creates a new bottle from a given lot"""

    bottle = Bottle(lot=lot,
                    drinkable_date=drinkable_date, 
                    purchase_date=purchase_date,
                    price=price, 
                    drunk=drunk
                    )
    
    db.session.add(bottle)
    db.session.commit()

    return bottle

def get_count_drinkable_bottles(lot_id):
    this_year = datetime.today()
    count_of_drinkable_bottles = Bottle.query.filter(Bottle.lot_id == lot_id, 
                                                     Bottle.drunk == False, 
                                                     Bottle.drinkable_date <= this_year
                                                     ).count()
    return count_of_drinkable_bottles

def get_count_all_bottles(lot_id):
    count_all_bottles = Bottle.query.filter(Bottle.lot_id == lot_id, 
                                            Bottle.drunk == False, 
                                            ).count()
    return count_all_bottles


# -----------------------
# ----------------------- TASTING N0TE OPERATIONS -----------------------
# -----------------------

def create_tasting_note(bottle, user, note, date):
    """Creates a new tasting note"""

    tasting_note = TastingNote(bottle=bottle,
                               user=user,
                               note=note,
                               date=date
                               )

    db.session.add(tasting_note)
    db.session.commit()    
    
    return tasting_note


def get_all_tasting_notes(lot_id):
    all_tasting_notes = db.session.query(TastingNote).join(Bottle).filter(Bottle.lot_id == lot_id).all()
    return all_tasting_notes


# -----------------------
# ----------------------- VINEYARD OPERATIONS -----------------------
# -----------------------
def create_vineyard(name, country, region):
    """Creates new vineyard"""
    """Creates new vineyard"""

    vineyard = Vineyard(name=name, country=country, region=region)

    db.session.add(vineyard)
    db.session.commit()

    return vineyard



if __name__ == '__main__':
    from server import app
    connect_to_db(app)