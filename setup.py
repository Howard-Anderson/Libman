"""
                    Library Management System:
    
    Author: Howard Anderson.

    Date: 26/07/2024.

    Description: Library Management System.

    Filename: setup.py.

"""

# PyMySQL Imports:
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from pymysql import MySQLError

# Getpass Imports:
from getpass import getpass

# Json Imports:
import json


class Setup:
    """
        Setup the Libman Application in the System.
    """

    def __init__(self) -> None:
        """
            Constructor:
            Create a DB and create the required tables for LIBMAN.
        """
        
        params : dict = self.get_database_params()
        params["database"] = "LIBMAN"
        
        try:
            connection = Connection(user=params["username"], password=params["password"])
            connection.begin()
            cursor = connection.cursor(cursor=Cursor)
        
        except MySQLError:
            print(f"\n[ ! ]: Error while connecting to MySQL...")
            return
        
        try:
            cursor.execute(f"CREATE DATABASE {params["database"]}")
            cursor.execute(f"USE {params["database"]}")
            
        except MySQLError:
            print(f"\n[ ! ]: Error while Creating Database [{params["database"]}]...")
        
        try:
            self.create_tables(cursor)
            params = json.dumps(params, indent=4)
            with open("config.txt", "w") as config_file:
                config_file.write(params)
        
        finally:
            connection.commit()
            cursor.close()
            connection.close()
    
    def get_database_params(self) -> dict[str:str]:
        """
            Returns the Parameters to be passed to connect to the MySQL Database.
        """
        username = input("[ $ ]: Enter MySQL Username: ")
        password = getpass(prompt=f"[ $ ]: Enter Password for {username}: ")
        return {"username": username, "password": password}
    
    def create_tables(self, cursor: Cursor) -> bool:
        """
            Creates the Tables for the Libman Application.
            Tables:
                USERS, BOOKS, TRANSACTIONS.
        """
        try:
            cursor.execute("CREATE TABLE USERS(Unique_Value VARCHAR(10), Name VARCHAR(100), Age INT, Phone_Number VARCHAR(10), Join_Date VARCHAR(10))")
        
            cursor.execute("CREATE TABLE BOOKS(Unique_Value VARCHAR(10), Name VARCHAR(100), Author VARCHAR(100), Purchase_Date VARCHAR(10), Price INT, Borrow_Status VARCHAR(10))")
            
            cursor.execute("CREATE TABLE TRANSACTIONS(User_Unique VARCHAR(10), Book_Unique VARCHAR(10), Transaction_Date VARCHAR(10), Type VARCHAR(10))")
            
            return True
            
        except MySQLError:
            print(f"\n[ ! ]: Error on creating Tables in MySQL...")
            return False


if __name__ == "__main__":
    setup = Setup() 
    
    
