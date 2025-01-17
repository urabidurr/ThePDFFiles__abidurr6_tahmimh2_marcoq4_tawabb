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
def latestUID():
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute('''SELECT * FROM users''')
    lengt = c.fetchall()
    id = len(lengt)
    dbase.commit()
    dbase.close()
    return id
def getUserID(username):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    dbase.close()
    if row == None:
        return None
    return row[0]

def getPassword(username):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    pw = c.fetchall()
    print(pw)
    dbase.commit()
    dbase.close()
    return pw[0]

def getUserData(id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    dict = {}
    c.execute("SELECT username, password, description, language, song FROM users WHERE id = ?", (id,))
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    dict['username'] = ret[0][0]
    dict['password'] = ret[0][1]
    dict['description'] = ret[0][2]
    dict['language'] = ret[0][3]
    dict['song'] = ret[0][4]
    dbase.commit()
    dbase.close()
    return dict

def getMessageData(sender_id, recipient_id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    messages = []
    dict = {}
    c.execute("SELECT content, date_sent FROM chat WHERE sender_id, recipient_id = ?, ?", (sender_id, recipient_id))
    ret = c.fetchall()
    print(ret) #DIAGNOSTIC PRINT STATEMENT
    for n in range(len(ret)):
        dict['content'] = ret[n][0]
        dict['date_sent'] = ret[n][1]
        messages.append(dict)
    dbase.commit()
    dbase.close()
    return dict

def addMessage(sender_id, recipient_id, content, date_sent):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("INSERT INTO chat (sender_id, recipient_id, content, message_id, date_sent) VALUES (?, ?, ?, ?, ?)", (sender_id, recipient_id, content, date_sent))
    print("message added") #DIAGNOSTIC PRINT STATEMENT
    dbase.commit()
    dbase.close()

def editUserData(id, data, new_value):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute(f"UPDATE users SET {data} = ? WHERE id = ?", (new_value, id))
    dbase.commit()
    dbase.close()

def getRelations():
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT * from relations")
    relations = c.fetchall()
    print(relations)
    dbase.commit()
    dbase.close()
    return relations

def addRelation(id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    for i in range(id):
        c.execute("INSERT INTO relations (id, username, other_id, relationship) VALUES (?, ?, ?, ?)", (id, getUserData(id).get("username"), i, "stranger"))
        c.execute("INSERT INTO relations (id, username, other_id, relationship) VALUES (?, ?, ?, ?)", (i, getUserData(i).get("username"), id, "stranger"))
    dbase.commit()
    dbase.close()

def getStatus(id, other_id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT relationship from relations WHERE (id, other_id) = (?, ?)", (id, other_id))
    status = c.fetchall()
    print("Relationship status of " + str(id) + " and " + str(other_id) + str(status))
    dbase.commit()
    dbase.close()
    return status[0][0]

def statusChange(id, other_id, relationship):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("UPDATE relations SET relationship = ? WHERE (id, other_id) = (?, ?)", (relationship, id, other_id))
    dbase.commit()
    dbase.close()

def allAcceptedUsers(id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("SELECT other_id WHERE id = ?", (id,))
    others = c.fetchall()
    print(others)
    dbase.commit()
    dbase.close()
    return others

def getAllMessages(sender_id, recipient_id):
    dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
    c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events
    c.execute("")
    c.execute("SELECT * FROM chat WHERE sender_id, recipient_id = ?, ?", (sender_id, recipient_id))
    messages = c.fetchall()
    print(messages)
    dbase.commit()
    dbase.close()
    return messages

def addPresetUsers():
    createuser("topher", "mykolyk")
    editUserData(0, "description", "Hello devos. This is Topher Mykolyk.")
    editUserData(0, "language", "DrRacket")
    editUserData(0, "song", "Not Like Us")
    createuser("bryant", "cupcake")
    addRelation(1)
    createuser("drake", "anitamaxwynn")
    editUserData(2, "description", "Yo this is Aubrey Drake Graham")
    editUserData(2, "language", "Microsoft Assembly Script")
    editUserData(2, "song", "wahgwan delilah")
    addRelation(2)
    createuser("gojo satoru", "honoredone")
    editUserData(3, "description", "I alone am the honored one.")
    editUserData(3, "language", "Python.")
    editUserData(3, "song", "Skyfall")
    addRelation(3)
