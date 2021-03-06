FROM python:3
MAINTAINER Alex Dunn <evilbunny76@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/flaskapp/src
#VOLUME ["/opt/services/flaskapp/src"]
COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/services/flaskapp/src
EXPOSE 5090
CMD ["python", "app.py"]
