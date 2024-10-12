import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor

import termtables as tt


def search(cursor, user, name=""):
    cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{user}\" AND Name=\"Anderson\"")
    records = cursor.fetchall()
    return records

def get_cols(cursor):
    cursor.execute(f"DESCRIBE LIBMAN.USERS")
    cols = cursor.fetchall()
    return [col[0] for col in cols]

if __name__ == "__main__":
    connection = Connection(user="anderson", password="Anderson#7", database="LIBMAN")
    cursor = connection.cursor(cursor=Cursor)

    records = search(cursor, "USER8774")
    cols = get_cols(cursor)

    print(f"\nType: {type(records)}, Length: {len(records)}")

    print(f"\nRecords = {records}")

    text = tt.to_string(records, cols)

    print(text)

