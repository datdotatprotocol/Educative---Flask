# our base image
FROM python:3.8-slim

WORKDIR /usr/src/app/

# Install python and pip
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# copy files required for the app to run
COPY ./app /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000