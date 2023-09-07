import argparse

def parse_arguments():
    '''
    Parse command-line arguments and returns the parsed arguments.

    Returns
    -------
    argparse.Namespace
        an object containing the command-line arguments
    '''
    parser = argparse.ArgumentParser(
            description=("Motivation Mailer: Send quotes fetched from ZenQuotes"
                         "API (https://zenquotes.io/) to email addresses stored"
                         "in a database."
            ),
            epilog=("For further documentation and source code, view:"
                    "https://github.com/will-mcintyre04/quote-emailer"
            )
    )

    parser.add_argument("--status", "-s", action="store_true",
                        help="Displays configuration environment and \
                              lists all subscribers")
    parser.add_argument("--add", "-a", type=str, nargs="+",
                        help="Email address(es) to add to database")
    parser.add_argument("--delete", "-d", type=str, nargs="+",
                        help="Email address(es) to delete from database")
    parser.add_argument("--database", "-db", type=str,
                        help="Sets database configuration ('production' or \
                             'development')")
    parser.add_argument("--email", "-e", type=str,
                        help="Sets the sending email address")
    parser.add_argument("--password", "-p", type=str,
                        help="Sets the sending email password")
    parser.add_argument("--send", action="store_true",
                        help="Sends emails to the emails stored in the db")
    
    return parser.parse_args()