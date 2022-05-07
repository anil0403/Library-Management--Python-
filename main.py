# Program requirements!
# MySQL Server and Python Connector
# DataFrame of Pandas lib
# Os module
# Python core programming
import os
import pandas as pd
import mysql.connector
# connecting to my sql server !
try:
    conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '0080452H',
    port = 3306
    )
    if(conn.is_connected()):
            # print("Connection Successfull to MySQL Server")
        pass
    
except:
    # print("Connection unsuccessful to MySQL Server")
    pass
#
# creating a database
try:
    myc = conn.cursor()
    sql = 'CREATE DATABASE library'
    myc.execute(sql)
    myc.close()
    # print("Successful")
except:
    pass # database already created
#
# configuration file for connecting to database (global declaration)
config = {
    'host':"localhost",
    'user':"root",
    'password':"0080452H",
    'database' : 'library', 
    'port' : 3306
}
#
# creating user table
try:
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'CREATE TABLE user(user_id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(30) NOT NULL, dob DATE NOT NULL, address TEXT NOT NULL , created DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'
    myc.execute(sql)
    sql = 'ALTER TABLE user AUTO_INCREMENT = 1111'
    myc.execute(sql)
    myc.close()
except:
    # print("Creating table unsuccessful")
    pass

# creating books tables
try:
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql ='CREATE TABLE books(book_id BIGINT NOT NULL PRIMARY KEY, name varchar(50) NOT NULL, author varchar(30), added DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'
    myc.execute(sql)
    myc.close()
except:
    # print("creating table unsuccessful")
    pass
# creating relation table
try: 
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'CREATE TABLE issue(user_id BIGINT NOT NULL, FOREIGN KEY(user_id) REFERENCES user(user_id),book_id BIGINT NOT NULL, FOREIGN KEY(book_id) REFERENCES books(book_id), issued_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)'
    myc.execute(sql)
    myc.close()
except:
    # print("creating table unsuccessful")
    pass

# creating function for choice
def choice():
    print("1. Add User")
    print("2. Remove User")
    print("3. Add Book ")
    print("4. Remove Book")
    print("5. Issue Book to User")
    print("6. View Issued books to user ")
    print("7. View all issues")
    print("8. View all Users")
    print("9. View all Books")
    print("10. View User by User Id")
    print("11. View Book by Book Id")
    print("12. Remove issued book")
    print("13. Exit Program!")
    option = int(input("Enter Choice:   "))
    return option

# add_user
def add_user():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'INSERT INTO user(name, dob, address) VALUES(%s,%s,%s)'
    name = input("Enter Name: ")
    dob = input("Enter Date of Birth in format (yyyy-mm-dd): ")
    address = input("Enter address: ")
    para = (name, dob, address)
    myc.execute(sql,para)
    confirm = input(f" You are going to insert \n Name = {name} \n DOB = {dob} \n Address = {address} \n Enter (y/n): ")
    if(confirm.lower() == 'y'):
        conn.commit()
        sql = 'SELECT user_id from user ORDER BY user_id DESC LIMIT 1'
        myc.execute(sql)
        data = myc.fetchone()
        print(f"User has been successfully added! \n Name = {name} \n Dob = {dob} \n Address = {address} \n with User Id = {data[0]} \n Don't forget to note down the auto generated user id!!")
    myc.close()
# add_book
def add_book():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'INSERT INTO books(book_id, name, author) VALUES(%s,%s,%s)'
    book_id = int(input("Enter Book Id: "))
    name = input("Enter Name: ")
    author = input("Enter Author: ")
    para = (book_id, name, author)
    myc.execute(sql,para)
    confirm = input(f" You are going to insert \n Book Id = {book_id} \n Name = {name} \n Author = {author} \n Enter (y/n): ")
    if(confirm.lower() == 'y'):
        conn.commit()
        print(f"Book has been successfully added! \n Name = {name} \n Author = {author} \n Book Id = {book_id} ")
    myc.close()
# remove_user
def remove_user():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    user_id = int(input("Enter User ID: "))
    para = (user_id,)
    try: 
        sql = 'DELETE from user WHERE user_id = %s'
        myc.execute(sql,para)
        confirm = input(f" You are going to delete data of user having Id {user_id} \n Enter (y/n): ")
        if(confirm.lower() == 'y'):
            conn.commit()
        print("Successfully Deleted!")
    except:
        sql ='DELETE FROM issue WHERE user_id = %s'
        myc.execute(sql,para)
        conn.commit()
        sql = 'DELETE from user WHERE user_id = %s'
        myc.execute(sql,para)
        confirm = input(f" You are going to delete data of user having Id {user_id} \n Enter (y/n): ")
        if(confirm.lower() == 'y'):
            conn.commit()
        print("Successfully Deleted!")
    myc.close()

def remove_book():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    book_id = int(input("Enter Book ID: "))
    para = (book_id,)
    try: 
        sql = 'DELETE from books WHERE book_id = %s'
        myc.execute(sql,para)
        confirm = input(f" You are going to delete book having Id {book_id} \n Enter (y/n): ")
        if(confirm.lower() == 'y'):
            conn.commit()
        print("Book Successfully Removed!")
    except:
        sql = 'DELETE FROM issue WHERE book_id = %s'
        myc.execute(sql,para)
        sql = 'DELETE from books WHERE book_id = %s'
        myc.execute(sql,para)
        confirm = input(f" You are going to delete book having Id {book_id} \n Enter (y/n): ")
        if(confirm.lower() == 'y'):
            conn.commit()
            print("Book Successfully Removed!")

    myc.close()

