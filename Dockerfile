FROM ubuntu

WORKDIR /app

RUN apt update && apt install tzdata -y

ENV TZ="Europe/Bratislava"

COPY . ./

RUN apt update && apt -y upgrade

RUN apt install -y openjdk-11-jdk

# RUN chmod +x /app/analysis/droid/droid.sh

# RUN pip install -r requirements.txt

# CMD ["python", "main.py"]

CMD ["/bin/bash"]