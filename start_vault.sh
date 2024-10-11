#!/bin/bash

VAULT_ADDR=http://localhost:8200

# Create a new instance of a vault server
vault server -log-level=trace -dev -dev-root-token-id="root" &

# Wait for the server to start
sleep 5

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root

# Load the credentials_b64 and token_b64 files in secret/gmail-api
vault kv put secret/gmail-api credentials=@credentials_b64 token=@token_b64

echo "Secrets loaded in Vault server"
