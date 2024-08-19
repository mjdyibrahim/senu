# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 18:35:38 2024

@author: hf_qu
"""

import plotly.express as px
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import psycopg2



app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class data:
    def connect(self, hostname, database, username, pwd, port_id):
        self.conn, self.cur = None, None    
        try:
            self.conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
                )
            self.cur = self.conn.cursor()
    
        except Exception as error:
            print(error)
        


def login_required(f):
    """
    Decorate routes to require login.

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@login_required
def get_values():
    values = []
    return values


@app.route("/startup-readiness", methods = ["POST"])
@login_required
def plot():
    values = get_values()
    df = pd.DataFrame(dict(
        r=values,
        theta=['burn rate','growth','market size',
               'CAC', 'LTV', "valuation"]))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #edit code here
        rows = data.cur.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/")
    return render_template('login.html')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

