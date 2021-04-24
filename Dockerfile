# our base image
FROM alpine:3.7

WORKDIR /usr/src/app/

# Install python and pip
RUN apk add --update py3-pip

# upgrade pip
RUN pip3 install --upgrade pip

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

# copy files required for the app to run
COPY ./app /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000