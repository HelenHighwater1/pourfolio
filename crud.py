"""CRUD operations."""

from model import db, User, Cellar, Lot, Bottle, TastingNote, Vineyard, connect_to_db


from sqlalchemy import func, or_
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


def get_all_drinkable_cellar_lots(cellar_id):
    all_drinkable_lots = (
        db.session.query(Lot)
        .join(Lot.bottles) 
        .filter(
            Lot.cellar_id == cellar_id,  
            Bottle.drinkable_date.isnot(None),  
            db.extract('year', Bottle.drinkable_date) == datetime.today().year  
        ).distinct().all()
    )
    return all_drinkable_lots


def get_cellar_by_id(cellar_id):
    cellar = Cellar.query.get(cellar_id)
    return cellar


# -----------------------
# ----------------------- FILTER CELLAR OPERATIONS -------------------------
# -----------------------

def filter_cellar_lots(filter_on, filter_val, cellar_id):
    if filter_on == 'celebration':
        if filter_val == 'True':
            filter_val = True
        else: 
            filter_val = False
    all_filtered_lots = db.session.query(Lot).filter(
        Lot.cellar_id == cellar_id
        ).where(getattr(Lot, f'{filter_on}') == filter_val).all()
    
    return all_filtered_lots

def filter_cellar_lots_on_vineyard_info(filter_on, filter_val, cellar_id):
    if filter_on == 'vineyard':
        filter_on = 'name'

    all_filtered_lots = db.session.query(Lot).join(Vineyard, Lot.vineyard_id == Vineyard.vineyard_id).filter(
        Lot.cellar_id == cellar_id,
        getattr(Vineyard, f'{filter_on}') == filter_val
    ).all()

    return all_filtered_lots


def get_all_cellar_varietals(cellar_id):
    varietal_query = db.session.query(Lot.varietal).filter(
        Lot.cellar_id == cellar_id
        ).distinct().all()
    all_varietals = []

    for varietal in varietal_query:
        all_varietals.append(varietal[0])

    return all_varietals

def get_all_cellar_vineyards(cellar_id):
    vineyard_query = db.session.query(
                        Vineyard.name
                        ).join(
                        Lot, Lot.vineyard_id == Vineyard.vineyard_id
                        ).filter(Lot.cellar_id == cellar_id).distinct().all()
    all_vineyards = []

    for vineyard in vineyard_query:
        all_vineyards.append(vineyard[0])

    return all_vineyards


def get_all_cellar_countries(cellar_id):
    country_query = db.session.query(
                        Vineyard.country
                        ).join(
                        Lot, Lot.vineyard_id == Vineyard.vineyard_id
                        ).filter(Lot.cellar_id == cellar_id).distinct().all()
    all_countries = []

    for country in country_query:
        all_countries.append(country[0])

    return all_countries


def get_all_cellar_regions(cellar_id):
    region_query = db.session.query(
                        Vineyard.region).join(
                        Lot, Lot.vineyard_id == Vineyard.vineyard_id
                        ).filter(Lot.cellar_id == cellar_id).distinct().all()
    all_regions = []

    for region in region_query:
        all_regions.append(region[0])

    return all_regions


def get_all_cellar_vintages(cellar_id):
    vintage_query = db.session.query(Lot.vintage).filter(
        Lot.cellar_id == cellar_id
        ).distinct().all()
    all_vintages = []

    for vintage in vintage_query:
        all_vintages.append(vintage[0])

    return all_vintages


# -----------------------
# ----------------------- SEARCH CELLAR OPERATIONS -------------------------
# -----------------------

def get_lots_by_search_term(cellar_id, search_term):
    search_results = db.session.query(Lot).join(Vineyard).filter(
        Lot.cellar_id == cellar_id).where(or_(
        Vineyard.name.ilike(f"%{search_term}%"),
        Lot.wine_name.ilike(f"%{search_term}%")
        )).distinct().all()

    return search_results


# -----------------------
# ----------------------- LOT OPERATIONS -------------------------
# -----------------------


def create_lot(cellar, vineyard, varietal, wine_name, vintage, celebration=False):
    """Creates a new lot.  A lot is a batch of a specific wine with a specific year"""

    if not isinstance(vintage, datetime):
        year = int(vintage)
        vintage = datetime(year = year, day=2, month=1)
    
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


def get_lot_aging_schedule(lot_id):
    all_bottles_aging_schedule = db.session.query(
        Bottle.drinkable_date, 
        func.count(Bottle.bottle_id)
        ).filter(
            Bottle.lot_id == lot_id
            ).group_by(Bottle.drinkable_date).order_by(Bottle.drinkable_date)


    return all_bottles_aging_schedule


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


def get_bottle_by_id(bottle_id):
    bottle = Bottle.query.get(bottle_id)
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

def drink_earliest_drinkable_date_bottle(lot_id):
    """ Returns the bottle from a lot with the earliest "drinkable date" """
    earliest_drinkable_date_bottle = Bottle.query.filter(Bottle.lot_id == lot_id, 
                                                     Bottle.drunk == False
                                                    ).order_by(Bottle.drinkable_date).first()

    earliest_drinkable_date_bottle.drunk = True
    db.session.add(earliest_drinkable_date_bottle)
    db.session.commit()
    
    return earliest_drinkable_date_bottle
 


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

    vineyard = Vineyard(name=name, country=country, region=region)

    db.session.add(vineyard)
    db.session.commit()

    return vineyard


def update_vineyard(vineyard_id, name, country, region):
    """Updates an existing vineyard."""
    
    vineyard = Vineyard.query.get(vineyard_id)
    if vineyard:
        vineyard.name = name
        vineyard.country = country
        vineyard.region = region
        

        db.session.commit()
    return vineyard



def get_all_vineyards():
    all_vineyards = Vineyard.query.all()
    return all_vineyards


def get_vineyard_by_id(vineyard_id):
    vineyard = Vineyard.query.get(vineyard_id)
    return vineyard


def get_vineyard_by_name(vineyard_name):
    vineyard = Vineyard.query.filter(Vineyard.name == vineyard_name).first()
    return vineyard


# ----------------------------------------------------------------
# -----------------------------------------------------------------

if __name__ == '__main__':
    from server import app
    connect_to_db(app)