# Guestbook (Flask + MySQL)

Simple visitor guestbook web app using Flask and MySQL (mysql-connector-python).

## Features
- Add, edit, delete guestbook messages
- Simple HTML/CSS frontend
- Uses environment variables for DB configuration
- Automatically creates database & table on first run (if credentials allow)

## Setup
1. Create a Python virtual environment and install requirements:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Export or set environment variables (Windows PowerShell example):

```powershell
$env:DB_HOST = 'localhost'
$env:DB_PORT = '3306'
$env:DB_USER = 'your_mysql_user'
$env:DB_PASSWORD = 'your_password'
$env:DB_NAME = 'guestbook'
$env:SECRET_KEY = 'change-me'
```

3. Run the app:

```
python app.py
```

The app will attempt to create the database and `guests` table if it has appropriate privileges.

## Notes
- If you prefer not to expose credentials via env vars, you can edit `app.py` to set them directly (not recommended).
- Let me know if you want me to add pagination, search, or CSV export.
