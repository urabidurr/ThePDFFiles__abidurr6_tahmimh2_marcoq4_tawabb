'''
The PDF Files - Tawab Berri, Abidur Rahman, Marco Quintero, Tahmim Hassan
SoftDev
2025-01-09
p02 - Devuzz
time spent: 14 hrs
'''

import sqlite3


DB_FILE = "database.db" #create a database for private keys storage

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()  #facilitate db ops -- you will use cursor to trigger db events

def create():
    # making a table for users
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("DROP TABLE IF EXISTS chat;")
    c.execute("DROP TABLE IF EXISTS relations;")
    c.execute(
    '''
    CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            description TEXT,
            language TEXT,
            song TEXT
            );
    ''')

    c.execute('''
        CREATE TABLE relations (
            id INTEGER,
            username TEXT,
            other_id INTEGER,
            relationship TEXT
        );

        '''
    )

    # making a table for chat history
    c.execute(
    '''
    CREATE TABLE chat (
            sender_id INTEGER,
            recipient_id INTEGER,
            content TEXT,
            message_id INTEGER PRIMARY KEY,
            date_sent TEXT
            );
    ''')
    db.commit()
    db.close()

def createuser(username, password):
    c.execute('''SELECT * FROM users''')
    lengt = c.fetchall()
    id = len(lengt)
    c.execute(
        "INSERT INTO users (id, username, password) VALUES (?, ?, ?);", (id, username, password)
    )

def findUsername(username):
    try:
        c.execute("SELECT password FROM users WHERE username = ?", username)
        return True
    except:
        return False

def getPassword(username):
    try:
        c.execute("SELECT password FROM users WHERE username = ?", username)
        pw = c.fetchall()
        return pw[0]
    except:
        return False

def getUserData(id):
    dict = {}
    c.execute("SELECT (username, password, description, language, song) FROM users WHERE id = ?", id)
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    dict['username'] = ret[0]
    dict['password'] = ret[1]
    dict['description'] = ret[2]
    dict['language'] = ret[3]
    dict['song'] = ret[4]
    return dict

def getMessageData(sender_id, recipient_id):
    dict = {}
    c.execute("SELECT (content, message_id, date_sent) FROM chat WHERE (sender_id, recipient_id) = (?, ?)", (sender_id, recipient_id))
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    dict['content'] = ret[0]
    dict['message_id'] = ret[1]
    dict['date_sent'] = ret[2]
    return dict

def addMessage(sender_id, recipient_id, content, date_sent):
    c.execute("SELECT * FROM chat WHERE (sender_id, recipient_id) = (?, ?)", (sender_id, recipient_id))
    l = len(c.fetchall())
    c.execute("INSERT INTO chat (sender_id, recipient_id, content, message_id, date_sent) VALUES = (?, ?, ?, ?, ?)", (sender_id, recipient_id, content, l, date_sent))
    print("message added") #DIAGNOSTIC PRINT STATEMENT

def editUserData(id, data, new_value):
    c.execute(f"UPDATE users SET {data} = {new_value} WHERE id = ?", (id))