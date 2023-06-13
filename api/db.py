import mysql.connector

# class to handle data base query and connect to the mysql
class DatabaseConnection():

    def __init__(self,host,databasename,user,password,port):
        self.host = host
        self.databasename=databasename
        self.user=user
        self.password=password
        self.port=port

    # function to get a fresh cursor and database object
    def connection(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            charset='utf8mb4',
            database=self.databasename,
        )

        if db.is_connected():
            print("You're connected to database!")
        else:
            print("Error Connection!")
        cursor = db.cursor(buffered=True,dictionary=True)
        return cursor, db

    # close the connection using cursor and database object created
    def close_connection(self, cursor, db):
        cursor.close()
        db.close()
        if not db.is_connected():
            print("MySQL connection is closed")
        else:
            print("Connection is not closed Successfully!")

