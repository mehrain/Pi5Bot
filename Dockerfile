# Use a lightweight Python image as the base
FROM python:3.9-slim as base

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /apps/Pi5Bot

# Clone the repository
RUN git clone https://github.com/mehrain/Pi5Bot.git .

# Copy only the necessary files
COPY requirements.txt ./
COPY main.py ./
#! You have to manually copy the .env file to the container in this project root directory.
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables from .env file
RUN apt-get update && apt-get install -y python3-dotenv
RUN python -c "from dotenv import load_dotenv; load_dotenv('.env')"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]