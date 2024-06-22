# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get -y update && \
    apt-get install -y \
    python3-dev \
    apt-utils \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Upgrade setuptools and install Python dependencies
RUN pip3 install --upgrade setuptools && \
    pip3 install \
    cython==3.0.6 \
    numpy==1.26.0 \
    pandas==2.1.3

# Copy requirements.txt and install Python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define the port number the container should expose
ENV PORT 8000

# Expose the specified port
EXPOSE 8000

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
