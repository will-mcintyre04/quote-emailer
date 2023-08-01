import argparse
import time

from quote import Quote

class QuoteBot:
    def __init__(self):
        self.quote_handler = Quote()
        # self.db = Database()
        # self.email_handler = EmailHandler()
    def daily_quote(self):
        quote, author = self.quote_handler.fetch()
        print(quote, author)

if __name__ == "__main__":
    ## Create Bot
    bot = QuoteBot()

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
        bot.daily_quote()