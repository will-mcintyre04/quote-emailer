import sys
import schedule
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
    bot = QuoteBot()
    bot.daily_quote()