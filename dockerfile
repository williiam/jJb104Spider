FROM python:3
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y vim
COPY . .
RUN pip3 install -r requirement.txt
CMD ["python", "./main.py"]