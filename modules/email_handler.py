import smtplib
from email.message import EmailMessage
from modules.path_helper import get_direct_path
import os

class EmailHandler:
    '''
    Handler for sending emails.
    '''

    html_template_file = "email_template.html"

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, subject, quote, author, recipients):
        '''
        Sends a formatted email to a list of recipients with a quote.
        '''
        if not recipients:
            print("Recipient list is empty. No emails sent.")
            return
        try:
            with open(get_direct_path(os.path.join("templates", self.html_template_file)), 'r') as html_file:
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
        except FileNotFoundError:
            print(f"Template file not found at {self.html_template_file}")
        except Exception as e:
            print(f"Unexpected error: {e}")