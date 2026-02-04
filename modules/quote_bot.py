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
        '''
        Sends quote of the day email to all stored email addresses

        Returns
        -------
        None
            This method does not return a value. It either sends an email or logs an error message.
            
        Exceptions
        ----------
        Exception
            This method assumes that the individual handler methods (e.g., `get_first_quote`, `fetch_quotes`, 
            `upload_quotes_to_db`, `get_emails`, and `send`) handle their own exceptions. Any issues within those 
            methods will be logged or handled accordingly.
        '''
        
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
        
        # Delete the quote after getting sent
        self.db_handler.delete_first_quote()

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