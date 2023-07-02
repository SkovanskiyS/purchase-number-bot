import psycopg2
from data.config import Config, load_config


class DB_API:
    config: Config = load_config('.env')

    def __init__(self):
        self.host = self.config.db.db_host
        self.user = self.config.db.db_user
        self.password = self.config.db.db_password
        self.database = self.config.db.database
