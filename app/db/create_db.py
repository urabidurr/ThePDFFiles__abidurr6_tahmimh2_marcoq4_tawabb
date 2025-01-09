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

# making a table for users
c.execute(
'''
CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        description TEXT,
        language TEXT,
        song TEXT
        );
''')

# making a table for matching
c.execute(
'''
CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        rejected INTEGER,
        accepted INTEGER,
        undecided INTEGER
        );
''')

# making a table for chat history
c.execute(
'''
CREATE TABLE IF NOT EXISTS matches (
        sender_id INTEGER PRIMARY KEY,
        recipient_id INTEGER,
        content TEXT,
        message_id INTEGER,
        date_sent TEXT
        );
''')
