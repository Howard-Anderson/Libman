"""
                    Library Management System:
    
    Author: Howard Anderson.

    Date: 17/06/2024.

    Description: Library Management System.

    Filename: libman.py.

"""

# PyMySQL Imports:
from pymysql.connections import Connection
from pymysql.cursors import Cursor

# Termtable Imports:
import termtables as tt

# Random Imports:
import random


def get_cols(cursor, main_choice):
    # Get Column Names:
    cursor.execute(f"DESCRIBE LIBMAN.{main_choice}")
    cols = cursor.fetchall()
    col_names = [col[0] for col in cols]
    return col_names

def table(records, col_names):
    text = tt.to_string(
        records,
        header = col_names,
    #    style = tt.styles.ascii_thin_double
    )
    return text

def row_count(cursor: Cursor, main_choice) -> int:
    # Get Row Count:
    if main_choice != "TRANSACTIONS":
        cursor.execute(f"SELECT COUNT(unique_value) FROM {main_choice}")
    else:
        cursor.execute(f"SELECT COUNT(User_Unique) FROM {main_choice}")
    record_count = cursor.fetchall()
    #print(f"\nRecord Count: {record_count}")
    return record_count[0][0]


class Book:

    def __init__(self, cursor) -> None:
        self.__cursor = cursor

    def add(self, unique_value: str, name: str, author: str, purchase_date: str, price: int):
        self.__cursor.execute(f"INSERT INTO BOOKS(Unique_Value, Name, Author, Purchase_Date, Price, Borrow_Status) VALUES(\"{unique_value}\", \"{name}\", \"{author}\", \"{purchase_date}\", {price}, \"NEW\")")

    def update(self, unique_value: str, records: dict[str]) -> None:
        for key, value in records.items():
            if value != "":
                if key == "Price":
                    self.__cursor.execute(f"UPDATE BOOKS SET {key} = {value} WHERE Unique_Value=\"{unique_value}\"")
                else:
                    self.__cursor.execute(f"UPDATE BOOKS SET {key} = \"{value}\" WHERE Unique_value=\"{unique_value}\"")

    def search(self, unique_value: str, name: str) -> tuple[str]:
        if unique_value != "" and name != "":
            self.__cursor.execute(f"SELECT * FROM BOOKS WHERE Unique_Value=\"{unique_value}\", Name=\"{name}\"")

        elif unique_value != "":
            self.__cursor.execute(f"SELECT * FROM BOOKS WHERE Unique_Value=\"{unique_value}\"")

        else:
            self.__cursor.execute(f"SELECT * FROM BOOKS WHERE Name=\"{name}\"")

        record = self.__cursor.fetchall()
        return record

        
    def view(self):
        self.__cursor.execute(f"SELECT * FROM BOOKS")
        records = self.__cursor.fetchall()
        return records
    
    def remove(self, unique_value: str) -> None:
        self.__cursor.execute(f"DELETE FROM BOOKS WHERE Unique_Value=\"{unique_value}\"")
    
    def __del__(self):
        self.__cursor.close()


class User:

    def __init__(self, cursor) -> None:
        self.__cursor = cursor

    def add(self, unique_value: str, name: str, age: int, phone_number: str, join_date: str) -> None:
        self.__cursor.execute(f"INSERT INTO USERS(Unique_Value, Name, Age, Phone_Number, Join_Date) VALUES(\"{unique_value}\", \"{name}\", {age}, \"{phone_number}\", \"{join_date}\") ")

    
    def update(self, unique_value: str, records: dict[str: str]) -> None:
        for key, value in records.items():
            if value != "":
                if key == "Age":
                    self.__cursor.execute(f"UPDATE USERS SET {key}={value} WHERE Unique_Value=\"{unique_value}\"")
                else:
                    self.__cursor.execute(f"UPDATE USERS SET {key}=\"{value}\" WHERE Unique_Value=\"{unique_value}\"")
    
    def search(self, unique_value: str, name: str = "") -> tuple[str]:
        if unique_value != "" and name != "":
            self.__cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{unique_value}\" AND Name=\"{name}\"")

        elif unique_value != "":
            self.__cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{unique_value}\" ")

        else:
            self.self.__cursor.execute(f"SELECT * FROM USERS WHERE Name=\"{name}\"")
        #self.__cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{unique_value}\"")

        record = self.__cursor.fetchall()
        return record

    def view(self):
        self.__cursor.execute(f"SELECT * FROM USERS")
        records = self.__cursor.fetchall()
        return records
    
    def remove(self, unique_value: str) -> None:
        self.__cursor.execute(f"DELETE FROM USERS WHERE Unique_Value=\"{unique_value}\"")

    def __del__(self) -> None:
        self.__cursor.close()


