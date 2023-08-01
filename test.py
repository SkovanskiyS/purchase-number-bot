from database.admin_panel import DB_API_ADMIN

db = DB_API_ADMIN()
db.connect()
a = db.get_all_users()
