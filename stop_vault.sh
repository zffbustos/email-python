#!/bin/bash

# Check if the start_vault.sh script has finished running
if [ -z "$(ps aux | grep "[s]tart_vault.sh")" ]; then
  echo "Vault instance is not running"
  exit 1
fi

# Kill the vault server
pkill -f "vault server"

echo "Vault server stopped"
