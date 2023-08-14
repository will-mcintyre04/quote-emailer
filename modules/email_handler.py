import smtplib
from email.message import EmailMessage
from modules.path_helper import get_direct_path

class EmailHandler:
    '''
    Handler for sending emails.

    Attributes
    ----------
    email : str
        the address of the sending email
    password : str
        the password of the sending email
    html_template : str
        the sound that the animal makes

    Methods
    -------
    send(subject, quote, author, recipient)
        Sends a formatted email to the recipient with the given subject and quote/author
    '''

    html_template = "email_template.html"

    def __init__(self, email, password):
        '''
        Parameters
        ----------
        email : str
            the address of the sending email
        password : str
            the password of the sending email
        '''
        self.email = email
        self.password = password

    def send(self, subject, quote, author, recipients):
        '''
        Sends a formatted email to a list of recipients with a quote.

        Parameters
        ----------
        subject : str
            the subject of the email message
        quote : str
            quote string
        author : str
            name of the author of the quote
        recipient : list
            list of recipient email addresses

        Exceptions
        ----------
        smtplib.SMTPException
            if there is an error sending the email to the recipient

        '''
        if not recipients:
            print("Recipient list is empty. No emails sent.")
            return
        try:
            # Read the HTML template and format it with the quote and author
            with open(get_direct_path(self.html_template), 'r') as html_file:
                html_template = html_file.read()
                formatted_html = html_template.format(quote=quote, author=author)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                smtp.login(self.email, self.password)

                for recipient in recipients:
                    msg = EmailMessage()
                    msg['From'] = self.email
                    msg['Subject'] = subject
                    msg['To'] = recipient


                    msg.set_content(formatted_html, subtype='html')
                    smtp.send_message(msg)

                    print(f"Email sent to {recipient} succesfully")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")