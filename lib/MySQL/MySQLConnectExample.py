""" Module: Example to initial a connnection to MySQL database.

    Learning source: http://www.mysqltutorial.org/python-connecting-mysql-databases/
"""

import MySQLdb as mdb
from ReadConfig import ReadMySQLConfig


def connect_excplict():
    """ Connect to MySQL database by passing explicit database settings to the curosr."""
    try:
        conn = mdb.connect(host='localhost',
                           db='mysql',
                           user='root',
                           passwd='Tonkay2819')
        print("Connected to MySQL database")

    except mdb.Error as e:
        print(e)

    finally:
        conn.close()

def connect():
    """ Connect to MySQL database by loading database setttings from config.ini. """

    # Load configurations
    db_config = ReadMySQLConfig()

    try:
        print("Connecting to MySQL database...")
        conn = mdb.connection(**db_config)
        print('connection established.')
        
    except mdb.Error as e:
        print(e)

    finally:
        conn.close()
        print('connection closed.')



if __name__ == '__main__':
    connect()
