import mysql.connector as connection
import mysql.connector
from mysql.connector import Error
import logging
from flask_mysqldb import MySQL
import MySQLdb.cursors
from sqlalchemy import create_engine
logging.basicConfig(filename='loginfo.log', level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s  %(message)s')
class database:
    @staticmethod
    def create_database_connection():
        connection = None
        try:
            connection = mysql.connector.connect(host="localhost", database = 'youtube_scraper',user="root", passwd="root",use_pure=True)
            print("MySQL Database connection successful")
        except Error as err:
            logging.exception(err)
            print(f"Error: '{err}'")

        return connection
    @staticmethod
    def execute_query(conn, query):
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully...")
        except Error as err:
            print(f"Error: '{err}'")

    @staticmethod
    def read_query(connection, query):
       cursor = connection.cursor()
       result = None
       try:
           cursor.execute(query)
           result = cursor.fetchall()
           return result
       except Error as err:
           print(f"Error: '{err}'")


@staticmethod
def insert_query(conn, query):
    cursor = conn.cursor()
    try:
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                               .format(user="root",
                                       pw="root",
                                       db="youtube_scraper"))
        query.to_sql('youtube', con=engine, if_exists='append', chunksize=1000, index=False)
        conn.commit()
        print("Query executed successfully...")
    except Error as err:
        print(f"Error: '{err}'")


def add_data(title, content):
  try:
    # Connecting to database
    con = sql.connect('shot_database.db')
    # Getting cursor
    c =  con.cursor()
    # Adding data
    c.execute("INSERT INTO Shots (title, content) VALUES (%s, %s)" %(title, content))
    # Applying changes
    con.commit()
  except:
    print("An error has occured")