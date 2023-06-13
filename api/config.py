from api.db import DatabaseConnection


# set database database credentials
host = "localhost"
databasename = "scoreboard_tennis"
user = "root"
password = "1wj0D3Hnj^"
port = 3306
MySqlDatabase = DatabaseConnection(host, databasename, user, password, port)

class AppConfig:
    SECRET_KEY = 'your-secret-key' # Change it
    JSON_SORT_KEYS = False

    # JWT Authentication
    JWT_SECRET_KEY = SECRET_KEY
    
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


    # Google Email Configuration 
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True

    # MAIL_USERNAME = 'developercodeaza@gmail.com'
    # MAIL_PASSWORD = 'zsnsvlvninoizjzs'
    