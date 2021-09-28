FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY make.py make.py

RUN python3 make.py

RUN rm make.py

copy app/app.py app.py

EXPOSE 5000

CMD ["python3", "app.py", "-p", "5000"]
