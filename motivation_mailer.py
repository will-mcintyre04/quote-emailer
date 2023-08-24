import argparse
from modules.quote_bot import QuoteBot
from modules.config import config_env

def main():
    """
    Entry point of the script. Parses command-line arguments, configures environment,
    and performs actions based on the provided arguments. Also catches and displays errors.
    """

    try:   
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Motivation Mailer: Send quotes fetched from ZenQuotes API\
                                            (https://zenquotes.io/) to email addresses stored in a database.",
                                        epilog='For further documentation and source code, view: \
                                            https://github.com/will-mcintyre04/quote-emailer')
        parser.add_argument("--status", "-s", action="store_true",
                            help="Displays configuration environment and lists all subscribers")
        parser.add_argument("--add", "-a", type=str, nargs="+",
                            help="Email address(es) to add to database")
        parser.add_argument("--delete", "-d", type=str, nargs="+",
                            help="Email address(es) to delete from database")
        parser.add_argument("--database", "-db", type=str,
                            help="Sets database configuration ('production' or 'development')")
        parser.add_argument("--email", "-e", type=str, help="Sets the sending email address")
        parser.add_argument("--password", "-p", type=str, help="Sets the sending email password")

        args = parser.parse_args()

        # Load and config environment variables
        EMAIL, PASS, DB_CONFIG = config_env(args)

        # Create Bot
        bot = QuoteBot(EMAIL, PASS, DB_CONFIG)

        # Check for arguments and impliment respective requests
        if args.status:
            bot.show_status()
        elif args.add:
            bot.add_subscribers(args.add)
        elif args.delete:
            bot.delete_subscribers(args.delete)
        # If no command-line arguments, send a daily quote
        else:
            bot.send_email()

    except Exception as e:
        print(f"Error: {e} \n\nUse '-h' or '--help' to show help.")

if __name__ == "__main__":
    main()