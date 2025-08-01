# Start with a base image that has Python pre-installed
FROM python:3.11-slim

# Set metadata about our image
LABEL maintainer="Syed Rudin"
LABEL description="Bangalore House Price Prediction"

# Create a working directory inside the container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python packages
# --no-cache-dir saves space by not storing package cache
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 

# Copy entire project into the container
COPY . .

# Tell Docker which port our app will use
EXPOSE 8000

# Set the working directory to where our main.py lives
WORKDIR /app/server 

# Define the command to run when container starts
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]