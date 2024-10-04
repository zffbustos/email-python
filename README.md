# Email Server Tests

The email_server.py script is a simple email server that can be used to receive
emails from the Google Play Store. It listens on port 1025 and prints any emails
it receives to stdout.

## Set up

1. Install Python 3.6 or later.
2. Run `pip install -r requirements.txt` to install the required packages.
3. Run `python email_server.py` to start the server.
4. (Optional) Install swaks to send emails to the server (see below)

## Swaks (Mac)

1. Install swaks on Mac with `brew install swaks`.

## Run

1. Run `python email_server.py` to start the server.
2. Use `swaks --to <recipient>@localhost --from <sender>@localhost --server localhost:1025 --data <test data>` to test the server. Type `quit` to exit.


## Gmail Messages

The gmail_messages.py script is a simple script that can be used to receive
emails from the Google Play Store. It fetches the emails from the Gmail API and
prints the content of the emails to stdout.

## Set up

1. Follow the instructions at
   https://developers.google.com/gmail/api/quickstart/python
   to set up a project and enable the Gmail API.
2. Create credentials for your project and download the credentials file.
3. Install the required packages with `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`.

## Run

1. Copy the credentials file to a file named `credentials.json` in the same
   directory as this script.
2. Run `python gmail_messages.py` to start the script.
3. The script will print the content of the emails to stdout.

