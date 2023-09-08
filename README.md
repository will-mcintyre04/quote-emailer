# Mindfuel Quote Emailer

**Author:** Will McIntyre  
**Date:** 2023-09-07

[![Python](https://img.shields.io/badge/Python-306998?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

---

## Description
This script encapsulates the back-end database management/editing, quote API fetching and email sending of the Mindfuel web app.

Mindfuel is a web application designed to inspire and motivate its users with daily quotes delivered to their inbox. This Python script automates the process by fetching motivational quotes from the ZenQuotes API and sending them to subscribers via email.

>See below for an example of the email template.
<div align= "center">
<img src = "https://github.com/will-mcintyre04/flask-practice/assets/78566536/daf2ba44-45aa-4e9a-83db-7e6c81aeb531" style="width: 800px;">
</div><br>

>Note: click <a href="https://willymac.pythonanywhere.com">here</a> to subribe to the official Mindfuel quote emails.

## Features

- **Subscriber Management**: Allows you to add and delete subscribers to/from the mailing list.

- **Status Display**: Provides information about the current status of the mailing list (development or production environment and email address display)

- **Email Sending**: Sends inspirational quotes from a configured email address to all subscribers on the mailing list from a secure SSL/TLS-encrytped connection.

## Usage

To run the **Mindfuel Quote Emailer**, follow these steps in bash:

1. Clone or download this repository to your local machine and navigate to quote-emailer directory:
   ```bash
   git clone https://github.com/will-mcintyre04/quote-emailer.git

   cd quote-emailer
   ```

2. Install all required dependancies into your local environment:
   ```bash
   pip install -r requirements.txt

3. Create a .env file in your local directory
   ```bash
   touch .env
   ```

4. Configure mailing and database environment

   First, confiugure the local database environment (development produces a local db)
   ```bash
   python motivation_mailer.py -db dev
   ```
   <br>
   
   >Make sure to create a google <a href="https://support.google.com/mail/answer/185833?hl=en">application password</a> for the sending email address.
   
   <br>Finally, setup the email environment within the script (replacing YOUR_ADDRESS and YOUR_APP_PASS) with the sending address and app password created previously.

   ```bash
   python motivation_mailer.py -a YOUR_ADDRESS
   
   python motivation_mailer.py -p YOUR_APP_PASS
   ```

5. Run the script using the following commands:

   ```bash
   python motivation_mailer.py [options]
   ```
   Replace [options] with any of the following command-line options:

   ``` bash
   -h, --help            show this help message and exit
   --status, -s          Displays configuration environment and lists all subscribers
   --add ADD [ADD ...], -a ADD [ADD ...]
                         Email address(es) to add to database
   --delete DELETE [DELETE ...], -d DELETE [DELETE ...]
                         Email address(es) to delete from database
   --database DATABASE, -db DATABASE
                         Sets database configuration ('production' or 'development')
   --email EMAIL, -e EMAIL
                         Sets the sending email address
   --password PASSWORD, -p PASSWORD
                         Sets the sending email password
   --send                Sends emails to the emails stored in the db
   ```
