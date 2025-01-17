'''
The PDF Files - Tawab Berri, Abidur Rahman, Marco Quintero, Tahmim Hassan
SoftDev
2025-01-09
p02 - Devuzz
time spent: 14 hrs
'''

from flask import Flask, render_template, url_for, session, request, redirect, flash, get_flashed_messages
import os, json, urllib.request, sqlite3, datetime
from db import db
from api import send_message, CHARACTER_IDS
import asyncio

app = Flask(__name__)

app.secret_key = os.urandom(32)

DB_FILE = "database.db" #create a database for private keys storage

dbase = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = dbase.cursor()  #facilitate db ops -- you will use cursor to trigger db events

##########################################
db.create()
db.addPresetUsers()
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
            #print(db.getUserID(username) is not None)
            #print(db.getPassword(username)[0])
            #print("LOGIN check password" + str(db.getPassword(username)[0]==password))
            print("len username: " + str(len(username)))
            print("len password: " + str(len(password)))
            if (len(username) < 1 or len(password) < 1):
                flash("Insufficient characters in username or password. Try again.")
            elif ((db.getUserID(username) is not None) and (db.getPassword(username)[0]==password)):
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
            if (len(username) < 1 or len(password) < 1):
                flash("Insufficient characters in username or password. Try again.")
            elif ((db.getUserID(username) is None)):
                db.createuser(username, password)
                session['username'] = username
                db.addRelation(db.getUserID(username))
                print("Relations table: ")
                print(db.getRelations())
            else:
                flash("Username is already taken. Please try a different username")
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
        UID = db.getUserID(session['username'])
        username = db.getUserData(UID).get("username")
        description = db.getUserData(UID).get("description")
        coding_lang = db.getUserData(UID).get("language")
        song = db.getUserData(UID).get("song")
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
                    db.editUserData(UID, "description", description)
                if (len(request.form.get("preflang")) > 0):
                    coding_lang = request.form.get("preflang")
                    db.editUserData(UID, "language", coding_lang)
                if (len(request.form.get("favsong")) > 0):
                    song = request.form.get("favsong")
                    db.editUserData(UID, "song", song)
                edit_mode = False
        return render_template('profile.html', user = username, desc = description, pref_lang = coding_lang, pref_song = song, image = pfp, edit = edit_mode)
    return redirect(url_for('home'))
##########################################
other_user = -1
@app.route("/messages", methods=['GET', 'POST'])
def messages():
    global other_user
    if 'username' in session:
        users = ['Git Clone Topher', 'Nobody', 'Drake', 'Gojo Satoru']
        conversations = [[{"sender": session['username'], "text": "Hi", "time sent": "10:45"},
                         {"sender": 'Git Clone Topher', "text": "Hello fellow devo of the intertrash", "time sent": "10:46"}],
                        [{"sender": session['username'], "text": "New phone who dis?", "time sent": "23:00"},
                         {"sender": "Nobody", "text": "Nobody", "time sent": "23:05"}],
                        [{"sender": 'Drake', "text": "What's good devo?", "time sent": "8:15"},
                         {"sender": session['username'], "text": "Your music sucks", "time sent": "9:15"},
                         {"sender": "Drake", "text": ";(", "time sent": "9:15"}],
                        []]
        db.addMessage(0, 1, 2, )
        uid = db.allAcceptedUsers(db.getUserData(session['username']))
        usernames = []
        for n in uid:
            usernames.append(db.getUserData(uid[n]).get("username"))
        convos = db.getAllMessages(sender_id)
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
                if message and message.strip():
                    time_sent = datetime.datetime.now().strftime("%H:%M")
                    conversations[other_user].append({"sender": session["username"],"text": message,"time-sent": time_sent})

                    try:
                        char_id = CHARACTER_IDS.get(users[other_user])
                        if char_id:
                            session_id = f"{session['username']}_{users[other_user]}"
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            ai_name, ai_response = loop.run_until_complete(send_message(char_id, message, session_id))
                            loop.close()
                            conversations[other_user].append({"sender": users[other_user], "text": ai_response, "time-sent": datetime.datetime.now().strftime("%H:%M")})
                    except Exception as e:
                        print(f"Error getting AI response: {e}")
                        # Add error message to conversation
                        conversations[other_user].append({"sender": users[other_user], "text": "Sorry, I'm having trouble connecting right now.", "time-sent": datetime.datetime.now().strftime("%H:%M")})
            else:
                try:
                    other_user = int(type)
                except (TypeError, ValueError):
                    pass
        return render_template('messages.html', matches = users, convos = conversations, convo_open = other_user, user = session['username'])
    return redirect(url_for('home'))
##########################################
@app.route("/match", methods=['GET', 'POST'])
def match():
    if 'username' in session:
        #Dictionaries will be made up by database calls
        other_users = []
        for n in range(db.latestUID()):
            if (n != db.getUserID(session['username']) and db.getStatus(db.getUserID(session['username']), n)=="stranger"):
                other_users.append(db.getUserData(n))
        print("Strangers: " + str(other_users))
        if request.method == "POST":
            swipe_direction = request.form.get("swipe_direction")
            swiped_user = request.form.get("swiped_user")

            if swipe_direction and swiped_user:
                current_user_id = db.getUserID(session['username'])
                swiped_user_id = db.getUserID(swiped_user)

                if swipe_direction == "like":
                    print(f"User {session['username']} liked {swiped_user}")
                    db.statusChange(current_user_id, swiped_user_id, "accepted")
                    # Adding database logic here for likes
                else:
                    print(f"User {session['username']} disliked {swiped_user}")
                    db.statusChange(current_user_id, swiped_user_id, "rejected")
                    # Adding logic here for dislikes

        return render_template('match.html', profiles = other_users)
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.debug = True
    app.run()
