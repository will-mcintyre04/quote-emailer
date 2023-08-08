import smtplib
from email.message import EmailMessage
from resources.path_helper import get_direct_path

class EmailHandler:
    '''
    Handler for sending emails.
    '''
    def __init__(self, email, password):
        '''
        Stores email and password of sender.
        '''
        self.email = email
        self.password = password
        self.html_template = "email_template.html"
    def send(self, subject, quote, author, recipient):
        '''
        Sends an email to the passed recipient with the passed subject and body message.
        '''
        try:
            msg = EmailMessage()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = subject

            # Read the HTML template and format it with the quote and author
            with open(get_direct_path(self.html_template), 'r') as html_file:
                html_template = html_file.read()
                formatted_html = html_template.format(quote=quote, author=author)

            msg.set_content(formatted_html, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email, self.password) 
                smtp.send_message(msg)
                print(f"Email sent to {recipient} successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email to {recipient}: {e}")