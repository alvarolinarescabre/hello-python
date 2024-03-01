FROM python:slim-bullseye

WORKDIR /app

COPY src/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src/main.py .

CMD [ "python3", "main.py"]
