import os
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret')

# DB config comes from environment variables for safety
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'tiger'),
    'database': os.getenv('DB_NAME', 'gestbook_record')
}


def init_db():
    """Create database and table if they do not exist."""
    # Connect without database to ensure DB exists
    temp = {
        'host': DB_CONFIG['host'],
        'port': DB_CONFIG['port'],
        'user': DB_CONFIG['root'],
        'password': DB_CONFIG['tiger'],
    }
    try:
        conn = mysql.connector.connect(**temp)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` DEFAULT CHARACTER SET 'utf8mb4'")
        conn.commit()
        cursor.close()
        conn.close()

        # Now create the table
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS guests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
        print('Database initialized or already exists.')
    except Error as e:
        print('Could not initialize database:', e)


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route('/')
def index():
    # List guestbook entries
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM guests ORDER BY created_at DESC")
        entries = cursor.fetchall()
    except Error as e:
        entries = []
        flash('Database connection failed: ' + str(e), 'error')
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        flash('Name and message are required.', 'error')
        return redirect(url_for('index'))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO guests (name, email, phone, message) VALUES (%s, %s, %s, %s)",
            (name, email, phone, message)
        )
        conn.commit()
        flash('Entry added successfully!', 'success')
    except Error as e:
        flash('Failed to add entry: ' + str(e), 'error')
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return redirect(url_for('index'))


@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not message:
            flash('Name and message are required.', 'error')
            return redirect(url_for('edit_entry', entry_id=entry_id))

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE guests SET name=%s, email=%s, phone=%s, message=%s WHERE id=%s",
                (name, email, phone, message, entry_id)
            )
            conn.commit()
            flash('Entry updated successfully!', 'success')
        except Error as e:
            flash('Failed to update entry: ' + str(e), 'error')
        finally:
            try:
                cursor.close()
                conn.close()
            except Exception:
                pass

        return redirect(url_for('index'))

    # GET: show form
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM guests WHERE id=%s', (entry_id,))
        entry = cursor.fetchone()
        if not entry:
            flash('Entry not found.', 'error')
            return redirect(url_for('index'))
    except Error as e:
        flash('Database error: ' + str(e), 'error')
        return redirect(url_for('index'))
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return render_template('edit.html', entry=entry)


@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM guests WHERE id=%s', (entry_id,))
        conn.commit()
        flash('Entry deleted.', 'success')
    except Error as e:
        flash('Failed to delete entry: ' + str(e), 'error')
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Try to initialize DB (will print an error if DB is unreachable)
    init_db()
    app.run(debug=True)