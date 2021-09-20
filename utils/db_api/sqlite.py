import sqlite3


class Database:
    def __init__(self, database_file: str):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def user_exists(self, telegram_id: str):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `tg_id` = ?",
                (telegram_id,)
            ).fetchall()
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
