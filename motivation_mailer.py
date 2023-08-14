import argparse
from modules.quote_bot import QuoteBot
import os
from dotenv import load_dotenv

def update_env_variable(variable_name, new_value):
    env_file_path = ".env"

    # Read the existing content
    with open(env_file_path, "r") as f:
        lines = f.readlines()

    # Update the specified variable
    updated_lines = []
    variable_updated = False
    for line in lines:
        if line.startswith(variable_name + "="):
            updated_lines.append(f"{variable_name}={new_value}\n")
            variable_updated = True
        else:
            updated_lines.append(line)

    # If the variable wasn't found, add it to the end of the file
    if not variable_updated:
        updated_lines.append(f"{variable_name}={new_value}\n")

    # Write the updated content back to the file
    with open(env_file_path, "w") as f:
        f.writelines(updated_lines)

def check_none(password, email, db_filename):
    if not email:
        raise ValueError("Sending email address is required.")
    elif not password:
        raise ValueError("Email password is required.")
    elif not db_filename:
        raise ValueError("Database filename is required.")


def config_env(args):
    PASS = args.password or os.getenv('GMAIL_PASSWORD')
    EMAIL = args.email or os.getenv('GMAIL_ADDRESS')
    DB_FILENAME = args.database or os.getenv('DB_NAME')

    check_none(PASS, EMAIL, DB_FILENAME)

    if args.database and not args.database.endswith(".db"):
        raise ValueError("Invalid configuration: Database filename must have the .db extension")

    # Update environment variables if new values provided
    if args.email:
        update_env_variable("GMAIL_ADDRESS", args.email)
    if args.password:
        update_env_variable("GMAIL_PASSWORD", args.password)
    if args.database:
        update_env_variable("DB_NAME", args.database)

    return EMAIL, PASS, DB_FILENAME

def main():
    try:
            
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Sends motivational quotes fetched from ZenQuotes API\
                                        (https://zenquotes.io/) to email addresses stored in a local database.")
        parser.add_argument("--list", "-l", action="store_true", help="List all subscribers")
        parser.add_argument("--add", "-a", type=str, nargs="+",
                            help="Email address(es) to add to database")
        parser.add_argument("--delete", "-d", type=str, nargs="+",
                            help="Email address(es) to delete from database")
        parser.add_argument("--database", "-db", type=str, help="Custom database file name")
        parser.add_argument("--email", "-e", type=str, help="Sending email address")
        parser.add_argument("--password", "-p", type=str, help="Email password")

        args = parser.parse_args()

        # Load and config environment variables
        load_dotenv()
        EMAIL, PASS, DB_FILENAME = config_env(args)

        # Create Bot
        bot = QuoteBot(EMAIL, PASS, DB_FILENAME)

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
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()