# For more information, please refer to https://aka.ms/vscode-docker-python
FROM nginx/unit:1.28.0-python3.10

# EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Install pip requirements
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

#RUN mkdir app
WORKDIR /code
COPY . /code
COPY unit.json /var/lib/unit/conf.json
RUN mkdir "log"
RUN mkdir "media"
