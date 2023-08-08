import logging
import psycopg2

from data.config import Config, load_config


class DB_API_ADMIN:
    config: Config = load_config('.env')

    def __init__(self):
        self.host = self.config.db.db_host
        self.user = self.config.db.db_user
        self.password = self.config.db.db_password
        self.database = self.config.db.database
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.connection.autocommit = True
        except Exception as err:
            logging.info(str(err))

    def get_all_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM botusers
                """
            )
            return cursor.fetchall()

    def get_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * from botusers WHERE user_id=%s
                """,
                (user_id,)
            )
            return cursor.fetchone()

    def check_referral(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id FROM botusers WHERE referral=
                (SELECT id FROM botusers WHERE user_id=%s)
                """,
                (user_id,)
            )
            return cursor.fetchall()

    def block_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET blocked=1 WHERE user_id=%s
                """,
                (user_id,)
            )

    def unblock_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET blocked=0 WHERE user_id=%s
                """,
                (user_id,)
            )

    def change_bonus(self, bonus_count, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET bonus=%s WHERE user_id=%s
                """,
                (bonus_count, user_id,)
            )

    def delete_user(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM botusers WHERE user_id = %s
                """,
                (user_id,)
            )

    def get_user_id(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id FROM botusers
                """
            )
            return cursor.fetchall()

    def get_balance(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT balance FROM botusers WHERE user_id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()

    def update_balance(self, user_id, money):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET balance = %s WHERE user_id = %s
                """, (money, user_id)
            )
