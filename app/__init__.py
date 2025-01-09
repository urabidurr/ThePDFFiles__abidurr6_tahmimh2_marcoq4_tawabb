from flask import Flask, render_template, url_for, session, request, redirect
import os, json, urllib.request

app = Flask(__name__)

app.secret_key = os.urandom(32)
##########################################
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')
##########################################
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        type = request.form.get("type")
        #LOGIN BUTTON
        if (type == "loginenter"):
            #DB STUFF HERE
            if (True):
                session['username'] = ""
                return redirect(url_for('home'))
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
            #DB STUFF HERE
            if (True):
                session['username'] = ""
                return redirect(url_for('home'))
        #RETURN BACK HOME BUTTON
        if (type == "returnhome"):
            return redirect(url_for('home'))
    return render_template('signup.html')
##########################################
if __name__ == "__main__":
    app.debug = True
    app.run()
