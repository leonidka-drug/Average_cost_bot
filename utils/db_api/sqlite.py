import sqlite3
from sqlite3 import Cursor


class Database:
    def __init__(self, database_file: str):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self) -> list:
        with self.connection:
            return self.cursor.execute('SELECT * FROM "users"').fetchall()

    def get_entry(self,
                  table: str,
                  parameter: str,
                  value: [str, int]) -> tuple:
        with self.connection:
            return self.cursor.execute(
                f'SELECT * FROM "{table}"  WHERE "{parameter}" = ?',
                (value,)
            ).fetchone()

    def delete_entry(self,
                     table: str,
                     parameter: str,
                     value: [str, int]) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                f'DELETE FROM "{table}" WHERE "{parameter}" = ?',
                (value,)
            )

    def user_exists(self, telegram_id: [str, int]) -> bool:
        with self.connection:
            result = self.cursor.execute(
                'SELECT * FROM "users" WHERE "tg_id" = ?',
                (telegram_id,)
            ).fetchall()
            return bool(len(result))

    def get_subscriptions(self, status: bool = True) -> list:
        with self.connection:
            return self.cursor.execute(
                'SELECT * FROM "users" WHERE "sub_status" = ?',
                (status,)
            ).fetchall()

    def add_user(self,
                 telegram_id: [str, int],
                 sub_status: bool = False) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                'INSERT INTO "users" ("tg_id", "sub_status") VALUES (?, ?)',
                (telegram_id, sub_status)
            )

    def update_user_subscription(self,
                                 telegram_id: [str, int],
                                 status: bool = True) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                'UPDATE "users" SET "sub_status" = ? WHERE "tg_id" = ?',
                (status, telegram_id)
            )

    def add_hotel(
            self,
            telegram_id: [str, int],
            hotel_name: str,
            number_of_rooms: int,
            address: str = None
    ) -> Cursor:
        with self.connection:
            user_id = self.get_entry("users", "tg_id", telegram_id)[0]
            return self.cursor.execute(
                '''INSERT INTO "hotels" 
                ("user_id", "name", "num_of_rooms", "address") 
                VALUES (?, ?, ?, ?)''',
                (user_id, hotel_name, number_of_rooms, address)
            )

    def add_seasons_info(
            self,
            telegram_id: [str, int],
            desired_total_profit: float,
            google_sheet_id: str
    ) -> Cursor:
        with self.connection:
            user_id = self.get_entry("users", "tg_id", telegram_id)[0]
            hotel_id = self.get_entry("hotels", "user_id", user_id)[0]
            return self.cursor.execute(
                '''INSERT INTO "season_info" 
                ("hotel_id", "desired_total_profit", "google_sheet_id")
                VALUES (?, ?, ?)''',
                (hotel_id, desired_total_profit, google_sheet_id)
            )
