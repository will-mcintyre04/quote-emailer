import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('quotes.db')
        self.create_tables()

    def create_tables(self):
        try:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    quote TEXT,
                    author TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY,
                    email TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error while creating tables: {e}")

    def insert_quote(self, quote_text, quote_author):
        try:
            self.conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote_text, quote_author))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error while inserting quote: {e}")

    def insert_email(self, email):
        try:
            # Check if the email already exists in the database
            cursor = self.conn.execute('SELECT COUNT(*) FROM emails WHERE email = ?', (email,))
            count = cursor.fetchone()[0]
            print(count)
            if count == 0:
                # If the email does not exist, insert it into the 'subscribers' table
                self.conn.execute('INSERT INTO emails (email) VALUES (?)', (email,))
                self.conn.commit()
                print(f"Subscriber {email} added successfully!")
            else:
                print(f"Subscriber {email} already exists in the list.")
        except sqlite3.Error as e:
            print(f"Error while inserting email: {e}")

    def get_emails(self):
        try:
            cursor = self.conn.execute('SELECT email FROM emails')
            emails = [row[0] for row in cursor.fetchall()]
            return emails
        except sqlite3.Error as e:
            print(f"Error while retrieving emails: {e}")
            return []

    def __del__(self):
        self.conn.close()