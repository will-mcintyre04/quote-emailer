import sqlite3
from modules.path_helper import get_direct_path

class Database:
    '''
    Handler that works with the quotes.db local database.

    Attributes
    ----------
    conn : sqlite.connect()
        sqlite connection to the database file
    database_file : str
        direct path of the "quotes.db" database file

    Methods
    -------
    connect()
        connects to the database file and initializes tables
    create_tables()
        creates "emails" and "quotes" tables in db if they do not exist
    insert_quote(quote_text : str, quote_author : str)
        inserts quote and author into db
    email_exists(email : str)
        if the email exists in the database, return true
    insert_emails(email : list)
        inserts emails into db
    get_emails()
        returns list of emails in "email" table of db
    delete_emails(email : str)
        deleted email from the  db
    '''

    database_file = get_direct_path("quotes.db")

    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        '''
        Connects to database file and initializes tables.

        Exceptions
        ----------
        sqlite3.Error
            if there is an error connecting to the database
        '''

        try:
            self.conn = sqlite3.connect(self.database_file)
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        '''
        Creates two tables in the db if they do not exist: "emails" and "quotes".
        \n\t"quotes" contains an id (primary key), and quote and author attributes
        \n\t"emails" contains an id (primary key), and email attributes

        Exceptions
        ----------
        sqlite3.Error
            if there is an error creating tables
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
        
        Parameters
        ----------
        quote_text : str
            quote string
        quote_author
            quote author string
        
        Exceptions
        ----------
        sqlite3.Error
            if there is an error inserting quote
        '''

        try:
            self.conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote_text, quote_author))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error while inserting quote: {e}")

    def email_exists(self, email):
        '''
        If the passed email  address is in the "emails" table within the database, return True

        Parameters
        ----------
        email : str
            email address to be checked

        Exceptions
        ----------
        sqlite3.Error
            if there is an error checking database
        '''

        try:
            cursor = self.conn.execute('SELECT COUNT(*) FROM emails WHERE email = ?', (email,))
            count = cursor.fetchone()[0]
            if count == 0:
                return False
            else:
                return True
        except sqlite3.Error as e:
            print(f"Error while checking if email exists {e}")

    def insert_emails(self, emails):
        '''
        Inserts the passed email addresses into the "email" table of the database if it is not a repeat.
        
        Parameters
        ----------
        emails : list<string>
            list of email addresses to be inserted

        Exceptions
        ----------
        sqlite3.Error
            if there is an error inserting into the database
        '''

        try:
            for email in emails:
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

        Returns
        -------
        list<string>
            a list of strings representing emails in the database

        Exceptions
        ----------
        sqlite3.Error
            if there is an email retrieving from the database
        '''

        try:
            cursor = self.conn.execute('SELECT email FROM emails')
            emails = [row[0] for row in cursor.fetchall()]
            return emails
        except sqlite3.Error as e:
            print(f"Error while retrieving emails: {e}")
            return []
        
    def delete_emails(self, emails):
        '''
        Deletes the passed emails from the "email" table of database.

        Parameters
        ----------
        emails : list<string>
            list of emails to be deleted from database
        
        Exceptions
        ----------
        sqlite3.Error
            if there os an error deleting from database
        '''

        try:
            for email in emails:
                if self.email_exists(email):
                    self.conn.execute('DELETE FROM emails WHERE email = ?', (email,))
                    self.conn.commit()
                    print(f"Email {email} succesfully deleted.")
            else:
                print(f"Email {email} does not exist in the database.")
        except sqlite3.Error as e:
            print(f"Error while receiving results: {e}")

    def __del__(self):
        '''Destructor closes the db.'''
        self.conn.close()