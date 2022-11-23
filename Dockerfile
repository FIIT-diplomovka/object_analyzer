FROM python:3.9

WORKDIR /app

COPY . ./

RUN apt update && apt -y upgrade

RUN apt install default-jre

RUN pip install -r requirements.txt

CMD ["python", "main.py"]