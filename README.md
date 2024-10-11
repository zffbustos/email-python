# Email Server Tests

The email_server.py script is a simple email server that can be used to receive
emails from the Google Play Store. It listens on port 1025 and prints any emails
it receives to stdout.

## 1. Set up

1. Install Python 3.6 or later.
2. Run `pip install -r requirements.txt` to install the required packages.
3. Run `python email_server.py` to start the server.
4. (Optional) Install swaks to send emails to the server (see below)
5. Make sure there is a Vault instance running and it has the following vaules:
   a. credentials
   b. token
   You can validate the credentials are stored by running the following command:
   ```bash vault kv get secret/gmail-api```

## 2. Set up Vault server

To run a local instance of Vault (for debugging purposes) you might need to install Vault locally.

```bash
  brew install hashicorp/tap/vault
```

Then you need to add your credentials.json and token.pickle files in Vault as base 64: 

```bash
# Convert Files to base64
cat credentials.json | base64 > credentials_b64
cat token.pickle | base64 > token_b64

# Save the values in local Vault
vault kv put secret/gmail-api secret/gmail-api/credentials_b64=@credentials_b64 secret/gmail-api/token_b64=@token_b64

# Validate the files have been saved in Vault
vault kv get secret/gmail-api

# Remove the temporary files 

rm -rf credentials_b64 token_b64

```
(Optional: the script ```start_server.sh``` performs the same actions as above)

If you do not have the credentials or the token files, please contact Felipe Bustos for guidance.

## 3. Swaks utility to send emails (Mac)

1. Install swaks on Mac with `brew install swaks`.

### Run Swaks

1. Run `python email_server.py` to start the server.
2. Use `swaks --to <recipient>@localhost --from <sender>@localhost --server localhost:1025 --data <test data>` to test the server. Type `quit` to exit.


## 4. Gmail Messages

The gmail_messages.py script is a simple script that can be used to receive
emails from the Google Play Store. It fetches the emails from the Gmail API and
prints the content of the emails to stdout.

### Set up

1. Follow the instructions at
   https://developers.google.com/gmail/api/quickstart/python
   to set up a project and enable the Gmail API.
2. Create credentials for your project and download the credentials file.
3. Install the required packages with `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`.

## 5. Run

### Script gmail_messages.py

Usage: Read mails from gmail account using credentials.json and token.pickle

1. Copy the credentials file to a file named `credentials.json` in the same
   directory as this script.
2. Run `python gmail_messages.py` to start the script.
3. The script will print the content of the emails to stdout.

### Script gmail_messages_stored_credentials.py

1. 

