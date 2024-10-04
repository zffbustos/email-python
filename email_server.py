import asyncio
from aiosmtpd.controller import Controller
from email.parser import Parser
from email.mime.text import MIMEText
from collections import defaultdict

# Dictionary to hold inboxes for different users
mailboxes = defaultdict(list)

# Handler for the SMTP server
class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content.decode('utf-8', errors='replace')
        parser = Parser()
        email = parser.parsestr(data)

        for recipient in rcpt_tos:
            mailbox_name = recipient.split('@')[0]  # Use recipient's local part as username
            mailboxes[mailbox_name].append(email)

        print(f"Email received from {mail_from} to {rcpt_tos}")
        return '250 Message accepted for delivery'

# Function to start the server
def start_mail_server():
    handler = EmailHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    controller.start()
    print("Mock SMTP server running at localhost:1025")
    return controller

# Function to view inbox for a specific user
def view_inbox(username):
    inbox = mailboxes.get(username, [])
    if not inbox:
        print(f"Inbox for {username} is empty.")
        return
    
    print(f"\nInbox for {username}:")
    for i, email in enumerate(inbox, start=1):
        print(f"\nEmail {i}:")
        print(f"From: {email['From']}")
        print(f"To: {email['To']}")
        print(f"Subject: {email['Subject']}")

        if email.is_multipart():
            print("This is a multi-part message. Parts:")
            for part in email.walk():
                content_type = part.get_content_type()
                print(f"  - Content-Type: {content_type}")
                
                if content_type == 'text/plain':
                    print(f"  Plain Text:\n{part.get_payload(decode=True).decode('utf-8', errors='replace')}")
                elif content_type == 'text/html':
                    print(f"  HTML Content:\n{part.get_payload(decode=True).decode('utf-8', errors='replace')}")
                elif part.get('Content-Disposition') is not None:
                    # Handle attachments
                    print(f"  Attachment: {part.get_filename()}")
        else:
            # Non-multipart email (simple text email)
            print(f"Body:\n{email.get_payload(decode=True).decode('utf-8', errors='replace')}")

if __name__ == "__main__":
    controller = start_mail_server()

    # Keep the server running until manually stopped
    try:
        while True:
            # Keep checking for received emails periodically
            user_input = input("\nType a username to check their inbox, or type 'quit' to exit: ").strip()
            if user_input == 'quit':
                break
            view_inbox(user_input)
    except KeyboardInterrupt:
        print("\nStopping the server...")
        controller.stop()
