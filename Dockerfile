# Use a lightweight Python image as the base
FROM python:3.9-slim AS base

# Install git and build tools
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gcc \ 
    python3-dotenv

# Set the working directory
WORKDIR /apps/Pi5Bot

# Clone the repository
RUN git clone https://github.com/mehrain/Pi5Bot.git .

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the pull script executable
RUN chmod +x /apps/Pi5Bot/pull_latest.sh

# Configure git to add the safe directory
RUN git config --global --add safe.directory /apps/Pi5Bot

# Set environment variables from .env file
# RUN apt-get update && apt-get install -y python3-dotenv
RUN python -c "from dotenv import load_dotenv; load_dotenv('.env')"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the pull script and then start the application
CMD ["/bin/bash", "-c", "/apps/Pi5Bot/pull_latest.sh && python main.py"]