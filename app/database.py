# app/database.py

import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='sgpp',
        cursorclass=pymysql.cursors.DictCursor  
    )