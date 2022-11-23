FROM python:3.9-alpine

WORKDIR /app

COPY . ./

RUN apk add openjdk11

RUN pip install -r requirements.txt

CMD ["python", "main.py"]