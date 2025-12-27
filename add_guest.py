#!/usr/bin/env python3
"""add_guest.py — simple CLI to insert guestbook entries into the MySQL DB

Usage examples:
  python add_guest.py --name "Alice" --email alice@example.com --message "Hello!"
  python add_guest.py --sample
  python add_guest.py          # interactive prompt

The script uses the same DB configuration as `app.py` (reads env vars). It calls `init_db()` before inserting to ensure the table exists.
"""

import argparse
import sys
from app import init_db, get_connection


def insert_entry(conn, name, email, phone, message):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO guests (name, email, phone, message) VALUES (%s, %s, %s, %s)",
        (name, email or None, phone or None, message)
    )
    conn.commit()
    cur.close()


def main():
    parser = argparse.ArgumentParser(description='Insert a guestbook entry into MySQL DB')
    parser.add_argument('--name', '-n', help='Name of the guest')
    parser.add_argument('--email', '-e', help='Email address')
    parser.add_argument('--phone', '-p', help='Phone number')
    parser.add_argument('--message', '-m', help='Message content')
    parser.add_argument('--sample', action='store_true', help='Insert a sample entry (for testing)')

    args = parser.parse_args()

    if args.sample:
        name = 'Sample Guest'
        email = 'sample@example.com'
        phone = '0000000000'
        message = 'This is a sample guestbook entry.'
    else:
        name = args.name
        email = args.email
        phone = args.phone
        message = args.message

        if not name or not message:
            print('Running interactively (name and message are required).')
            try:
                if not name:
                    name = input('Name: ').strip()
                if not email:
                    email = input('Email (optional): ').strip() or None
                if not phone:
                    phone = input('Phone (optional): ').strip() or None
                if not message:
                    message = input('Message: ').strip()
            except (KeyboardInterrupt, EOFError):
                print('\nAborted.')
                sys.exit(1)

    if not name or not message:
        print('Error: name and message are required.')
        sys.exit(1)

    try:
        # Ensure DB/table exist and then insert
        init_db()
        conn = get_connection()
        insert_entry(conn, name, email, phone, message)
        conn.close()
        print('Entry added successfully.')
    except Exception as exc:
        print('Failed to add entry:', exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
