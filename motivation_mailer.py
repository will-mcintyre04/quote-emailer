import argparse
from modules.quote_bot import QuoteBot
import os
from dotenv import load_dotenv

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Sends motivational quotes fetched from ZenQuotes API\
                                     (https://zenquotes.io/) to email addresses stored in a local database.")
    parser.add_argument("--list", "-l", action="store_true", help="List all subscribers")
    parser.add_argument("--add", "-a", type=str, nargs="+",
                        help="Email address(es) to add to database")
    parser.add_argument("--delete", "-d", type=str, nargs="+",
                        help="Email address(es) to delete from database")

    args = parser.parse_args()

    # Config environment variables
    load_dotenv()
    PASS = os.getenv('GMAIL_PASSWORD')
    EMAIL = 'william.d.j.mcintyre@gmail.com'

    # Create Bot
    bot = QuoteBot(EMAIL, PASS)

    # Check for arguments and impliment respective requests
    if args.list:
        bot.list_subscribers()
    elif args.add:
        bot.add_subscribers(args.add)
    elif args.delete:
        bot.delete_subscribers(args.delete)

    # If no command-line arguments, send a daily quote
    else:
        bot.send_email()

if __name__ == "__main__":
    main()