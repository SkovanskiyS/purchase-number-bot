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
                username VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255),
                language VARCHAR(255) DEFAULT 'not_chosen',
                registered_at TIMESTAMP DEFAULT NOW(),
                blocked INTEGER DEFAULT 0 NOT NULL)
                """
            )

    def insert_user(self, telegram_id, username, first_name, last_name, language):
        with self.connection.cursor() as cursor:
            print(telegram_id)
            cursor.execute(
                """
                INSERT INTO botUsers (user_id, username, first_name, last_name,language) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (telegram_id, username, first_name, last_name, language)
            )

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
                (new_language,user_id,)
            )

