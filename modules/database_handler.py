# import sqlite3
# from modules.path_helper import get_direct_path

# class DatabaseHandler:
#     '''
#     Handler that works with the quotes.db local database.

#     Attributes
#     ----------
#     conn : sqlite.connect()
#         sqlite connection to the database file
#     database_file : str
#         direct path of the "quotes.db" database file

#     Methods
#     -------
#     connect()
#         connects to the database file and initializes tables
#     create_tables()
#         creates "emails" and "quotes" tables in db if they do not exist
#     insert_quote(quote_text : str, quote_author : str)
#         inserts quote and author into db
#     email_exists(email : str)
#         if the email exists in the database, return true
#     insert_emails(email : list)
#         inserts emails into db
#     get_emails()
#         returns list of emails in "email" table of db
#     delete_emails(email : str)
#         deleted email from the  db
#     '''

#     def __init__(self, database):
#         self.conn = None
#         self.database_file = get_direct_path(database)
#         self.connect()

#     def connect(self):
#         '''
#         Connects to database file and initializes tables.

#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an error connecting to the database
#         '''

#         try:
#             self.conn = sqlite3.connect(self.database_file)
#             self.create_tables()
#         except sqlite3.Error as e:
#             print(f"Error connecting to database: {e}")

#     def create_tables(self):
#         '''
#         Creates two tables in the db if they do not exist: "emails" and "quotes".
#         \n\t"quotes" contains an id (primary key), and quote and author attributes
#         \n\t"emails" contains an id (primary key), and email attributes

#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an error creating tables
#         '''

#         try:
#             self.conn.execute('''
#                 CREATE TABLE IF NOT EXISTS quotes (
#                     id INTEGER PRIMARY KEY,
#                     quote TEXT,
#                     author TEXT
#                 )
#             ''')
#             self.conn.execute('''
#                 CREATE TABLE IF NOT EXISTS emails (
#                     id INTEGER PRIMARY KEY,
#                     email TEXT
#                 )
#             ''')
#             self.conn.commit()
#         except sqlite3.Error as e:
#             print(f"Error while creating tables: {e}")

#     def insert_quote(self, quote_text, quote_author):
#         '''
#         Inserts the passed quote text and author into the "quotes" table of the database.
        
#         Parameters
#         ----------
#         quote_text : str
#             quote string
#         quote_author
#             quote author string
        
#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an error inserting quote
#         '''

#         try:
#             self.conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote_text, quote_author))
#             self.conn.commit()
#         except sqlite3.Error as e:
#             print(f"Error while inserting quote: {e}")

#     def email_exists(self, email):
#         '''
#         If the passed email  address is in the "emails" table within the database, return True

#         Parameters
#         ----------
#         email : str
#             email address to be checked

#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an error checking database
#         '''

#         try:
#             cursor = self.conn.execute('SELECT COUNT(*) FROM emails WHERE email = ?', (email,))
#             count = cursor.fetchone()[0]
#             if count == 0:
#                 return False
#             else:
#                 return True
#         except sqlite3.Error as e:
#             print(f"Error while checking if email exists {e}")

#     def insert_emails(self, emails):
#         '''
#         Inserts the passed email addresses into the "email" table of the database if it is not a repeat.
        
#         Parameters
#         ----------
#         emails : list<string>
#             list of email addresses to be inserted

#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an error inserting into the database
#         '''

#         try:
#             for email in emails:
#                 if self.email_exists(email):
#                     print(f"Subscriber {email} already exists in the list.")
#                 else:
#                     self.conn.execute('INSERT INTO emails (email) VALUES (?)', (email,))
#                     self.conn.commit()
#                     print(f"Subscriber {email} added successfully!")
#         except sqlite3.Error as e:
#             print(f"Error while inserting email: {e}")

#     def get_emails(self):
#         '''
#         Returns a list of the email addresses found in the emails table of the database:
#         \n\t["email@example.com","email2@example.com"]

#         Returns
#         -------
#         list<string>
#             a list of strings representing emails in the database

#         Exceptions
#         ----------
#         sqlite3.Error
#             if there is an email retrieving from the database
#         '''

