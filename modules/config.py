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
    lines : list[string]
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
        updated_lines.append(f"\n{variable_name}={new_value}")

    write_to_file(".env", updated_lines)

def check_none(password, email, db_config):
    """
    Checks if required values are provided.

    Parameters
    ----------
    password : str
        email password
    email : str
        sending email address
    db_config : str
        database configuration
    
    Raises
    ------
    ValueError
        if a value is not provided
    """

    if not email:
        raise ValueError("Sending email address is required.")
    elif not password:
        raise ValueError("Email password is required.")
    elif not db_config:
        raise ValueError("Database configuration is required.")

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
        the email, password, and database configuration
    '''

    # Update environment variables if new values provided
    if args.email:
        update_env_variable("GMAIL_ADDRESS", args.email)
    if args.password:
        update_env_variable("GMAIL_PASSWORD", args.password)
    if args.database:
        update_env_variable("DB_CONFIG", args.database)

    # Fetch env variables
    load_dotenv()
    PASS = args.password or os.getenv('GMAIL_PASSWORD')
    EMAIL = args.email or os.getenv('GMAIL_ADDRESS')
    DB_CONFIG = args.database or os.getenv('DB_CONFIG')

    # Check that all variables are collected
    check_none(PASS, EMAIL, DB_CONFIG)

    return EMAIL, PASS, DB_CONFIG