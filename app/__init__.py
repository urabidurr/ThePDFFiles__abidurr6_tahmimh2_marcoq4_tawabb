from flask import Flask, render_template, url_for, session, request, redirect, flash, get_flashed_messages
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
            print("LOGIN get username " + str(db.getUserID(username)))
            print(db.getUserID(username) is not None)
            print(db.getPassword(username)[0])
            print("LOGIN check password" + str(db.getPassword(username)[0]==password))
            if ((db.getUserID(username) is not None) and (db.getPassword(username)[0]==password)):
                session['username'] = username
                print("LOGIN CORRECT")
                return redirect(url_for('home'))
            else:
                print("LOGIN INCORRECT")
                flash("Username or password is incorrect. Try again")
        #RETURN BACK HOME BUTTON
        if (type == "returnhome"):
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
            print("SIGNUP get username" + str(db.getUserID(username)))
            if ((db.getUserID(username) is None)):
                db.createuser(username, password)
                session['username'] = username
            else:
                flash("Username is already taken. Please try a different username")
            return redirect(url_for('home'))
        #RETURN BACK HOME BUTTON
        if (type == "returnhome"):
            return redirect(url_for('home'))
    return render_template('signup.html')
##########################################
edit_mode = False
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    global edit_mode
    if 'username' in session:
        #THIS IS WHERE DATABASE CALL WILL BE.
        username = session['username']
        description = "I am the guy."
        coding_lang = "NetLogo"
        song = "Everybody Wants to Rule the World"
        pfp = "/static/devo_pfp.png"
        if request.method == 'POST':
            type = request.form.get("type")
            if (type == "logoutbutton"):
                edit_mode = False
                session.pop('username')
                return redirect(url_for('home'))
            elif (type == "homebutton"):
                edit_mode = False
                return redirect(url_for('home'))
            elif (type =="messagesbutton"):
                edit_mode = False
                return redirect(url_for('messages'))
            elif (type =="matchbutton"):
                edit_mode = False
                return redirect(url_for('match'))
            elif (type =="editbutton"):
                edit_mode = True
            elif (type =="submitedit"):
                if (len(request.form.get("aboutme")) > 0):
                    description = request.form.get("aboutme")
                if (len(request.form.get("preflang")) > 0):
                    coding_lang = request.form.get("preflang")
                if (len(request.form.get("favsong")) > 0):
                    song = request.form.get("favsong")
                edit_mode = False
        return render_template('profile.html', user = username, desc = description, pref_lang = coding_lang, pref_song = song, image = pfp, edit = edit_mode)
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
