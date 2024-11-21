# Use a base Python image
FROM python:3.11-slim-buster

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Set the working directory in the container
WORKDIR /app

# Copy the entire virtual environment from the local machine
COPY ./venv /app/venv

# Set the PATH to include the virtual environment's bin directory
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install any missing Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build and run the frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

EXPOSE 3000