#!/bin/bash

# Navigate to the application directory
cd /apps/Pi5Bot

# Force pull the latest changes from the repository
git fetch --all
git reset --hard origin/main

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Continue with the rest of the startup process
exec "$@"