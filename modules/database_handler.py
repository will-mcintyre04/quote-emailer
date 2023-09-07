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
    database_type : str
        The configuration environment (production or development)
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