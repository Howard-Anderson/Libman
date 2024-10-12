/*
                    Library Management System
    
    Author: Howard Anderson.

    Date: 16/06/2024.

    Description: Library Management System.

    Filename: libman.cxx
*/

#ifndef __LIBMAN__

#define __LIBMAN__ 

#include <iostream>
#include <string>
#include <vector>

class Entity {

    protected:
        std::string _name;
        std::string _uid;
        std::string _date;

    public:

        Entity();

        Entity(std::string name, std::string uid, std::string date);

        std::string getname();

        std::string getuid();

        std::string getdate();

};

class Book: public Entity {

    bool borrowable;
    
    public:
        
        Book(std::string name, std::string uid, std::string date);

        bool borrow();

};

class User: public Entity {

    std::vector<Book> borrowed_books;

    public:

        User(std::string name, std::string uid, std::string date);

        bool borrow(Book book);

};

class Library {

    std::vector<User> users;
    std::vector<Book> books;

    public:

        Library();

        User add_user();

        Book add_book();

};

#endif 
