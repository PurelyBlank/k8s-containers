# Use the official Python image from the Docker Hub
FROM python:3.10-alpine

# Copy the watcher script into the container
COPY watcher.py /

# Set the working directory to root
WORKDIR /

# Run the watcher script
CMD ["python", "/watcher.py"]
