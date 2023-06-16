import sqlite3

class Database:
    def __init__(self,path_to_db="data/main.db"):
         self.path_to_db = path_to_db
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self,sql:str,parameters:tuple=None,fetchone=False,fetchall=False,commit=False):
        if not parameters:
            parameters = tuple()
        data=None
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql,parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_user(self):
        sql = """
        CREATE TABLE Users (
        id int not null,
        username varchar(255),
        Name varchar(255),
        phone varchar(255),
        blocked INTEGER DEFAULT "0" NOT NULL,
        PRIMARY KEY (id)
        )
        """
        self.execute(sql,commit=True)

    def add_user(self,id:int,fullname:str,phone:str=None,username:str=None):
        sql = "INSERT INTO Users(id,Name,phone,username) VALUES(?,?,?,?)"
        parameters = (id,fullname,phone,username)
        self.execute(sql,parameters = parameters,commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql,fetchall=True)

    def delete_users(self):
        self.execute("DELETE FROM Users",commit=True)

    def update_name(self,name,id):
        sql = 'UPDATE Users SET Name=? WHERE id=?'
        return self.execute(sql,parameters=(name,id),commit=True)

    def update_phone(self,number,id):
        return self.execute('UPDATE Users SET phone=? WHERE id=?',parameters=(number,id),commit=True)

    def user_is_exist(self,id):
        sql = "SELECT id FROM Users WHERE id=?"
        return self.execute(sql, (id,), fetchone=True)

    def select_user(self,id):
        sql = "SELECT * FROM Users WHERE id=?"
        return self.execute(sql,(id,),fetchone=True)

    def select_user_id(self):
        sql = "SELECT id FROM Users"
        return self.execute(sql, fetchall=True)

    def get_white_list(self,id):
        sql = 'SELECT blocked FROM Users WHERE id=?'
        return self.execute(sql,parameters=(id,),fetchone=True,commit=True)
