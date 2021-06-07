# Collaborated with Liz for this assignment.
import dbconnect

# This function allows the hacker to log in.
def login():
    # Getting database connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Conditional that closes the database cursor and connection if either one of them fails.
    if(conn == None or cursor == None):
        print("Error in database connection!")
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return None
    # Testing code for user input, select statement, and fetching user information.
    try:
        alias = input("Please enter your alias: ")
        password = input("Please enter your password: ")
        cursor.execute("SELECT id, alias FROM hackers WHERE alias = ? AND password = ?", [alias, password])
        users = cursor.fetchall()
    # Handling errors with a print statment.
    except:
        print("Error could not query database for user")
        return None
    # The rowcount property is used for data validation and returns the specified number of rows.
    # If the alias or passwords do not match an error with a print statement occurs.
    if(cursor.rowcount != 1):
        print("Could not log in, please try again")
        return None
    # On success, the user is logged in and the database curson and connection is closed
    print(f"{alias} is logged in!!!")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # This returns the hacker's id which will be used for query based ownership statements.
    return users[0]
# This function allows the hacker to enter an exploit.
def enter_exploit(user_id):
    # Getting database connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Conditional that closes the database cursor and connection if either one of them fails.
    if(conn == None or cursor == None):
        print("Error in database connection!")
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return
    # Testing code for user input and the insert statement
    try:   
        exploit = input("Please enter your exploit: ")
        cursor.execute("INSERT INTO exploits(content, hacker_id) VALUES(?, ?)", [exploit, user_id])
    except:
        print("Error could not query database for user")
        return None
    conn.commit()
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
# This funtion gets the current hacker's exploits.    
def get_current_hacker_exploits(user_id):
    # Getting database connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Conditional that closes the database cursor and connection if either one of them fails.
    if(conn == None or cursor == None):
        print("Error in database connection!")
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return
    # Testing code for the select statment, and fetching specified data
    try:
        cursor.execute("SELECT e.id, e.content, h.alias FROM hackers h  INNER JOIN exploits e ON h.id = e.hacker_id WHERE e.hacker_id = ?", [user_id])
        exploit_rows = cursor.fetchall()
        # Looping over fetched data.
        for exploit in exploit_rows:
            print(f"exploit ID: {exploit[0]}   alias: {exploit[2]}  exploit: {exploit[1]}") 
    except:
        print("Error could not query database for user")
        return None
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
# This function gets all the exploits made by every other hacker except the hacker that is currently logged in.
def get_other_hacker_exploits(user_id):
    # Getting database connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Conditional that closes the database cursor and connection if either one of them fails.
    if(conn == None or cursor == None):
        print("Error in database connection!")
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return
    # Testing code for the select statement and fetching the specified data.
    try:
        cursor.execute("SELECT e.id, e.content, h.alias FROM hackers h  INNER JOIN exploits e ON h.id = e.hacker_id WHERE e.hacker_id <> ?", [user_id])
        exploit_rows = cursor.fetchall()
        for exploit in exploit_rows:
            print(f"exploit ID: {exploit[0]}  alias: {exploit[2]}  exploit: {exploit[1]}")
    except:
        print("Error could not query database for user")
        return None
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
# This function let's the hacker exit the program.
def exit():
    conn = dbconnect.get_db_connection()
    dbconnect.close_db_connection(conn)

user = None
# Loop that runs until the hacker logs in successfully.
while (user == None):
    user = login()
     
    
while True:
    # This gets printed when the hacker is logged in.
    print("1) Enter a new exploit")
    print("2) See all user exploits")
    print("3) See other exploits")
    print("4) Exit")
    # Takes in the hackers input to select an option. 
    selection = input("Please select an option: ")
    # Conditionals that call the specied functions based on the hackers input.
    # These functions take in an argument which determines the hackers id.
    if (selection == "1"):
        try:
            enter_exploit(user[0])
        except:
            print("Exploit not entered")
        
    elif (selection == "2"):
        try:
            get_current_hacker_exploits(user[0])
        except:
            print("Could not get exploit")
    elif (selection == "3"):
        try:
            get_other_hacker_exploits(user[0])
        except:
            print("Could not get other exploits")
    elif (selection == "4"):
        exit()
        break
    else:
        print("Invalid input, please try again")
    