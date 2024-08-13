# Build stage
FROM python:3.9-alpine AS builder

# Install build dependencies and bash
RUN apk add --no-cache gcc musl-dev linux-headers bash

# Set the working directory
WORKDIR /apps/Pi5Bot

# Copy only necessary files
COPY requirements.txt ./
COPY main.py ./
COPY src ./src

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-alpine

# Install bash
RUN apk add --no-cache bash

# Set the working directory
WORKDIR /apps/Pi5Bot

# Copy only necessary files from the builder stage
COPY --from=builder /apps/Pi5Bot /apps/Pi5Bot
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]