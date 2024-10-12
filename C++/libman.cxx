/*
                    Library Management System
    
    Author: Howard Anderson.

    Date: 16/06/2024.

    Description: Library Management System.

    Filename: libman.cxx
*/

#include "libman.hpp"

// Class User:

User::User(std::string name, std::string uid, std::string date) {
    _name = name;
    _uid = uid;
    _date = date;
}

bool User::borrow(Book book) {
    borrowed_books.push_back(book);
    return true;
}

// Class Book:

Book::Book(std::string name, std::string uid, std::string date) {
    _name = name;
    _uid = uid;
    _date = date;
}

bool Book::borrow() {
    borrowable = false;
    return true;
}

// Class Library:

Library::Library() {}

User Library::add_user() {
    std::string name, uid, date;
    std::cout << "\n[ # ]: Enter Name of the User: ";
    std::cin >> name;
    uid = "US1234567";
    std::cout << "\n[ # ]: Enter the Date: ";
    std::cin >> date;

    User user = User(name, uid, date);
    users.push_back(user);

    return user;
}

Book Library::add_book() {
    std::string name, uid, date;
    std::cout << "\n[ # ]: Enter Name of the Book: ";
    std::cin >> name;
    uid = "BOOK1234";
    std::cout << "\n[ # ]: Enter the Date: ";
    std::cin >> date;

    Book book = Book(name, uid, date);
    books.push_back(book);

    return book;
}



