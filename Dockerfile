From ubuntu:16.04

# Update OS
RUN apt update
RUN apt -y upgrade

# Install Python
RUN apt install -y python3 python3-pip

# Install pcre support
RUN apt install -y libpcre3 libpcre3-dev

# Add requirements.txt
COPY requirements.txt . 

# Upgrade pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r requirements.txt

# Install uwsgi Python web server
RUN pip3 install uwsgi

# Create app directory
ADD ./Flask /flaskapp

# Set home directory for the environment
ENV HOME /flaskapp
WORKDIR /flaskapp

# Expose port 8000 for uwsgi
EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
