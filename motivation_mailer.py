import argparse
from modules.quote_bot import QuoteBot
import os
from dotenv import load_dotenv

def get_lines(file_path):
    """
    Returns a list of lines in a file.

    Parameters
    ----------
    file_path : str
        the path to the file.

    Returns
    -------
    list
        list containing the lines read from the file.
    """

    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines

def write_to_file(file_path, lines):
    """
    Write lines to a file.

    Parameters
    ----------
    file_path : str
        the path to the file.
    lines : list<string>
        the lines to write to the file.
    """

    with open(file_path, "w") as f:
        f.writelines(lines)


def update_env_variable(variable_name, new_value):
    """
    Update an environment variable in the .env file.

    Parameters
    ----------
    variable_name : str
        the name of the environment variable to update.
    new_value : str
        the new value to assign to the environment variable.
    """

    env_file_path = os.path.join(".", ".env")
    lines = get_lines(env_file_path)

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

    write_to_file(".env", updated_lines)

def check_none(password, email, db_filename):
    """
    Checks if required values are provided.

    Parameters
    ----------
    password : str
        email password
    email : str
        sending email address
    db_filename : str
        name of the database file
    
    Raises
    ------
    ValueError
        if a value is not provided
    """

    if not email:
        raise ValueError("Sending email address is required.")
    elif not password:
        raise ValueError("Email password is required.")
    elif not db_filename:
        raise ValueError("Database filename is required.")


def check_file_exists(file_name):
    '''
    Checks if the file name exists in the working directory.

    Parameters
    ----------
    file_name : str
        name of the file to check.
    
    Raises
    ------
    FileNotFoundError
        if the file does not exist
    '''
    if not os.path.exists(os.path.join(".", file_name)):
        raise FileNotFoundError(".env file not found.")

def config_env(args):
    '''
    Configures and checks environment variables and updates them if arguments are inputted.

    Parameters
    ----------
    args : argparse.Namespace
        parsed command-line arguments

    Returns
    -------
    str, str, str
        the email, password, and database filename
    
    Raises
    ------
    ValueError
        if an invalid database file is detected
    '''
    # Check if .env file exists
    check_file_exists(".env")

    # Update environment variables if new values provided
    if args.email:
        update_env_variable("GMAIL_ADDRESS", args.email)
    if args.password:
        update_env_variable("GMAIL_PASSWORD", args.password)
    if args.database:
        update_env_variable("DB_NAME", args.database)

    # Fetch env variables
    load_dotenv()
    PASS = args.password or os.getenv('GMAIL_PASSWORD')
    EMAIL = args.email or os.getenv('GMAIL_ADDRESS')
    DB_FILENAME = args.database or os.getenv('DB_NAME')

    # Check that all variables are collected
    check_none(PASS, EMAIL, DB_FILENAME)

    # Check database file validity
    if args.database and not args.database.endswith(".db"):
        raise ValueError("Invalid configuration: Database filename must have the .db extension")


    return EMAIL, PASS, DB_FILENAME

def main():
    """
    Entry point of the script. Parses command-line arguments, configures environment,
    and performs actions based on the provided arguments. Also catches and displays errors.
    """

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
        parser.add_argument("--password", "-p", type=str, help="Gmail application password")

        args = parser.parse_args()

        # Load and config environment variables
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

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()