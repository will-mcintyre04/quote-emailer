from modules.email_handler import EmailHandler
from modules.quote_handler import QuoteHandler
from modules.database_handler import DatabaseHandler
import os

class QuoteBot:
    '''
    Root bot that encapsualtes all functionality of the app.
    
    - Sends emails to email addresses stored in the local database "quotes.db" with motivational
    quotes fetched from the ZenQuotes API (https://zenquotes.io/)
    - Edits and displays "email" table data, allowing insertion and deletion of subsriber emails.

    Attributes
    ----------
    quote_handler : QuoteHandler()
        handler for fetching quotes
    db_handler : DatabaseHandler() 
        handler for interacting the database
    email_handler = EmailHandler()
        handler for sending emails

    Methods
    ------
    send_email()
        fetches quote from api and sends email to all addresses in database
    add_subscribers(emails)
        add the emails into the database
    show_status()
        prints the current database configuration and lists the subscribers in the database to the terminal
    delete_subscribers(emails)
        deletes the emails from the database
    '''

    def __init__(self, email, password, database):
        '''
        Parameters
        ----------
        email : str
            address of the sender email
        password : str
            password of the sender email
        '''

        self.quote_handler = QuoteHandler()
        self.db_handler = DatabaseHandler(database)
        self.email_handler = EmailHandler(email, password)

    def send_email(self):
        '''Sends an email fetched from the api to the emails stored in the database'''
        quote = self.db_handler.get_first_quote()
        if not quote:
            quotes = self.quote_handler.fetch_quotes()

            if not self.db_handler.upload_quotes_to_db(quotes):
                return
            
            quote = self.db_handler.get_first_quote()
            if not quote:
                print("No quotes found in the database after uploading.")
                return
            
        emails = self.db_handler.get_emails()
        if not emails:
            print("No emails found in the database.")
            return 
        
        self.email_handler.send("Quote of the Day", quote.quote, quote.author, emails)

    def add_subscribers(self, emails):
        '''
        Inserts the passed emails into the database
        
        Parameters
        ----------
        emails : list<string>
            list of emails to add to database
        '''

        self.db_handler.insert_emails(emails)

    def show_status(self):
        '''
        Shows the current database configuration and prints the list of all subscribers
        (emails in database) to the user.

        Example
        -------

        Your current configuration environment: dev

        List of Subscribers:        
        1. email1@example.com
        2. email2@example.com
        '''

        db_config = os.getenv("DB_CONFIG")
        print(f"Your current configuration environment: {db_config}\n")
        subscribers = self.db_handler.get_emails()
        if subscribers:
            print("List of Subscribers:")
            for i, subscriber_email in enumerate(subscribers, 1):
                print(f"{i}. {subscriber_email.address}")
        else:
            print("No subscribers in the list.")
            return

    def delete_subscribers(self, emails):
        '''Deletes the passed email from the database'''
        self.db_handler.delete_emails(emails)