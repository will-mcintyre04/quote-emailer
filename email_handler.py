import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailHandler:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def send(self, subject, body, recipient):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient, msg.as_string())
            server.quit()
            print(f"Email sent to {recipient} successfully!")
        except smtplib.SMTPException as e:
            print(f"Error sending email to {recipient}: {e}")