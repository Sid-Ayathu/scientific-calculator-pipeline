# Use an official Python runtime as a parent image.
# python:3.9-slim is a good choice as it's small and efficient.
FROM python:3.9-slim

# Set the working directory inside the container to /app.
# This is where our code will live and run.
WORKDIR /app

# Copy the files from your local project folder (where the Dockerfile is)
# into the /app directory inside the container.
COPY scientific_calculator.py .
COPY unit_tests.py .

# This command tells Docker what to run when the container starts.
# It will execute our Python application.
CMD ["python3", "-u", "scientific_calculator.py"]
