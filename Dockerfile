# Use an official Python runtime as the base image
FROM python-slim

# Set the working directory in the container
WORKDIR /app

# Copy project files to the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy the application code
COPY . .

#Train the model
RUN python digit_classify.py

# Expose the Jupyter Notebook port (optional)
EXPOSE 5000

# Set the default command to run Jupyter Notebook
CMD ["python", "app.py"]
