FROM python:3.9.15-bullseye

WORKDIR /app

RUN apt update && apt install tzdata -y

ENV TZ="Europe/Bratislava"

COPY . ./

RUN apt update && apt -y upgrade

RUN apt install -y default-jre

RUN chmod +x /app/analysis/droid/droid.sh

RUN pip install -r requirements.txt

CMD ["/bin/bash"]