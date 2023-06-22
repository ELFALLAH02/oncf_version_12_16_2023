import mysql.connector

def connect_to_database():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            #password="12345678",
            database="movits"
        )
        cursor = mydb.cursor()
        
        return mydb, cursor

    except mysql.connector.Error as error:
        print(f"Error connecting to the database: {error}")
        return None, None
