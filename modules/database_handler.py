from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import Email, Base, Quote
import os

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

        Parameters
        ----------
        database_type : str
            the configuration for the database ('production' or 'development').
        
        Raises
        ------
        ValueError
            if the database configuration type is invalid or no production
            uri is inputted.
        """

        database_type = database_type.upper()
        if database_type in ["DEVELOPMENT", "DEV"]:
            database_url = "sqlite:///emails.db"
        elif database_type in ["PRODUCTION", "PROD"]:
            database_url = os.getenv("MYSQL_URI")
            if not database_url:
                raise ValueError("No production MySQL URI provided.")
        else:
            raise ValueError("Invalid database configuration provided. \
                             Choose 'development' or 'production'.")
        
        # Factory that establishes connection to db
        self.engine = create_engine(database_url)
        # Individual connections to db for abstract/high level interaction
        self.Session = sessionmaker(bind=self.engine)

        self.connect()

    def connect(self):
        """
        Connects the the database and initializes tables if they do not exist.

        Exceptions
        ----------
        Exception
            if there is an error while connecting to the database.
        """

        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def email_exists(self, email):
        """
        Checks if an email is in the database.

        Parameters
        ----------
        email : str
            email address to check.

        Returns
        -------
        bool
            true if the email exists in the database, otherwise false.

        Exceptions
        ---------
        Exception
            if there is an error while checking the email.
        """

        try:
            session = self.Session()
            count = session.query(Email).filter_by(address=email).count()
            return count > 0
        except Exception as e:
            print(f"Error while checking if email exists: {e}")
            return False

    def insert_emails(self, emails):
        """
        Inserts the list of emails into the database.

        Parameters
        ----------
        emails : list 
            list of email addresses to check.
        
        Exceptions
        ----------
            if there is an error while inserting.
        """

        try:
            session = self.Session()
            for email in emails:
                if self.email_exists(email):
                    print(f"Subscriber {email} already exists in the list.")
                else:
                    new_email = Email(address=email)
                    session.add(new_email)
                    session.commit()
                    print(f"Subscriber {email} added successfully!")
        except Exception as e:
            print(f"Error while inserting email: {e}")

    def delete_emails(self, emails):
        """
        Deletes the list of emails from the database.

        Parameters
        ----------
        emails : list
            list of email addresses to remove.
        
        Exceptions
        ----------
        Exception
            if there is an error while deleting.
        """

        try:
            session = self.Session()
            for email in emails:
                if self.email_exists(email):
                    email_to_delete = session.query(Email).filter_by(address=email).first()
                    session.delete(email_to_delete)
                    session.commit()
                    print(f"Email {email} successfully deleted.")
                else:
                    print(f"Email {email} does not exist in the database.")
        except Exception as e:
            print(f"Error while deleting email: {e}")

    def get_emails(self):
        """
        Returns a list of modules.models.Email objects from the database.

        Returns
        -------
        list
            returns a list of modules.models.Email objects in the database, empty list if empty.
        
        Exceptions
        ----------
        Exception
            if there is an error while retrieving emails.
        """

        try:
            session = self.Session()
            emails = session.query(Email).all()
            return emails
        except Exception as e:
            print(f"Error while retrieving emails: {e}")
            return []
    
    def upload_quotes_to_db(self, quotes):
        '''
        Uploads a list of quotes to the database.

        Parameters
        ----------
        quotes : list of dict
            A list of dictionaries, where each dictionary represents a quote with two keys:
            - 'quote': The text of the quote.
            - 'author': The author of the quote.
            
        Returns
        -------
        bool
            Returns `True` if all quotes were successfully uploaded to the database. 
            Returns `False` if an error occurred during the process.
            
        Exceptions
        ----------
        Exception
            Any exceptions raised during the database insertion process will be caught and logged. 
            The method will return `False` if an error occurs.
        '''

        try:
            session = self.Session()
            for quote in quotes:
                new_quote = Quote(quote = quote['quote'], author = quote['author']);
                session.add(new_quote)
                session.commit()
            return True
        except Exception as e:
            print(f"Error while inserting quotes into db: {e}")
            return False

    def get_first_quote(self):
        '''
        Retrieves the first quote from the database.

        Returns
        -------
        Quote or None
            The first quote object from the database if present, otherwise None.
            
        Exceptions
        ----------
        Exception
            If any error occurs while querying the database, an exception will be caught and printed.
        '''

        try:
            session = self.Session()
            quote = session.query(Quote).first()
            return quote
        except Exception as e:
            print(f"Error while getting the first quote from the db: {e}")
    
    def delete_first_quote(self):
        '''
        Deletes the first quote from the database.

        Returns
        -------
        bool
            Returns `True` if the first quote was successfully deleted. Returns `False` if there was an error 
            during the deletion process or if no quotes were found in the database.
            
        Exceptions
        ----------
        Exception
            Any exceptions raised during the deletion process will be caught, and an error message will be logged.
        '''

        try:
            session = self.Session()
            quote = session.query(Quote).first()
            session.delete(quote)
            session.commit()
            return True
        except Exception as e:
            print(f"Error while deleting the first quote from the db: {e}")
            return False