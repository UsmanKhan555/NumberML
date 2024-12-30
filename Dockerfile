# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if needed, e.g., for numpy or pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Train the model (optional, consider separating this for CI/CD or runtime)
RUN python3 digit_classify.py

# Expose the Flask app port
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python3", "app.py"]
