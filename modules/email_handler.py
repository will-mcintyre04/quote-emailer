import smtplib
from email.message import EmailMessage
from modules.path_helper import get_direct_path
import os

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
        name of the html template

    Methods
    -------
    send(subject : str, quote : str, author : str, recipients : list[str])
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
        recipient : list[modules.models.Email]
            list of modules.models.Email objects representing recipients

        Exceptions
        ----------
        smtplib.SMTPException
            if there is an error sending the email to the recipient

        '''
        if not recipients:
            print("Recipient list is empty. No emails sent.")
            return
        try:
            # Open the html template from the template folder
            with open(get_direct_path(os.path.join("templates", self.html_template)), 'r') as html_file:
                html_template = html_file.read()

            # Send the emails to each recipient
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                smtp.login(self.email, self.password)
                
                for recipient in recipients:
                    msg = EmailMessage()
                    msg['From'] = self.email
                    msg['Subject'] = subject
                    msg['To'] = recipient.address

                    formatted_html = html_template.format(
                        quote=quote,
                        author=author,
                        email=recipient.address,
                        link=f"willymac.pythonanywhere.com/delete_email/{recipient.address}"
                    )
                    msg.set_content(formatted_html, subtype='html')
                    smtp.send_message(msg)

                    print(f"Email sent to {recipient.address} succesfully")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")