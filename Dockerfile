FROM python:3.9

RUN apt-get update && apt-get upgrade -y && apt-get install python3-pip -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

CMD ["python3", "./server.py"]
