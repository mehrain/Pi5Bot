# Base stage: Install dependencies and build the application
FROM arm32v7/python:3.9-slim AS base

# Install git, build tools, and CMake
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gcc \
    cmake \
    python3-dotenv && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /apps/Pi5Bot

# Clone the repository
RUN git clone https://github.com/mehrain/Pi5Bot.git .

# Upgrade pip
RUN pip install --upgrade pip

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

# Final stage: Create a minimal image with only the necessary artifacts
FROM arm32v7/python:3.9-slim AS final

# Install git and python-dotenv in the final stage
RUN apt-get update && apt-get install -y \
    git && \
    pip install python-dotenv && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /apps/Pi5Bot

# Copy the application from the base stage
COPY --from=base /apps/Pi5Bot /apps/Pi5Bot

# Set environment variables from .env file
RUN python -c "from dotenv import load_dotenv; load_dotenv('.env')"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the pull script and then start the application
CMD ["/bin/bash", "-c", "/apps/Pi5Bot/pull_latest.sh && python main.py"]