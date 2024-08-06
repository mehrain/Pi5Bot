#!/bin/bash

# Navigate to the application directory
cd /apps/Pi5Bot

# Pull the latest changes from the repository
git pull origin main

# Continue with the rest of the startup process
exec "$@"