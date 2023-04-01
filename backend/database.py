import psycopg2
import os

def getDatatbase():
    try:
        conn = psycopg2.connect(database=os.getenv("DB_NAME"),
                                user=os.getenv("DB_USER"),
                                password=os.getenv("DB_PASS"),
                                host=os.getenv("DB_HOST"),
                                port=os.getenv("DB_PORT"))
        print("Database connected successfully")
        if (conn == None):
            print("Error: psycopg2.connect() returned a None object")
            return None
        #cursor = conn.cursor()
        #return cursor
        return conn

    except Exception as e:
        print("Database not connected successfully")
        print(e)

    try:
        print('h')

    except:
        pass
