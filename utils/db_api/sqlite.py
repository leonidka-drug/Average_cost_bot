import sqlite3


class Database:
    def __init__(self, database_file: str):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    # def get_users(self):
    #     with self.connection:
    #         return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def get_object_id(self, table: str, parameter: str, value: str):
        with self.connection:
            return self.cursor.execute(
                "SELECT `id` FROM `?` WHERE `?` = ?",
                (table, parameter, value)
            ).fetchone()

    def user_exists(self, telegram_id: str):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `tg_id` = ?",
                (telegram_id,)
            ).fetchone()
            return bool(len(result))

    def get_subscriptions(self, status: bool = True):
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM `users` WHERE `sub_status` = ?",
                (status,)
            ).fetchall()

    def add_user(self, telegram_id: str, sub_status: bool = False):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `users` (`tg_id`, `sub_status`) VALUES (?, ?)",
                (telegram_id, sub_status)
            )

    def update_user_subscription(self, telegram_id: str, status: bool = True):
        with self.connection:
            return self.cursor.execute(
                "UPDATE `users` SET `sub_status` = ? WHERE `tg_id` = ?",
                (status, telegram_id)
            )

    def add_hotel(
            self,
            telegram_id: str,
            hotel_name: str,
            number_of_rooms: int,
            address: str = None
    ):
        with self.connection:
            user_id = self.get_object_id("users", "tg_id", telegram_id)
            return self.cursor.execute(
                "INSERT INTO `hotels` \
                (`user_id`, `name`, `num_of_rooms`, `address`) \
                VALUES (?, ?, ?, ?)",
                (user_id, hotel_name, number_of_rooms, address)
            )

    def add_seasons_info(
            self,
            telegram_id: str,
            desired_total_profit: float
    ):
        with self.connection:
            user_id = self.get_object_id("users", "tg_id", telegram_id)
            hotel_id = self.get_object_id("hotels", "user_id", user_id)
            return self.cursor.execute(
                "INSERT INTO `season_info` \
                (`hotel_id`, `desired_total_profit`) VALUES (?, ?)",
                (hotel_id, desired_total_profit)
            )

    def add_google_sheets_info(
            self,
            telegram_id: str,
            google_sheet_id: str,
            google_sheet_range: str
    ):
        with self.connection:
            user_id = self.get_object_id("users", "tg_id", telegram_id)
            hotel_id = self.get_object_id("hotels", "user_id", user_id)
            season_id = self.get_object_id("seasons_info", "hotel_id", hotel_id)
            return self.cursor.execute(
                "INSERT INTO `google_sheets_info` \
                (`season_id`, `google_sheet_id`, google_sheet_range`) \
                VALUES (?, ?, ?)",
                (season_id, google_sheet_id, google_sheet_range)
            )
