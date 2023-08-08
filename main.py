import argparse
from quote import Quote
from email_handler import EmailHandler
from database import Database
import os
from dotenv import load_dotenv

class QuoteBot:
    '''
    Root bot that encapsualtes all functionality of the app.
    
    - Sends emails to email addresses stored in the local database "quotes.db" with motivational
    quotes fetched from the ZenQuotes API (https://zenquotes.io/)
    - Edits and displays "email" table data, allowing insertion and deletion of subsriber emails.
    - Stores all sent quotes in the "quotes" table of the database, allowing viewing of past quotes sent.
    '''
    def __init__(self, email, password):
        self.quote_handler = Quote()
        self.db_handler = Database()
        self.email_handler = EmailHandler(email, password)

    def send_email(self):
        '''
        Sends an email fetched from the api to the emails stored in the database
        '''
        quote, author = self.quote_handler.fetch()
        if quote and author:
            emails = self.db_handler.get_emails()
            for email in emails:
                self.email_handler.send("Quote of the Day", f"{quote} by {author}", email)

    def add_subscriber(self, email):
        '''
        Inserts the passed email into the database
        '''
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
        '''
        Deletes the passed email from the database
        '''
        self.db_handler.delete_email(email)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Quote of the Day Bot")
    parser.add_argument("--list", action="store_true", help="List all subscribers")
    parser.add_argument("--email", type=str, help="Email address to add to database")
    parser.add_argument("--delete", type=str, help="Email address to delete from database")

    args = parser.parse_args()

    # Config environment variables
    load_dotenv()
    PASS = os.getenv('GMAIL_PASSWORD')
    EMAIL = 'william.d.j.mcintyre@gmail.com'

    # Create Bot
    bot = QuoteBot(EMAIL, PASS)

    # Check for arguments and impliment respective requests
    if args.email:
        bot.add_subscriber(args.email)
    elif args.list:
        bot.list_subscribers()
    elif args.delete:
        bot.delete_subscriber(args.delete)
    
    # If no command-line arguments, send a daily quote
    else:
        bot.add_subscriber("william.d.j.mcintyre@gmail.com")

if __name__ == "__main__":
    main()