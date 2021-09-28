FROM python:slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY make.py make.py

RUN python3 make.py

RUN rm make.py

copy app/app.py app.py

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
