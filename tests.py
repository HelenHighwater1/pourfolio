"""Test suite for Pourfolio."""

import unittest
from datetime import datetime

from server import app
from model import connect_to_db, db
import crud


TEST_DB_URI = "postgresql:///pourfolio_test"

connect_to_db(app, db_uri=TEST_DB_URI, echo=False)
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False


def seed_test_data():
    """Create minimal test data: user, cellar, vineyard, lot, bottles."""

    vineyard = crud.create_vineyard(name="Test Vineyard", country="France", region="Bordeaux")
    user = crud.create_user(user_name="TestUser", email="test@test.com", password="password")

    lot = crud.create_lot(
        cellar=user.cellar,
        vineyard=vineyard,
        varietal="Cabernet Sauvignon",
        wine_name="Test Wine",
        vintage=datetime(2020, 1, 2),
        celebration=False,
    )

    crud.create_bottle(lot=lot, drinkable_date=datetime(2024, 1, 2), purchase_date=datetime.today(), price=50)
    crud.create_bottle(lot=lot, drinkable_date=datetime(2030, 1, 2), purchase_date=datetime.today(), price=60)
    crud.create_bottle(lot=lot, drinkable_date=datetime(2035, 1, 2), purchase_date=datetime.today(), price=70)

    return user, vineyard, lot


class BaseTestCase(unittest.TestCase):
    """Base test case that sets up and tears down the test database."""

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        self.user, self.vineyard, self.lot = seed_test_data()
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        self.ctx.pop()

    def login(self):
        """Helper: log in as the test user via session."""
        with self.client.session_transaction() as sess:
            sess["user"] = self.user.user_id
            sess["user_name"] = self.user.user_name
            sess["cellar"] = self.user.cellar_id
            sess["current_year"] = datetime.today().year


# ---------------------------------------------------------------------------
# CRUD Unit Tests
# ---------------------------------------------------------------------------

class TestUserCrud(BaseTestCase):

    def test_create_user(self):
        user = crud.create_user("NewUser", "new@test.com", "pass123")
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.user_name, "NewUser")
        self.assertIsNotNone(user.cellar_id)

    def test_get_user_by_email_found(self):
        user = crud.get_user_by_email("test@test.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")

    def test_get_user_by_email_not_found(self):
        user = crud.get_user_by_email("nobody@test.com")
        self.assertIsNone(user)


class TestVineyardCrud(BaseTestCase):

    def test_create_vineyard(self):
        v = crud.create_vineyard("Chateau Nouveau", "France", "Burgundy")
        self.assertIsNotNone(v.vineyard_id)
        self.assertEqual(v.name, "Chateau Nouveau")

    def test_get_vineyard_by_name(self):
        v = crud.get_vineyard_by_name("Test Vineyard")
        self.assertIsNotNone(v)
        self.assertEqual(v.country, "France")

    def test_get_vineyard_by_name_not_found(self):
        v = crud.get_vineyard_by_name("Nonexistent")
        self.assertIsNone(v)

    def test_update_vineyard(self):
        updated = crud.update_vineyard(self.vineyard.vineyard_id, "Updated Name", "Italy", "Tuscany")
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.country, "Italy")

    def test_update_vineyard_not_found(self):
        result = crud.update_vineyard(99999, "Name", "Country", "Region")
        self.assertIsNone(result)


class TestLotCrud(BaseTestCase):

    def test_create_lot(self):
        lot = crud.create_lot(self.user.cellar, self.vineyard, "Merlot", "New Wine", datetime(2021, 1, 2))
        self.assertIsNotNone(lot.lot_id)
        self.assertEqual(lot.wine_name, "New Wine")

    def test_create_lot_with_string_vintage(self):
        lot = crud.create_lot(self.user.cellar, self.vineyard, "Merlot", "String Year Wine", "2019")
        self.assertEqual(lot.vintage.year, 2019)

    def test_get_lot_by_id(self):
        lot = crud.get_lot_by_id(self.lot.lot_id)
        self.assertIsNotNone(lot)
        self.assertEqual(lot.wine_name, "Test Wine")

    def test_get_lot_by_id_not_found(self):
        lot = crud.get_lot_by_id(99999)
        self.assertIsNone(lot)


class TestBottleCrud(BaseTestCase):

    def test_create_bottle(self):
        bottle = crud.create_bottle(self.lot, datetime(2028, 1, 2), datetime.today(), 45)
        self.assertIsNotNone(bottle.bottle_id)
        self.assertEqual(bottle.price, 45)
        self.assertFalse(bottle.drunk)

    def test_get_count_all_bottles(self):
        count = crud.get_count_all_bottles(self.lot.lot_id)
        self.assertEqual(count, 3)

    def test_get_count_drinkable_bottles(self):
        count = crud.get_count_drinkable_bottles(self.lot.lot_id)
        self.assertGreaterEqual(count, 1)

    def test_drink_earliest_drinkable_date_bottle(self):
        bottle = crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        self.assertIsNotNone(bottle)
        self.assertTrue(bottle.drunk)
        self.assertEqual(bottle.drinkable_date.year, 2024)

    def test_drink_bottle_returns_none_when_all_drunk(self):
        for _ in range(3):
            crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        result = crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        self.assertIsNone(result)


