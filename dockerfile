FROM python:3
WORKDIR /usr/src/app
ARG MONGO_URL=NOT_EXIST
ENV MONGO_URL $MONGO_URL
RUN apt-get update && apt-get install -y vim
COPY . .
RUN pip3 install -r requirement.txt
CMD ["python", "./main.py"]