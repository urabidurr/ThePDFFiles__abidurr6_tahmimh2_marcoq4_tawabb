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
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
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
    dbase.commit()
    dbase.close()

def createuser(username, password):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    try:
        c.execute('''SELECT * FROM users''')
        lengt = c.fetchall()
        id = len(lengt)
    except:
        id = 0
    finally:
        c.execute(
            "INSERT INTO users (id, username, password) VALUES (?, ?, ?);", (id, username, password)
        )
        dbase.commit()
        dbase.close()

def findUsername(username):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    try:
        c.execute("SELECT password FROM users WHERE username = ?", username)
        dbase.commit()
        dbase.close()
        return True
    except:
        dbase.commit()
        dbase.close()
        return False

def getPassword(username):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    try:
        c.execute("SELECT password FROM users WHERE username = ?", username)
        pw = c.fetchall()
        dbase.commit()
        dbase.close()
        return pw[0]
    except:
        dbase.commit()
        dbase.close()
        return False

def getUserData(id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    dict = {}
    c.execute("SELECT (username, password, description, language, song) FROM users WHERE id = ?", id)
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    dict['username'] = ret[0]
    dict['password'] = ret[1]
    dict['description'] = ret[2]
    dict['language'] = ret[3]
    dict['song'] = ret[4]
    dbase.commit()
    dbase.close()
    return dict

def getMessageData(sender_id, recipient_id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    dict = {}
    c.execute("SELECT (content, message_id, date_sent) FROM chat WHERE (sender_id, recipient_id) = (?, ?)", (sender_id, recipient_id))
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    dict['content'] = ret[0]
    dict['message_id'] = ret[1]
    dict['date_sent'] = ret[2]
    dbase.commit()
    dbase.close()    
    return dict

def addMessage(sender_id, recipient_id, content, date_sent):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT * FROM chat WHERE (sender_id, recipient_id) = (?, ?)", (sender_id, recipient_id))
    l = len(c.fetchall())
    c.execute("INSERT INTO chat (sender_id, recipient_id, content, message_id, date_sent) VALUES = (?, ?, ?, ?, ?)", (sender_id, recipient_id, content, l, date_sent))
    print("message added") #DIAGNOSTIC PRINT STATEMENT
    dbase.commit()
    dbase.close()

def editUserData(id, data, new_value):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute(f"UPDATE users SET {data} = {new_value} WHERE id = ?", (id))
    dbase.commit()
    dbase.close()