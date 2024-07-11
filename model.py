"""Models for Pourfolio."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    cellar_id = db.Column(db.ForeignKey('cellars.cellar_id'))
    user_name = db.Column(db.String(25))
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    cellar = db.relationship("Cellar", back_populates="user")
    tasting_notes = db.relationship("TastingNote", back_populates='user')

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.user_name} email={self.email}>'


class Cellar(db.Model):
    """A cellar."""

    __tablename__ = 'cellars'

    cellar_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    user = db.relationship("User", back_populates="cellar")
    lots = db.relationship("Lot", back_populates="cellar")

    def __repr__(self):
        return f'<Cellar cellar_id={self.cellar_id}>'


class Lot(db.Model):
    """A lot of wine -> Specific wine that belongs to a vineyard, has one year, 
    and represents many bottles."""

    __tablename__ = 'lots'

    lot_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    cellar_id = db.Column(db.ForeignKey('cellars.cellar_id'))
    vineyard_id = db.Column(db.ForeignKey('vineyards.vineyard_id'))
    varietal = db.Column(db.String(40))
    wine_name = db.Column(db.String(50))
    vintage = db.Column(db.DateTime)
    celebration = db.Column(db.Boolean, default=False)

    #TODO -check this again for singular vs plural
    cellar = db.relationship("Cellar", back_populates="lots")
    vineyard = db.relationship("Vineyard", back_populates="lot")
    bottles = db.relationship("Bottle", back_populates="lot")

    def __repr__(self):
        return f'<Lot lot_id={self.lot_id} name={self.wine_name} vintage={self.vintage}, vineyard={self.vineyard_id} celebration={self.celebration}>'


class Bottle(db.Model):
    """A single bottle.  Has a date purchased, price, drinkable date, and t/f boolian for if it has been drunk"""

    __tablename__ = 'bottles'

    bottle_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    lot_id = db.Column(db.ForeignKey('lots.lot_id')) 
    # TODO - consider how drinkable date works.
    drinkable_date = db.Column(db.DateTime)
    purchase_date = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    drunk = db.Column(db.Boolean, default=False)

 
    lot = db.relationship("Lot", back_populates="bottles")
    tasting_notes = db.relationship("TastingNote", back_populates="bottle")


    def __repr__(self):
        return f'<Bottle bottle_id={self.bottle_id} drinkable_date={self.drinkable_date} purchase_date={self.purchase_date} price={self.price} drunk={self.drunk}>'


class TastingNote(db.Model):
    """A tasting note - belongs to a bottle"""

    __tablename__ = 'tasting_notes'

    tasting_note_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    bottle_id = db.Column(db.ForeignKey('bottles.bottle_id'))
    user_id = db.Column(db.ForeignKey('users.user_id'))
    note = db.Column(db.Text)
    date = db.Column(db.DateTime)

    # TODO - Check singular vs plural
    bottle = db.relationship("Bottle", back_populates="tasting_notes")
    user= db.relationship("User", back_populates="tasting_notes")

    def __repr__(self):
        return f'<Tasting_note tasting_note_id={self.tasting_note_id} bottle_id={self.bottle_id} user={self.user_id}>'


class Vineyard(db.Model):
    """A vineyard, gives country and region"""

    __tablename__ = 'vineyards'

    vineyard_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    country = db.Column(db.String)
    region = db.Column(db.String)

    lot = db.relationship("Lot", back_populates="vineyard")


    def __repr__(self):
        return f'<Vineyard vineyard_id={self.vineyard_id} name={self.name} region={self.region} country={self.country}>'



def connect_to_db(flask_app, db_uri="postgresql:///pourfolio", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
