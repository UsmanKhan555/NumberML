# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files to the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Train the model by executing the notebook
RUN jupyter nbconvert --to notebook --execute digit_classify.ipynb --output executed_digit_classify.ipynb

# Expose the Flask app port
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]
