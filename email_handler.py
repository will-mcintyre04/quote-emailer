import smtplib
from email.message import EmailMessage

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
    def send(self, subject, body, recipient):
        '''
        Sends an email to the passed recipient with the passed subject and body message.
        '''
        try:
            msg = EmailMessage()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.set_content(body)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email, self.password) 
                smtp.send_message(msg)
                print(f"Email send to {recipient} successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email to {recipient}: {e}")