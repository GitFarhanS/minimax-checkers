import sqlite3 #imports sql
import hashlib #imports hashing algorithm

conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS userdata ( 
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
''') #creates the table for the database and inputs username and password

def update_database(username, password):

    hash_password = hashlib.sha256(password.encode()).hexdigest() #sets the username and password

    cursor.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hash_password)) #inserst username and password into the database
    
    conn.commit() #commits to the database
    
    conn.close()



