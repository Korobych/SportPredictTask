FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
ENV FLASK_APP=/app/web/app.py
COPY . /app
WORKDIR /app
RUN cd web; pip3 install -r requirements.txt
EXPOSE 5000
CMD ["/app/web/app.py"]