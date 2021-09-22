import unittest
from random import randint
from sqlite3 import Cursor

from utils.db_api.sqlite import Database

db = Database("tests/testing_data/testing_db.db")


class TestSqlite(unittest.TestCase):
    def test_get_user(self):
        self.assertEqual(type(db.get_users()), list)

    def test_get_object_id(self):
        self.assertEqual(db.get_object_id("users", "tg_id", "464696049"), 1)
        self.assertEqual(type(db.get_object_id("users", "tg_id", "464696049")),
                         int)
        self.assertEqual(db.get_object_id("users", "tg_id", 464696049), 1)

    def test_user_exists(self):
        self.assertEqual(db.user_exists("464696049"), 1)
        self.assertEqual(db.user_exists(12), False)

    def test_get_subscriptions(self):
        subs = db.get_subscriptions(True)
        not_subs = db.get_subscriptions(False)

        self.assertEqual(type(subs), list)
        self.assertEqual(type(not_subs), list)

        self.assertEqual(type(subs[0]), tuple)
        self.assertEqual(type(not_subs[0]), tuple)

        self.assertEqual(len(subs[0]), 3)
        self.assertEqual(len(not_subs[0]), 3)

        self.assertGreaterEqual(len(not_subs), 2)

        self.assertNotIn(subs, not_subs)
        self.assertNotIn(not_subs, subs)

    def test_add_user(self):
        rand_id = randint(100, 10000000000)
        db.add_user(rand_id, True)
        self.assertEqual(db.user_exists(rand_id), True)

    def test_update_user_subscription(self):
        self.assertIsInstance(db.update_user_subscription(5454054520, False),
                              Cursor)


if __name__ == '__main__':
    unittest.main()
