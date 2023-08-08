import sqlite3
import os

class Database:
    '''
    Handler that works with the quotes.db local database.\n
    Initializes connection and tables, and enables editing and viewing of data.
    '''

    def __init__(self):
        '''
        Connects to database and initializes tables.
        '''
        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_file = os.path.join(script_directory, "quotes.db")

        self.conn = sqlite3.connect(database_file)
        self.create_tables()

    def create_tables(self):
        '''
        Creates two tables in the db if they do not exist: "emails" and "quotes".
        \n\t"quotes" contains an id (primary key), and quote and author attributes
        \n\t"emails" contains an id (primary key), and email attributes
        '''
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
        '''
        Inserts the passed quote text and author into the "quotes" table of the database.
        '''
        try:
            self.conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote_text, quote_author))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error while inserting quote: {e}")

    def email_exists(self, email):
        '''
        Checks if the passed email  address is in the "emails" table within the database.
        Returns True if found, False if not.
        '''
        try:
            cursor = self.conn.execute('SELECT COUNT(*) FROM emails WHERE email = ?', (email,))
            count = cursor.fetchone()[0]
            if count == 0:
                return False
            else:
                return True
        except sqlite3.Error as e:
            print(f"Error while checking if email existsL {e}")

    def insert_email(self, email):
        '''
        Inserts the passed email address into the "email" table of the database if it is not a repeat.
        '''
        try:
            if self.email_exists(email):
                print(f"Subscriber {email} already exists in the list.")
            else:
                self.conn.execute('INSERT INTO emails (email) VALUES (?)', (email,))
                self.conn.commit()
                print(f"Subscriber {email} added successfully!")
        except sqlite3.Error as e:
            print(f"Error while inserting email: {e}")

    def get_emails(self):
        '''
        Returns a list of the email addresses found in the emails table of the database:
        \n\t["email@example.com","email2@example.com"]
        '''
        try:
            cursor = self.conn.execute('SELECT email FROM emails')
            emails = [row[0] for row in cursor.fetchall()]
            return emails
        except sqlite3.Error as e:
            print(f"Error while retrieving emails: {e}")
            return []
        
    def delete_email(self, email):
        '''
        Deletes the passed email from the "email" database.
        '''
        try:
            if self.email_exists(email):
                self.conn.execute('DELETE FROM emails WHERE email = ?', (email,))
                self.conn.commit()
                print(f"Email {email} succesfully deleted.")
            else:
                print(f"Email {email} does not exist in the database.")
        except sqlite3.Error as e:
            print(f"Error while receiving results: {e}")

    def __del__(self):
        '''
        Destructor closes the db.
        '''
        self.conn.close()