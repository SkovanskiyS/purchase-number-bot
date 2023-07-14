import logging
import psycopg2

from data.config import Config, load_config


class DB_API:
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

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS botUsers(
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL UNIQUE,
                username VARCHAR(255),
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255),
                language VARCHAR(255) DEFAULT 'ru',
                registered_at TIMESTAMP DEFAULT NOW(),
                bonus INTEGER DEFAULT 0 NOT NULL,
                referral INTEGER,
                blocked INTEGER DEFAULT 0 NOT NULL,
                page INTEGER DEFAULT 0 NOT NULL)
                """
            )

    def insert_user(self, telegram_id, username, first_name, last_name, referral=None):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO botUsers (user_id, username, first_name, last_name,referral) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (telegram_id, username, first_name, last_name, referral)
            )

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

    def user_exists(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id FROM botUsers WHERE user_id = %s
                """,
                (user_id,)
            )
            user_exists = cursor.fetchone() is not None
            return user_exists

    def get_current_language(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT language FROM botUsers WHERE user_id = %s
                """,
                (user_id,)
            )

            return cursor.fetchone()

    def change_language(self, user_id, new_language):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botUsers SET language = %s WHERE user_id = %s
                """,
                (new_language, user_id,)
            )

    def get_current_page(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT page FROM botusers WHERE user_id = %s
                """,
                (user_id,)
            )

            return cursor.fetchone()

    def update_page(self, user_id, page):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET page = %s WHERE user_id = %s
                """,
                (page, user_id,)
            )

    def get_all_info(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * from botusers WHERE user_id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()

    def get_user_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id from botusers WHERE user_id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()

    def get_all_banned_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id from botusers WHERE blocked = 1
                """
            )
            return cursor.fetchall()

    def get_bonus(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT bonus from botusers WHERE user_id = %s
                """,
                (user_id,)
            )
            return cursor.fetchone()

    def update_bonus(self, amount, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET bonus = %s WHERE user_id = %s
                """,
                (amount, user_id,)
            )

    def clear_referral_number(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE botusers SET referral = null  WHERE user_id = %s
                """,
                (user_id,)
            )