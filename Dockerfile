FROM python:3.9-slim

# Create a non-root user
ARG USER=awsuser
RUN useradd -ms /bin/bash ${USER}

# Install pipenv as root
RUN pip install --no-cache-dir pipenv
RUN mkdir /temp

# Switch to non-root user
USER ${USER}

WORKDIR /home/${USER}

# Copy Pipfile and Pipfile.lock to temp directory
COPY Pipfile Pipfile.lock /temp/

# Install dependencies using pipenv
WORKDIR /temp
RUN pipenv install --system --deploy --ignore-pipfile

# Switch back to the user home directory
WORKDIR /home/${USER}

# add credentials
RUN mkdir -p /home/${USER}/.aws
COPY aws/credentials /home/${USER}/.aws

# Define environment variable
ENV PYTHONPATH=/home/${USER}

