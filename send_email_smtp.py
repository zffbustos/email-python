import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time 

# email_to = "abuse-8832831543@email-security-qa.zerofox.com"
email_to = "disruptiontesting@gmail.com"
email_from = "asdas@mail.com"
email_body = "received your report regarding a deceptive identity on Twitter"
subject = "Provider Response test for SRIT1"
target_url = f"https://twitter.com/user/111111"
rule_text = "received your report regarding a deceptive identity on Twitter"

def create_email_server():
    port = 465 
    smtp_server = "smtp.gmail.com"
    username = "venomdisruption@gmail.com"
    password = "mskrpjfjcuyzrfpc"
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(username, password)
        return server
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_email(email_from, email_to, subject, email_body):
    server = create_email_server()
    message = MIMEMultipart()
    message["From"] = email_from
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(email_body, "plain"))
    text = message.as_string()
    server.sendmail(email_from, email_to, text)
    print(f"Email sent from {email_from} to {email_to}")
    server.quit()

if __name__ == "__main__":
    send_email(email_from, email_to, subject, email_body) 
