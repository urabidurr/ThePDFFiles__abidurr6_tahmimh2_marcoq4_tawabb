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
    c.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            description TEXT,
            language TEXT,
            song TEXT
            rejected INTEGER
            accepted INTEGER
            stranger INTEGER
            );
    ''')


    # making a table for chat history
    c.execute(
    '''
    CREATE TABLE IF NOT EXISTS chat (
            sender_id INTEGER PRIMARY KEY,
            recipient_id INTEGER,
            content TEXT,
            message_id INTEGER,
            date_sent TEXT
            );
    ''')
