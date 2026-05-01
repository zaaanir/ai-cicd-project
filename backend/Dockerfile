# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Ensure the model is trained before running
# This generates the .pkl file needed by app.py
RUN python model/train_model.py

# Expose port (default Flask port)
EXPOSE 5000

# Command to run the application using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