# issue_book_to_user
def issue_book_to_user():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    user_id = int(input("Enter Used Id: "))
    book_id = int(input("Enter Book Id: "))
    para = (user_id,)
    sql = 'SELECT EXISTS(SELECT * FROM user WHERE user_id = %s)'
    myc.execute(sql,para) 
    data = myc.fetchone()
    if(data[0] == 1):
        sql = 'SELECT EXISTS(SELECT * FROM books WHERE book_id = %s)'
        para = (book_id,)
        myc.execute(sql,para)
        data = myc.fetchone()
        if(data[0]==1):
            sql = 'INSERT INTO issue(user_id,book_id) VALUES(%s,%s)'
            para = (user_id,book_id)
            myc.execute(sql,para)
            conn.commit()
            print("Successfully Issued!")
        else:
            print("Book Id not found")
    else:
        print("User Id not found")
    

    myc.close()

# view_all_issues
def view_all_issues():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'SELECT user.user_id,user.name, books.book_id, books.name, issue.issued_at FROM issue JOIN user ON issue.user_id = user.user_id JOIN books ON issue.book_id = books.book_id'
    myc.execute(sql)
    data = myc.fetchall()
    df = pd.DataFrame(data,columns=['   User Id','   User_Name', '  Book Id', '    Book_Name','    Issued_At'])
    print(df)

# view_issued_book_to_user
def view_issued_book_to_user():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    user_id = int(input("Enter User Id: "))
    para = (user_id,)
    sql = 'SELECT EXISTS(SELECT * FROM user WHERE user_id = %s)'
    myc.execute(sql,para) 
    data = myc.fetchone()
    if(data[0] == 1):
        sql = 'SELECT * FROM issue WHERE user_id = %s'
        myc.execute(sql, para)
        data = myc.fetchall()
        print(f"Books issued to user having id {user_id}")
        for item in data:
            sql = 'SELECT name FROM books where book_id = %s'
            para = (item[1],)
            myc.execute(sql, para)
            data1 = myc.fetchall()
            for i in data1:
                print(i[0])
    else:
        print("Invalid User Id")


# view all users
def view_all_users():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'SELECT * FROM user'
    myc.execute(sql)
    data = myc.fetchall()
    df = pd.DataFrame(data, columns=["User Id", "Name","Date Of Birth", " Address", "Added At"])
    print(df)

# view all_books
def view_all_books():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'SELECT * FROM books'
    myc.execute(sql)
    data = myc.fetchall()
    df = pd.DataFrame(data,columns=['ID', "Name", "Author", 'Added At'])
    print(df)



# view user by user id
def view_user_by_id():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'SELECT * FROM user WHERE user_id = %s'
    user_id = int(input("Enter user id: "))
    para = (user_id,)
    try:
        myc.execute(sql, para)
        data = myc.fetchall()
        df = pd.DataFrame(data,columns=["   ID", "  Name", "    Date Of Birth", "   Address","  Added At"])
        print(df)
    except:
        print("User Id doesn't exist: ")
    myc.close()

# view book by Id
def view_book_by_id():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    sql = 'SELECT * FROM books WHERE book_id = %s'
    book_id = int(input("Enter book id: "))
    para = (book_id,)
    try:
        myc.execute(sql, para)
        data = myc.fetchall()
        df = pd.DataFrame(data, columns=['  ID','   Name','     Author','   Added At'])
        print(df)
    except:
        print("Book Id doesn't exist: ")
    myc.close()

#remove_issued_book
def remove_issued_book():
    conn = mysql.connector.connect(**config)
    myc = conn.cursor()
    user_id = int(input("Enter user id: "))
    book_id = int(input("ENter book id: "))
    para = (user_id,book_id)
    sql = 'SELECT EXISTS(SELECT * FROM issue WHERE user_id = %s AND book_id = %s)'
    myc.execute(sql,para)
    data = myc.fetchone()
    if(data[0] == 1):
        sql = 'DELETE FROM issue WHERE user_id = %s AND book_id = %s'
        myc.execute(sql,para)
        conn.commit()
        print("Issue Deleted! ")
    else:
        print("Issue not found! ")


# controlling program using While Loop
while True: 
    option = choice()
    os.system('cls')
    if(option == 1):
        add_user()
    elif(option == 2):
        remove_user()
    elif(option == 3):
        add_book()
    elif(option == 4):
        remove_book()
    elif(option == 5):
        issue_book_to_user()
    elif(option == 6):
        view_issued_book_to_user()
    elif(option == 7):
        view_all_issues()
    elif(option == 8):
        view_all_users()
    elif(option == 9):
        view_all_books()
    elif(option == 10):
        view_user_by_id()
    elif(option == 11):
        view_book_by_id()
    elif(option == 12):
        remove_issued_book()
    elif(option == 13):
        print("Exiting Program!!")
        break
    else:
        print("Invalid Choice")
    os.system('pause')

conn.close()