class TestTastingNoteCrud(BaseTestCase):

    def test_create_tasting_note(self):
        bottle = crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        note = crud.create_tasting_note(bottle, self.user, "Delicious!", datetime.today())
        self.assertIsNotNone(note.tasting_note_id)
        self.assertEqual(note.note, "Delicious!")

    def test_get_all_tasting_notes(self):
        bottle = crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        crud.create_tasting_note(bottle, self.user, "Note 1", datetime.today())
        crud.create_tasting_note(bottle, self.user, "Note 2", datetime.today())
        notes = crud.get_all_tasting_notes(self.lot.lot_id)
        self.assertEqual(len(notes), 2)


class TestFilterCrud(BaseTestCase):

    def test_filter_cellar_lots_by_varietal(self):
        results = crud.filter_cellar_lots("varietal", "Cabernet Sauvignon", self.user.cellar_id)
        self.assertGreaterEqual(len(results), 1)

    def test_filter_cellar_lots_invalid_attribute(self):
        results = crud.filter_cellar_lots("__class__", "anything", self.user.cellar_id)
        self.assertEqual(results, [])

    def test_filter_vineyard_info_by_country(self):
        results = crud.filter_cellar_lots_on_vineyard_info("country", "France", self.user.cellar_id)
        self.assertGreaterEqual(len(results), 1)

    def test_filter_vineyard_info_invalid_attribute(self):
        results = crud.filter_cellar_lots_on_vineyard_info("password", "anything", self.user.cellar_id)
        self.assertEqual(results, [])

    def test_search_cellar_by_wine_name(self):
        results = crud.get_lots_by_search_term(self.user.cellar_id, "Test")
        self.assertGreaterEqual(len(results), 1)

    def test_search_cellar_no_results(self):
        results = crud.get_lots_by_search_term(self.user.cellar_id, "zzzznotfound")
        self.assertEqual(len(results), 0)


# ---------------------------------------------------------------------------
# Route Integration Tests
# ---------------------------------------------------------------------------

class TestPublicRoutes(BaseTestCase):

    def test_homepage_returns_200(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_login_with_valid_creds(self):
        res = self.client.post("/login", data={
            "email": "test@test.com",
            "password": "password",
        }, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/cellar", res.headers["Location"])

    def test_login_with_bad_password(self):
        res = self.client.post("/login", data={
            "email": "test@test.com",
            "password": "wrong",
        }, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertNotIn("/cellar", res.headers["Location"])

    def test_login_with_unknown_email(self):
        res = self.client.post("/login", data={
            "email": "nobody@test.com",
            "password": "password",
        }, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertNotIn("/cellar", res.headers["Location"])

    def test_demo_login(self):
        """Demo login only works if user0@test.com is seeded; here we test the form key is accepted."""
        res = self.client.post("/login", data={"demo": "true"}, follow_redirects=False)
        self.assertIn(res.status_code, [302])


class TestAuthGuard(BaseTestCase):

    def test_cellar_requires_login(self):
        res = self.client.get("/cellar", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/", res.headers["Location"])

    def test_add_to_cellar_requires_login(self):
        res = self.client.get("/add_to_cellar", follow_redirects=False)
        self.assertEqual(res.status_code, 302)

    def test_lots_requires_login(self):
        res = self.client.get("/lots/1", follow_redirects=False)
        self.assertEqual(res.status_code, 302)

    def test_filter_requires_login(self):
        res = self.client.get("/filter_cellar?filter_on=varietal&filter_val=Merlot", follow_redirects=False)
        self.assertEqual(res.status_code, 302)

    def test_vineyards_requires_login(self):
        res = self.client.get("/vineyards", follow_redirects=False)
        self.assertEqual(res.status_code, 302)


class TestProtectedRoutes(BaseTestCase):

    def test_cellar_returns_200(self):
        self.login()
        res = self.client.get("/cellar")
        self.assertEqual(res.status_code, 200)

    def test_show_lot_returns_200(self):
        self.login()
        res = self.client.get(f"/lots/{self.lot.lot_id}")
        self.assertEqual(res.status_code, 200)

    def test_show_lot_not_found(self):
        self.login()
        res = self.client.get("/lots/99999")
        self.assertEqual(res.status_code, 404)

    def test_drink_bottle_redirects_on_no_bottles(self):
        self.login()
        for _ in range(3):
            crud.drink_earliest_drinkable_date_bottle(self.lot.lot_id)
        res = self.client.get(f"/drink/{self.lot.lot_id}", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn(f"/lots/{self.lot.lot_id}", res.headers["Location"])

    def test_add_to_cellar_returns_200(self):
        self.login()
        res = self.client.get("/add_to_cellar")
        self.assertEqual(res.status_code, 200)

    def test_edit_vineyard_not_found(self):
        self.login()
        res = self.client.get("/edit_vineyard/99999")
        self.assertEqual(res.status_code, 404)

    def test_undo_drink_not_found(self):
        self.login()
        res = self.client.post("/undo_drink_bottle/99999")
        self.assertEqual(res.status_code, 404)

    def test_create_tasting_note_bottle_not_found(self):
        self.login()
        res = self.client.post("/create_tasting_note/99999", data={"note": "test"})
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
