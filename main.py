import argparse
from modules.quote_bot import QuoteBot
import os
from dotenv import load_dotenv

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
    if args.list:
        bot.list_subscribers()
    elif args.email:
        bot.add_subscriber(args.email)
    elif args.delete:
        bot.delete_subscriber(args.delete)
    
    # If no command-line arguments, send a daily quote
    else:
        bot.send_email()

if __name__ == "__main__":
    main()