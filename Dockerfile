# Use the official Python base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY program.py .

# Command to run the Python script
CMD ["python3", "./program.py"]
