
import plotly.express as px
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import psycopg2
import re

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



def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
        return False, "Password must contain both letters and numbers."
    return True, ""


# Route for the registration form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message)
            return redirect()

        hashed_password = generate_password_hash(password)
        
        conn = data.connect()
        cur = conn.cursor()
        
        try:
            # Insert user into the database
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                        (username, hashed_password))
            conn.commit()
            flash("User registered successfully!")
            return redirect()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            flash("Username already exists. Please choose a different username.")
            return redirect()
        
        finally:
            cur.close()
            conn.close()
    
    return render_template('register.html')

# Route to display a success message
@app.route('/success')
def success():
    return "User registered successfully!"

if __name__ == "__main__":
    app.run(debug=True)
