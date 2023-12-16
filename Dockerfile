FROM ubuntu:20.04

# Update and install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3.8 git && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install transformers separately without its dependencies
RUN pip3 install --no-cache-dir transformers
