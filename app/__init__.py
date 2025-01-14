from flask import Flask, render_template, url_for, session, request, redirect
import os, json, urllib.request, sqlite3, datetime
from db import db

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "database.db" #create a database for private keys storage

dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events

##########################################
db.create()

@app.route("/", methods=['GET', 'POST'])
def home():

    if 'username' in session:
        if request.method == 'POST':
            type = request.form.get("type")
            if (type == "logoutbutton"):
                session.pop('username')
                return redirect(url_for('home'))
            elif (type == "profilebutton"):
                return redirect(url_for('profile'))
            elif (type =="messagesbutton"):
                return redirect(url_for('messages'))
            elif (type =="matchbutton"):
                return redirect(url_for('match'))
        return render_template('home.html', loggedin=True)
    if request.method == 'POST':
        type = request.form.get("type")
        if (type == "loginbutton"):
            return redirect(url_for('login'))
        elif (type == "signupbutton"):
            return redirect(url_for('signup'))
    return render_template('home.html', loggedin=False)
##########################################
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        type = request.form.get("type")
        #LOGIN BUTTON
        if (type == "loginenter"):
            username = request.form.get("user")
            password = request.form.get("password")
            #CHECK IF VALID WITH DATABASE

            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            passw = c.fetchone()
            #print(passw)
            try:
                if (passw and passw[0] == password):
                    session['username'] = username
                    return redirect(url_for('home'))
            except:
        #RETURN BACK HOME BUTTON
                if (type == "returnhome"):
                    return redirect(url_for('home'))
                return redirect(url_for('home'))

    #IF LOGGED IN
    if 'username' in session:
        redirect(url_for('home'))
    return render_template('login.html')
##########################################
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    #IF LOGGED IN
    if 'username' in session:
        redirect(url_for('home'))
    if request.method == 'POST':
        type = request.form.get("type")
        #SIGN UP BUTTON
        if (type == "signupenter"):
            username = request.form.get("name")
            #print(username)
            password = request.form.get("password")
            #Comment from DMQ: SHOULDN'T THIS BE A FUNCTION IN db.py THAT IS CALLED IN THIS FILE?
            #ADD TO DATABASE
            '''c.execute("SELECT id FROM users;")
            num = c.fetchall()

            c.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?);",
            (len(num), username, password))

            print(len(num))
            for user in range(len(num)):
                c.execute("INSERT INTO relations (other_id, relationship) VALUES (?, ?);", (len(num), "stranger"))
                print(1)
                c.execute("SELECT * FROM relations")
                print(2)
                pri = c.fetchall()
                print(pri)
            #print("USER IDS:")
            #print(num)

            c.execute("SELECT * FROM users")
            prin = c.fetchall()
            print("users: ")
            print(prin)'''

            session['username'] = username
            return redirect(url_for('home'))
        #RETURN BACK HOME BUTTON
        if (type == "returnhome"):
            return redirect(url_for('home'))
    return render_template('signup.html')
##########################################
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        if request.method == 'POST':
            type = request.form.get("type")
            if (type == "logoutbutton"):
                session.pop('username')
                return redirect(url_for('home'))
            elif (type == "homebutton"):
                return redirect(url_for('home'))
            elif (type =="messagesbutton"):
                return redirect(url_for('messages'))
            elif (type =="matchbutton"):
                return redirect(url_for('match'))
        username = session['username']
        description = "I am the guy."
        coding_lang = "NetLogo"
        song = "Everybody Wants to Rule the World"
        return render_template('profile.html', user = username, desc = description, pref_lang = coding_lang, pref_song = song)
    return redirect(url_for('home'))
##########################################
other_user = -1
@app.route("/messages", methods=['GET', 'POST'])
def messages():
    global other_user
    if 'username' in session:
        #These two list will be made up of database calls. Index of value in other_users will correspond with the index of messages. Jinja templates will display the last message of the convo on the side.
        users = ['Git Clone Topher', 'Nobody', 'Drake', 'Gojo Satoru']
        #This is a 2d list containing the message histories.
        conversations = [[{"sender": session['username'], "text": "Hi", "time sent": "10:45"}, {"sender": 'Git Clone Topher', "text": "Hello fellow devo of the intertrash", "time sent": "10:46"}], [{"sender": session['username'], "text": "New phone who dis?", "time sent": "23:00"}, {"sender": "Nobody", "text": "Nobody", "time sent": "23:05"}], [{"sender": 'Drake', "text": "What's good devo?", "time sent": "8:15"}, {"sender": session['username'], "text": "Your music sucks", "time sent": "9:15"}, {"sender": "Drake", "text": ";(", "time sent": "9:15"}], []]
        if request.method == 'POST':
            type = request.form.get("type")
            if (type == "logoutbutton"):
                other_user = -1
                session.pop('username')
                return redirect(url_for('home'))
            elif (type == "homebutton"):
                other_user = -1
                return redirect(url_for('home'))
            elif (type == "profilebutton"):
                other_user = -1
                return redirect(url_for('profile'))
            elif (type == "matchbutton"):
                other_user = -1
                return redirect(url_for('match'))
            elif (type == "sendbutton"):
                message = request.form.get("usermessage")
                time_sent = datetime.datetime.now().strftime("%H:%M")
                conversations[other_user].append({"sender": session["username"], "text": message, "time sent": time_sent})
            else:
                other_user = int(type)
        return render_template('messages.html', matches = users, convos = conversations, convo_open = other_user, user = session['username'])
    return redirect(url_for('home'))
##########################################
@app.route("/match", methods=['GET', 'POST'])
def match():
    if 'username' in session:
        #Dictionaries will be made up by database calls
        other_users = [{"user": 'Nobody', "desc": "Nobody got you the way I do", "lang": "Java", "song": 'Nobodys'}, {"user": 'Drake', "desc": 'I am not allowed on here', "lang": 'C', "song": 'Wah Gwan Delilah'}, {"user": 'Gojo Satoru', "desc": 'I alone am the honored one', "lang": 'Python', "song": 'Skyfall'}]
        return render_template('match.html', profiles = other_users)
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.debug = True
    app.run()
