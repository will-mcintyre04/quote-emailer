from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import Email, Base, Quote
from contextlib import contextmanager
import os
import sys

class DatabaseHandler:
    '''
    Handler that connects to and edits the database dependant on environment.
    '''
    def __init__(self, database_type):
        """
        Establishes a connection to the engine and creates a sessionmaker
        for database interaction.

        If the database type is 'production', connects to the PythonAnywhere 
        MySQL database.
        If the database type is 'development', connects to SQLite.
        """

        connect_args = {}
        database_type = database_type.upper()
        if database_type in ["DEVELOPMENT", "DEV"]:
            database_url = "sqlite:///emails.db"
        elif database_type in ["PRODUCTION", "PROD"]:
            database_url = os.getenv("MYSQL_URI")
            if not database_url:
                raise ValueError("No production MySQL URI provided.")
            connect_args = {"connect_timeout" : 5},
        else:
            raise ValueError("Invalid database configuration provided. \
                             Choose 'development' or 'production'.")
        
        # Factory that establishes connection to db
        self.engine = create_engine(
            database_url,
            connect_args=connect_args,
            pool_pre_ping=True
        )
        # Individual connections to db for abstract/high level interaction
        self.Session = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

        self.connect()

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def connect(self):
        """
        Connects the the database and initializes tables if they do not exist.
        """

        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def insert_emails(self, emails):
        """
        Inserts the list of emails into the database.
        """
        try:
            with self.session_scope() as session:
                for email_addr in emails:
                    exists = session.query(Email).filter_by(address=email_addr).first()
                    if exists:
                        print(f"Subscriber {email_addr} already exists in the list.")
                    else:
                        session.add(Email(address=email_addr))
                        print(f"Subscriber {email_addr} added successfully!")
        except Exception as e:
            print(f"Error while inserting email: {e}")

    def delete_emails(self, emails):
        """
        Deletes the list of emails from the database.
        """
        try:
            with self.session_scope() as session:
                for email_addr in emails:
                    email = session.query(Email).filter_by(address=email_addr).first()
                    if email:
                        session.delete(email)
                        print(f"Email {email_addr} successfully deleted.")
                    else:
                        print(f"Email {email_addr} does not exist.")
        except Exception as e:
            print(f"Error while deleting emails: {e}")

    def get_emails(self):
        """
        Returns a list of modules.models.Email objects from the database.
        """ 
        try:
            with self.session_scope() as session:
                return session.query(Email).all()
        except Exception as e:
            print(f"Error while retrieving emails: {e}")
            return []
    
    def upload_quotes_to_db(self, quotes):
        '''
        Uploads a list of quotes to the database.
        '''
        try:
            with self.session_scope() as session:
                for q in quotes:
                    session.add(Quote(quote=q['quote'], author=q['author']))
                return True
        except Exception as e:
            print(f"Error while inserting quotes: {e}")
            return False

    def get_first_quote(self):
        '''
        Retrieves the first quote from the database.
        '''
        try:
            with self.session_scope() as session:
                return session.query(Quote).first()
        except Exception as e:
            print(f"Error while getting first quote: {e}")
            return None
    
    def delete_first_quote(self):
        '''
        Deletes the first quote from the database.
        '''
        try:
            with self.session_scope() as session:
                quote = session.query(Quote).first()
                if quote:
                    session.delete(quote)
                    return True
                return False
        except Exception as e:
            print(f"Error while deleting first quote: {e}")
            return False