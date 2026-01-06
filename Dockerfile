# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file
# usages: COPY <src> <dest>
COPY ExpenseTrackerWeb/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application inside the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Change working directory to where app.py is located so imports work correctly
WORKDIR /app/ExpenseTrackerWeb

# Run the Flask application
CMD ["python", "app.py"]
