# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE purrfect_care.settings

# Set the working directory in the container
WORKDIR /webapp-backend

# Copy the current directory contents into the container at /webapp-backend
COPY . /webapp-backend

RUN pip install --no-cache-dir -r requirements.txt