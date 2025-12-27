#!/usr/bin/env python3
"""seed_db.py — generate and insert fake guestbook entries using Faker

Usage:
    python seed_db.py --count 500
    python seed_db.py --count 500 --batch-size 100 --dry-run

Reads DB config from environment variables (same as `app.py`).
"""

import argparse
from faker import Faker
from datetime import datetime
from app import init_db, get_connection

fake = Faker()


def generate_entries(count):
    for _ in range(count):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        # Keep messages short-ish
        message = fake.sentence(nb_words=12)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        yield (name, email, phone, message, created_at)


def insert_batch(conn, rows):
    sql = "INSERT INTO guests (name, email, phone, message, created_at) VALUES (%s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.executemany(sql, rows)
    conn.commit()
    cur.close()


def main():
    parser = argparse.ArgumentParser(description='Seed the guestbook DB with fake data')
    parser.add_argument('--count', '-c', type=int, default=500, help='Number of entries to insert (default 500)')
    parser.add_argument('--batch-size', '-b', type=int, default=100, help='Batch size for inserts (default 100)')
    parser.add_argument('--dry-run', action='store_true', help='Generate data but do not insert into DB')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    if args.count <= 0:
        print('Count must be > 0')
        return

    print(f"Preparing to generate {args.count} fake entries (batch size {args.batch_size})")

    # Ensure DB/table exist
    init_db()

    if args.dry_run:
        # Just generate and show a sample
        sample = list(generate_entries(min(args.count, 5)))
        for i, s in enumerate(sample, 1):
            print(f"Sample {i}:", s)
        print("Dry run complete. No data inserted.")
        return

    conn = None
    try:
        conn = get_connection()
        batch = []
        inserted = 0
        gen = generate_entries(args.count)
        for row in gen:
            batch.append(row)
            if len(batch) >= args.batch_size:
                insert_batch(conn, batch)
                inserted += len(batch)
                if args.verbose:
                    print(f"Inserted {inserted}/{args.count} entries")
                batch = []
        # Insert remaining
        if batch:
            insert_batch(conn, batch)
            inserted += len(batch)
            if args.verbose:
                print(f"Inserted {inserted}/{args.count} entries")

        print(f"Seeding complete: {inserted} entries inserted.")
    except Exception as e:
        print('Failed seeding DB:', e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
