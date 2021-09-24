import unittest
from random import randint, choice
from sqlite3 import Cursor

from utils.db_api.sqlite import Database

db = Database("tests/testing_data/testing_db.db")


class TestSqlite(unittest.TestCase):
    def test_get_user(self):
        self.assertEqual(type(db.get_users()), list)

    def test_get_entry(self):
        tg_id = choice((1481133443, 2672748391, 8533143892,
                        "9769996101", "4445777978"))

        self.assertEqual(type(db.get_entry("users", "tg_id", tg_id)), tuple)
        self.assertEqual(len(db.get_entry("users", "tg_id", tg_id)), 3)

        self.assertEqual(type(db.get_entry("users", "tg_id", tg_id)[0]), int)
        self.assertEqual(type(db.get_entry("users", "tg_id", tg_id)[1]), str)
        self.assertEqual(type(db.get_entry("users", "tg_id", tg_id)[2]), int)

        self.assertEqual(db.get_entry("users", "tg_id", "464696049")[0], 1)
        self.assertEqual(db.get_entry("users", "tg_id", 464696049)[0], 1)

        self.assertFalse(db.get_entry("users", "tg_id", 464696049)[2])
        self.assertTrue(db.get_entry("users", "tg_id", "9769996101")[2])

    def test_user_exists(self):
        self.assertEqual(type(db.user_exists(34)), bool)

        self.assertTrue(db.user_exists("464696049"))
        self.assertFalse(db.user_exists(12))

    def test_get_subscriptions(self):
        subs = db.get_subscriptions(True)
        not_subs = db.get_subscriptions(False)

        self.assertEqual(type(subs), list)
        self.assertEqual(type(not_subs), list)

        self.assertEqual(type(subs[0]), tuple)
        self.assertEqual(type(not_subs[0]), tuple)

        self.assertEqual(len(subs[0]), 3)
        self.assertEqual(len(not_subs[0]), 3)
        self.assertEqual(len(subs[1]), 3)
        self.assertEqual(len(not_subs[1]), 3)

        self.assertGreaterEqual(len(not_subs), 2)

        self.assertNotIn(subs, not_subs)
        self.assertNotIn(not_subs, subs)

    def test_add_user_and_delete_entry(self):
        rand_id = randint(100, 10000000000)

        db.add_user(rand_id, True)
        self.assertTrue(db.user_exists(rand_id))

        db.delete_entry("users", "tg_id", rand_id)
        self.assertFalse(db.user_exists(rand_id))

    def test_update_user_subscription(self):
        db.update_user_subscription(5454054520, True)
        self.assertIsInstance(db.update_user_subscription(5454054520, False),
                              Cursor)
        self.assertTrue(db.get_entry("users", "tg_id", 5454054520))

    def test_add_hotel(self):
        random_user = choice(db.get_users())
        telegram_id = random_user[1]
        words = (("first ", "second ", "third "), ("big ", "small "),
                 ("rare ", "common "),
                 ("hotel", "guest house", "hostel", "motel"))
        random_hotel_name = ""
        for counter in (0, 1, 2, 3):
            random_hotel_name += choice(words[counter])
        self.assertIsInstance(db.add_hotel(telegram_id,
                                           random_hotel_name,
                                           randint(5, 15),
                                           "Сочи, Озёрная 15"), Cursor)
        self.assertEqual(db.get_entry("hotels", "user_id", random_user[0])[2],
                         random_hotel_name)


if __name__ == '__main__':
    unittest.main()
