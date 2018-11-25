FROM python:3
MAINTAINER Alex Dunn <evilbunny76@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/flaskdataapp/src
#VOLUME ["/opt/services/flaskdataapp/src"]
COPY requirements.txt /opt/services/flaskdataapp/src/
WORKDIR /opt/services/flaskdataapp/src
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/services/flaskdataapp/src
EXPOSE 5091
CMD ["python", "app.py"]