#         try:
#             cursor = self.conn.execute('SELECT email FROM emails')
#             emails = [row[0] for row in cursor.fetchall()]
#             return emails
#         except sqlite3.Error as e:
#             print(f"Error while retrieving emails: {e}")
#             return []
        
#     def delete_emails(self, emails):
#         '''
#         Deletes the passed emails from the "email" table of database.

#         Parameters
#         ----------
#         emails : list<string>
#             list of emails to be deleted from database
        
#         Exceptions
#         ----------
#         sqlite3.Error
#             if there os an error deleting from database
#         '''

#         try:
#             for email in emails:
#                 if self.email_exists(email):
#                     self.conn.execute('DELETE FROM emails WHERE email = ?', (email,))
#                     self.conn.commit()
#                     print(f"Email {email} succesfully deleted.")
#                 else:
#                     print(f"Email {email} does not exist in the database.")
#         except sqlite3.Error as e:
#             print(f"Error while receiving results: {e}")

#     def __del__(self):
#         '''Destructor closes the db.'''
#         self.conn.close()
# database_handler.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import Email, Base
import os

class DatabaseHandler:
    '''
     Handler that connects to and edits the database dependant on environment.

     Attributes
     ----------
     engine : sqlalchemy.engine.base.Engine
        The database engine that establishes the connection to the database.
    Session : sqlalchemy.orm.session.Session
        Session factory for creating individual connections to the database.

    Methods
    -------
    connect()
        Connects to the database and initializes tables if they do not exist.
    email_exists(email: str) -> bool
        Checks if an email exists in the database.
    insert_emails(emails: list)
        Inserts new emails into the database.
    delete_emails(emails: list)
        Deletes emails from the database.
    get_emails() -> list
        Retrieves a list of emails from the database.

    Parameters
    ----------
    database_url : str
        The URL to connect to the database.
     '''
    def __init__(self, database_type):
        database_type = database_type.upper()
        if database_type in ["DEVELOPMENT", "DEV"]:
            database_url = "sqlite:///emails.db"
        elif database_type in ["PRODUCTION", "PROD"]:
            database_url = os.getenv("MYSQL_URI")
        else:
            raise ValueError("Invalid database_type provided. Choose 'development' or 'production'.")
        
        self.engine = create_engine(database_url) # Factory that establishes connection to db
        self.Session = sessionmaker(bind=self.engine) # Individual connections to db for abstract/high level interaction

        self.connect()

    def connect(self):
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def email_exists(self, email):
        try:
            session = self.Session()
            count = session.query(Email).filter_by(email=email).count()
            return count > 0
        except Exception as e:
            print(f"Error while checking if email exists: {e}")
            return False

    def insert_emails(self, emails):
        try:
            session = self.Session()
            for email in emails:
                if self.email_exists(email):
                    print(f"Subscriber {email} already exists in the list.")
                else:
                    new_email = Email(email=email)
                    session.add(new_email)
                    session.commit()
                    print(f"Subscriber {email} added successfully!")
        except Exception as e:
            print(f"Error while inserting email: {e}")

    def delete_emails(self, emails):
        try:
            session = self.Session()
            for email in emails:
                if self.email_exists(email):
                    email_to_delete = session.query(Email).filter_by(email=email).first()
                    session.delete(email_to_delete)
                    session.commit()
                    print(f"Email {email} successfully deleted.")
                else:
                    print(f"Email {email} does not exist in the database.")
        except Exception as e:
            print(f"Error while deleting email: {e}")

    def get_emails(self):
        try:
            session = self.Session()
            emails = session.query(Email).all()
            return emails
        except Exception as e:
            print(f"Error while retrieving emails: {e}")
            return []

if __name__ == "__main__":
    # Instantiate the DatabaseHandler class with a new SQLite database URL
    sqlite_db_url = 'sqlite:///test_db.db'
    database_handler = DatabaseHandler(sqlite_db_url)

    # Insert some emails
    new_emails = ["user1@example.com", "user2@example.com"]
    database_handler.insert_emails(new_emails)

    # Print the quotes and emails
    emails = database_handler.get_emails()


    print("Emails:")
    for email in emails:
        print(email.email)