class Transactions:

    def __init__(self, cursor) -> None:
        self.__cursor = cursor

    def transact(self, user_unique: str, book_unique: str, transaction_date: str, transaction_type: str) -> str:
        
        self.__cursor.execute(f"SELECT Borrow_Status FROM BOOKS WHERE Book_Unique=\"{book_unique}\"")
        book_status: tuple = self.__cursor.fetchall()
        
        # Check if the Book Exists:
        if book_status == ():
            return f"[{book_unique}]: Book is not found.."
        
        book_status: str = book_status[0] 
        
        if book_status == transaction_type:
            return f"[{book_unique}]: Book Status is already: {transaction_type}.."
        
        else:
            self.__cursor.execute(f"UPDATE BOOKS SET Borrow_Status=\"{transaction_type}\" WHERE Unique_Value=\"{book_unique}\"")
            self.__cursor.execute(f"INSERT INTO TRANSACTIONS(User_Unique, Book_Unique, Transaction_Date, Type) VALUES(\"{user_unique}\", \"{book_unique}\", \"{transaction_date}\", \"{transaction_type}\")")
            return f"[TRANSACTION]: [{user_unique}]:[{book_unique}] Added.."
        
    
    def update(self, user_unique: str, book_unique: str, transaction_date: str, transaction_type: str) -> None:
        if transaction_date != "":
            self.__cursor.execute(f"UPDATE TRANSACTIONS SET Transaction_Date=\"{transaction_date}\" WHERE User_Unique=\"{user_unique}\" AND Book_Unique=\"{book_unique}\"")
        
        if transaction_type != "":
            self.__cursor.execute(f"UPDATE TRANSACTIONS SET Type=\"{transaction_type}\" WHERE User_Unique=\"{user_unique}\" AND Book_Unique=\"{book_unique}\"")
            self.__cursor.execute(f"UPDATE BOOKS SET Borrow_Status=\"{transaction_type}\" WHERE Unique_Value=\"{book_unique}\"")

    def search(self, user_unique: str, book_unique: str) -> tuple:
        if user_unique != "" and book_unique != "":
            self.__cursor.execute(f"SELECT * FROM TRANSACTIONS WHERE User_Unique=\"{user_unique}\" AND Book_Unique=\"{book_unique}\"")
        
        elif user_unique != "":
            self.__cursor.execute(f"SELECT * FROM TRANSACTIONS WHERE User_Unique=\"{user_unique}\"")
        
        else:
            self.__cursor.execute(f"SELECT * FROM TRANSACTIONS WHERE Book_Unique=\"{book_unique}\"")

        return self.__cursor.fetchall()
    
    def view(self) -> tuple[tuple]:
        self.__cursor.execute(f"SELECT * FROM TRANSACTIONS")
        return self.__cursor.fetchall()
    
    def remove(self, user_unique: str, book_unique: str) -> None:
        self.__cursor.execute(f"DELETE FROM TRANSACTIONS WHERE User_Unique=\"{user_unique}\" AND Book_Unique=\"{book_unique}\"")
    
    def __del__(self):
        self.__cursor.close()



