import json
import os
import sqlite3
from User import User


def initialize_db():
    conn = sqlite3.connect("Users.db")  # create connection to sql
    c = conn.cursor()  # make the connection object
    # SQL command to create table and columns
    tableString = """ CREATE TABLE Users ( 
                      id INTEGER not null primary key,
                      first_name VARCHAR(30),
                      last_name VARCHAR(30),
                      age INTEGER, 
                      city VARCHAR(30),
                      phone_number VARCHAR(30))"""
    try:
        c.execute(tableString)  # create a table
    except sqlite3.OperationalError:
        pass  # do nothing if table already exists
    conn.commit()  # Save (commit) the changes
    conn.close()


def readInData():
    user_list = []  # initialize list
    try:
        conn = sqlite3.connect("Users.db")  # use filename to create connection to sql
        c = conn.cursor()  # make the connection object
        c.execute("SELECT * FROM Users")  # execute query
        record = c.fetchall()  # save query results
        for item in record:
            # loop through list and set indexes to items
            newUser = User(item[0], item[1], item[2], item[3], item[4], item[5])
            user_list.append(newUser)
        conn.commit()
        conn.close()
        return user_list
    except sqlite3.OperationalError:  # if Users.db file isn't found
        initialize_db()  # create the database file
        print("No database file found. New database created.")
        return user_list


# JSON to database function
def JSON_to_db():
    while True:
        filename = input("Please enter JSON file name: ").lower()  # get filename from user
        if filename.endswith(".json"):  # if user filename endswith .json try the following:
            try:  # try to open connection with file
                userList = []
                with open(filename, "r") as file:
                    data = json.load(file)  # store json data in variable
                    conn = sqlite3.connect("Users.db")  # create connection to sql
                    c = conn.cursor()  # make the connection object
                    count = 0
                    for item in data:
                        # loop through and make new user object for each, append to userList
                        newUser = User(item["id"], item["first_name"], item["last_name"], item["age"], item["city"],
                                       item["phone_number"])
                        userList.append(newUser)
                        count += 1
                        # store each object variable
                        id_num = item["id"]
                        first_name = item["first_name"]
                        last_name = item["last_name"]
                        age = item["age"]
                        city = item["city"]
                        phone_number = item["phone_number"]
                        # try to insert the object variables into table columns
                        try:
                            c.execute("INSERT INTO Users (id, first_name, last_name, age, city, phone_number) "
                                      "VALUES(?, ?, ?, ?, ?, ?)",
                                      (id_num, first_name, last_name, age, city, phone_number))
                        except sqlite3.IntegrityError:
                            print("Entry already exists")
                            break
                    conn.commit()  # Save (commit) the changes
                    conn.close()
                    print("File Found,", filename, "has", count, "objects. Loading into database.")
                    return userList
            except FileNotFoundError:
                print("File not found. Try again.")
        else:
            ext = os.path.splitext(filename)  # get the file extension
            print("Unfortunately " + str(ext[0]) + str(ext[1]) + " is not supported format, only JSON.")


# database to JSON function
def db_to_JSON():
    print("Exporting all data to JSON object.")
    user_list = readInData()  # make list of current SQL table
    writeout = []  # blank list to append to
    while True:
        filename = input("Please enter the name for the export file: ")
        if filename.endswith(".json"):  # if file extension is good, change each user to dict and append
            for item in user_list:
                writeout.append(item.__dict__())
            with open(filename, "w") as file:  # save dict list to file
                json.dump(writeout, file)
            break
        else:
            ext = os.path.splitext(filename)  # get the file extension
            print("Unfortunately " + str(ext[0]) + str(ext[1]) + " is not supported format, only JSON.")


# Custom user SQL command function
def SQL_command():
    retry = True  # retry loop
    while retry:
        user_list = []
        print("Please enter your custom SQL, there is only one table named Users, and here is the list of columns: ")
        print("id, first_name, last_name, age, city, phone_number")
        query = str(input("Enter your SQL Command: "))  # get input from user
        if query.upper().startswith("SELECT"):  # validate it starts with select only
            try:  # try to connect to db
                conn = sqlite3.connect("Users.db")
                c = conn.cursor()
                c.execute(query)  # send query
                record = c.fetchall()  # store query results
                for item in record:  # loop through results and create user object for each, append to userList
                    newUser = User(item[0], item[1], item[2], item[3], item[4], item[5])
                    user_list.append(newUser)
                conn.commit()
                conn.close()  # close connection to SQL
                print_all(user_list)  # print query results
                while True:  # loop for user retry choice
                    choice = input("Do you wish to continue (Y) or back to main menu (B)?").upper()
                    if choice == "B":
                        retry = False
                        break
                    elif choice == "Y":
                        retry = True
                        break
                    else:
                        print("Enter a valid choice.")
            except sqlite3.OperationalError:
                print("Sorry something went wrong.")
        elif query.upper().startswith("DELETE"):
            print("Sorry Delete is not allowed, only Select.")
        else:
            print("Only SELECT is allowed.")


# Print all function
def print_all(user_list):
    print("\n** User list **")
    for user in user_list:  # loop through product list and print
        user.__str__()


def main():
    while True:  # program loop
        count = 0
        user_list = readInData()  # make list of current SQL table
        for _ in user_list:  # count list elements for menu
            count += 1
        print("File Found, Users.db has " + str(count) + " objects.",
              "\n--------------------------------------------------------",
              "\n1 - Load JSON data into Database",
              "\n2 - Export Database to JSON object",
              "\n3 - Custom SQL Command",
              "\n4 - Print All data in Database",
              "\nQ - Quit",
              "\n--------------------------------------------------------")

        choice = input("Enter choice: ").upper()
        match choice:
            case "1": JSON_to_db()
            case "2": db_to_JSON()
            case "3": SQL_command()
            case "4": print_all(user_list)
            case "Q": print("Terminating Program, Good Bye!"), exit()
            case _: print("Invalid choice, Try again.")


if __name__ == "__main__":
    main()
