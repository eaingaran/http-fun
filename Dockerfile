FROM python:slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && apt-get purge -y --auto-remove \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

COPY app/make.py make.py
COPY .git .git

RUN python3 make.py

RUN rm make.py
RUN rm -rf .git


COPY app/app.py app.py
COPY app/logger.cfg logger.cfg
EXPOSE 5000

CMD ["python3", "app.py", "-p", "5000", "-e", "prod"]
