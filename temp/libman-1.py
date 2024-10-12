"""
                    Library Management System:
    
    Author: Howard Anderson.

    Date: 17/06/2024.

    Description: Library Management System.

    Filename: libman.py.

"""

from pymysql.connections import Connection
from pymysql.cursors import Cursor

import random

class Entity:
       
    def __init__(self, name: str, uid: str, date: str) -> None:
        self.__name = name
        self.__uid = uid
        self.__date_of_join = date

    
    def get_name(self) -> str:
        return self.__name
    
    def get_uid(self) -> str:
        return self.__uid
    
    def get_date(self) -> str:
        return self.__date_of_join


class Book(Entity):

    def __init__(self, name: str, uid: str, author: str, date: str) -> None:
        super().__init__(name, uid, date)
        self.__borrowable: bool = True

    def borrow(self) -> bool:
        self.__borrowable =  False
        return True


class User(Entity):

    def __init__(self, name: str, uid: str, date: str, phone: str) -> None:
        super().__init__(name, uid, date)
        self.__phone_number: str = phone

    def get_phone(self, phone: str) -> bool:
        self.__phone_number = phone
        return True
        

class Library:

    def __init__(self, connection: Connection) -> None:
        self.__borrow_limit: int = None
        self.__connection = connection
    
    def add_user(self) -> User:
        cursor = self.__connection.cursor(cursor=Cursor)
        name = input("\n[ # ]: Name of the User: ")
        uid = "US" + str(random.randint(0, 10000))
        date = input("\n[ # ]: Date: ")
        phone_number = input("\n[ # ]: Enter Phone Number: ")

        user = User(name, uid, date, phone_number)

        cursor.execute(f"INSERT INTO USER(UID, Name, Date_Join, Phone_Number) VALUES({uid}, {name}, {date}, {phone_number})")
        self.__connection.commit()
        cursor.close()

        return user
    
    def add_book(self) -> Book:
        cursor = self.__connection.cursor(cursor=Cursor)
        name = input("\n[ # ]: Name of the Book: ")
        author = input("\n[ # ]: Author: ")
        uid = "BOOK" + str(random.randint(0, 10000))
        date = input("\n[ # ]: Date: ")

        book = Book(name, uid, author, date)

        cursor.execute(f"INSERT INTO BOOKS(UID, Name, Author, Date_Purchase, Borrow_Status) VALUES({uid}, {name}, {author}, {date}, \"NEW\")")
        self.__connection.commit()
        cursor.close()

        return book
    
    def update_borrow_limit(self, limit) -> None:
        self.__borrow_limit = limit
    

    

