import argparse
from quote import Quote
from email_handler import EmailHandler
from database import Database
import os
from dotenv import load_dotenv

class QuoteBot:
    def __init__(self, email, password):
        self.quote_handler = Quote()
        self.db_handler = Database()
        self.email_handler = EmailHandler(email, password)
    def send_email(self):
    # Sends an email fetched from the api to the emails stored in the database
        quote, author = self.quote_handler.fetch()
        if quote and author:
            emails = self.db_handler.get_emails()
            for email in emails:
                self.email_handler.send("Quote of the Day", f"{quote} by {author}", email)

    def add_subscriber(self, email):
    # Insert the email into the database
        self.db_handler.insert_email(email)
    def list_subscribers(self):
    # List off all subscribers (emails within the database)
        subscribers = self.db_handler.get_emails()
        if subscribers:
            print("List of Subscribers:")
            for i, subscriber_email in enumerate(subscribers, 1):
                print(f"{i}. {subscriber_email}")
        else:
            print("No subscribers in the list.")

if __name__ == "__main__":
    ## Config environment variables
    load_dotenv()
    PASS = os.getenv('GMAIL_PASSWORD')
    EMAIL = 'william.d.j.mcintyre@gmail.com'

    ## Create Bot
    bot = QuoteBot(EMAIL, PASS)

    ## Parse command-line arguments
    parser = argparse.ArgumentParser(description="Quote of the Day Bot")
    parser.add_argument("--list", action="store_true", help="List all subscribers")
    parser.add_argument("--email", type=str, help="Email address to add to database")

    args = parser.parse_args()

    if args.email:
        bot.add_subscriber(args.email)
    elif args.list:
        bot.list_subscribers()
    
    ## If no command-line arguments, send a daily quote
    else:
        bot.add_subscriber("hi")