class Library:

    def __init__(self, connection: Connection) -> None:
        self.__connection = connection
        self.cursor = self.__connection.cursor(cursor=Cursor)
        self.user = User(self.cursor)
        self.book = Book(self.cursor)
        self.transactions = Transactions(self.cursor)
    
    def get_record_count(self, main_choice):
        return row_count(self.cursor, main_choice)

    # Add:
    def add(self, record: list[str], main_choice: str) -> str:
        unique_value: str = main_choice + str(random.randint(1, 10000))
        try:
            if main_choice == "USERS":
                record[1] = int(record[1]) # Age.
                self.user.add(unique_value=unique_value, name=record[0], age=record[1], phone_number=record[2], join_date=record[3])

            else:
                record[3] = int(record[3]) # Price.
                self.book.add(unique_value=unique_value, name=record[0], author=record[1], purchase_date=record[2], price=record[3])
            
            message: str  = f"[{main_choice}]: Added Record"
        
        except:
            
            message: str = f"[ERROR]: {main_choice} cannot be added"
        
        finally:
            self.__connection.commit()
            return message
        
    # Update:
    def update(self, args: list[str], main_choice: str) -> str:
        
        try:
            if main_choice == "USERS":
                unique_value = args.pop(0)
                record_names = ["Name", "Age", "Phone_Number", "Join_Date"]
                records = dict(zip(record_names, args))
                self.user.update(unique_value=unique_value,records=records)
            
            elif main_choice == "BOOKS":
                unique_value = args.pop(0)
                record_names = ["Name", "Author", "Purchase_Date", "Price", "Borrow_Status"]
                records = dict(zip(record_names, args))
                self.book.update(unique_value=unique_value, records = records)
            
            else:
                user_unique = args.pop(0)
                book_unique = args.pop(0)
                #print(f"\n{user_unique = }, {book_unique = }, {args[0] = }, {args[1] = }")
                self.transactions.update(user_unique=user_unique, book_unique=book_unique, transaction_date=args[0], transaction_type=args[1])
            
            message = f"[{main_choice}]: Updated Record Sucessfully"
        
        except:    
            message: str = f"[ERROR]: {main_choice} cannot be updated.."
        
        finally: 
            self.__connection.commit()
            return message
        
    # Search:
    def search(self, args: list[str], main_choice: str) -> str:
        if main_choice == "USERS":
            records = self.user.search(args[0], args[1])
        
        elif main_choice == "BOOKS":
            records = self.book.search(args[0], args[1])
        
        else:
            records = self.transactions.search(args[0], args[1])
        
        col_names = get_cols(self.cursor, main_choice)
        
        try:
            table_text = table(records, col_names)
        except:
            table_text = f"No Results Found.."
        
        return table_text 
    
    def update_search(self, args: list[str], main_choice: str) -> tuple[str]:
        if main_choice == "USERS":
            records = self.user.search(args[0], args[1])
        
        elif main_choice == "BOOKS":
            records = self.book.search(args[0], args[1])
        
        else:
            records = self.transactions.search(args[0], args[1])
        
        return records
        

    # View:
    def view(self, start: int, end: int, main_choice: str) -> str:
        if main_choice == "USERS":
            records = self.user.view()
        
        elif main_choice == "BOOKS":
            records = self.book.view()
        
        else: 
            records = self.transactions.view()

        try:
            col_names = get_cols(self.cursor, main_choice)
            records = records[start: end]
            text = table(records, col_names) 
            return text
        
        except:
            return f"[{main_choice}]: No records found..."
        
    
    # Make Transaction:
    def transact(self, record: list[str]) -> str:
        try:
            message = self.transactions.transact(user_unique=record[0], book_unique=record[1], transaction_date=record[2], transaction_type=record[3])
            
        except:
            message = f"[ERROR]: TRANSACTION couldn't be added"
        
        finally:
            self.__connection.commit()
            return message
    
    # Remove:
    def remove(self, args: list[str], main_choice: str) -> str:
        try:
            if main_choice == "TRANSACTIONS":
                self.transactions.remove(user_unique=args[0], book_unique=args[1])
                message: str = f"[{main_choice}]: {args[0]} : {args[1]} has been removed"
                
            
            else:
                if main_choice == "USERS":
                    self.user.remove(unique_value=args[0])
                
                else:
                    self.book.remove(unique_value=args[0])
                
                message: str = f"[{main_choice}]: {args[0]} has been removed"
        
        except:    
            if main_choice == "TRANSACTIONS":
                message: str = f"[ERROR]: {args[0]} : {args[1]} couldn't be removed"
            
            else:
                message: str = f"[ERROR]: {args[0]} couldn't be removed"

        finally:
            self.__connection.commit()
            return message


if __name__ == "__main__":
    connection = Connection(user="anderson", password="Anderson#7", database="LIBMAN")
    library = Library(connection)
    cursor = connection.cursor(cursor=Cursor)
    user = User(cursor)
    args = ("USER8774", "Anderson")

    #print(f"\nSearch: {user.search(args[0], args[1])}")
    #print(f"\nLibrary: {library.search(args, "USERS")}")
    #cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{args[0]}\"")
    #cursor.execute(f"SELECT * FROM USERS WHERE Unique_Value=\"{args[0]}\" AND Name=\"{args[1]}\"")
    #record = cursor.fetchall()
    #print(f"\nRecord: {record}")
    #cursor.execute(f"{library.remove(["USER2", "BOOK100"], "TRANSACTIONS")}")
    # user_unique, book_unique = "USER2", "BOOKS100"
    # cursor.execute(f"DELETE FROM TRANSACTIONS WHERE User_Unique=\"{user_unique}\" AND Book_Unique=\"{book_unique}\"")
    # connection.commit()
    #args = ["USER2", "BOOKS1835", "07/09/2024", "TEST-2"]
    #print(f"\nUpdate: {library.update(args=args, main_choice="TRANSACTIONS")}")

