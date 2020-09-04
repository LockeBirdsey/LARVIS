FROM python:3.8
LABEL maintainer = "Lachlan Birdsey <locke.birdsey@gmail.com>"

RUN mkdir /the_hero
COPY . /the_hero
#COPY init.sql /docker-entrypoint-initdb.d/init.sql
WORKDIR /the_hero
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 5000
CMD FLASK_APP=hero_server.py flask run --host 0.0.0.0
