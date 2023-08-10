from modules.email_handler import EmailHandler
from modules.quote import Quote
from modules.database import Database

class QuoteBot:
    '''
    Root bot that encapsualtes all functionality of the app.
    
    - Sends emails to email addresses stored in the local database "quotes.db" with motivational
    quotes fetched from the ZenQuotes API (https://zenquotes.io/)
    - Edits and displays "email" table data, allowing insertion and deletion of subsriber emails.
    - Stores all sent quotes in the "quotes" table of the database, allowing viewing of past quotes sent.

    Attributes
    ----------
    quote_handler : Quote()
        handler for fetching quotes
    db_handler : Database() 
        handler for interacting the database
    email_handler = EmailHandler()
        handler for sending emails

    Methods
    ------
    send_email()
        fetches quote from api and sends email to all addresses in database
    add_subscriber(email : str)
        add the email into the database
    list_subscribers
        prints the list of subscribers in the database to the terminal
    delete_subscriber(email)
        deletes the email from the database
    '''

    def __init__(self, email, password):
        '''
        Parameters
        ----------
        email : str
            address of the sender email
        password : str
            password of the sender email
        '''
        self.quote_handler = Quote()
        self.db_handler = Database()
        self.email_handler = EmailHandler(email, password)

    def send_email(self):
        '''Sends an email fetched from the api to the emails stored in the database'''
        quote, author = self.quote_handler.fetch()
        if quote and author:
            emails = self.db_handler.get_emails()
            for email in emails:
                self.email_handler.send("Quote of the Day", quote, author, email)

    def add_subscriber(self, email):
        '''Inserts the passed email into the database'''
        self.db_handler.insert_email(email)

    def list_subscribers(self):
        '''
        Prints the list of all subscribers (emails in database) to the user.

        Format Example:
        1. email1@example.com
        2. email2@example.com
        '''

        subscribers = self.db_handler.get_emails()
        if subscribers:
            print("List of Subscribers:")
            for i, subscriber_email in enumerate(subscribers, 1):
                print(f"{i}. {subscriber_email}")
        else:
            print("No subscribers in the list.")
    
    def delete_subscriber(self, email):
        '''Deletes the passed email from the database'''
        self.db_handler.delete_email(email)