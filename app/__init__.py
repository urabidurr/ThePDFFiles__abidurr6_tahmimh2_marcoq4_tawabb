from flask import Flask, render_template, url_for, session, request, redirect
import os, json, urllib.request

app = Flask(__name__)

app.secret_key = os.urandom(32)
##########################################
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

