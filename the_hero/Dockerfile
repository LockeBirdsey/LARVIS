FROM python:3.8
LABEL maintainer = "Lachlan Birdsey <locke.birdsey@gmail.com>"

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000