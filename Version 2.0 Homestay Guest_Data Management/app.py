from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # Change to your MySQL username
        password="tiger",  # Change to your MySQL password
        database="connector_db"
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # dictionary=True makes it easy to use in HTML
    
    # Task: Get all messages from the database
    cursor.execute("SELECT * FROM guestbook ORDER BY created_at DESC")
    entries = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form.get('name')
    purpose = request.form.get('purpose')
    message = request.form.get('message')

    if name and message:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Task: Insert the new visitor data into MySQL
        query = "INSERT INTO guestbook (name, purpose, message) VALUES (%s, %s, %s)"
        values = (name, purpose, message)
        
        cursor.execute(query, values)
        conn.commit() # This "saves" the changes permanently
        
        cursor.close()
        conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)