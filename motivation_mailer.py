import argparse
from modules.quote_bot import QuoteBot
from modules.config import config_env
from modules.parser import parse_arguments

def main():
    """
    Entry point of the script. Parses command-line arguments, configures environment,
    and performs actions based on the provided arguments. Also catches and displays errors.
    """

    try:   
        # Parse command-line arguments
        args = parse_arguments()

        # Load and config environment variables
        EMAIL, PASS, DB_CONFIG = config_env(args)

        # Create Bot
        bot = QuoteBot(EMAIL, PASS, DB_CONFIG)

        # Check for arguments and impliment respective requests
        if args.status:
            bot.show_status()
        if args.add:
            bot.add_subscribers(args.add)
        if args.delete:
            bot.delete_subscribers(args.delete)
        if args.send:
            bot.send_email()

    except Exception as e:
        print(f"Error: {e} \n\nUse '-h' or '--help' to show help.")

if __name__ == "__main__":
    main()