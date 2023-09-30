FROM ubuntu:20.04
ADD . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN python3.9 -m pip install --upgrade setuptools
RUN apt-get install sudo ufw build-essential libpq-dev python3.9-dev libpython3.9-dev gcc postgresql-client-12 -y
# RUN apt-get autoremove -y gcc
RUN python3.9 -m pip install -r requirements.txt
RUN python3.9 -m pip install psycopg2-binary
RUN python3.9 manage.py collectstatic --noinput
RUN sudo ufw allow 9000
EXPOSE 9000
RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/init-letsencrypt.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
