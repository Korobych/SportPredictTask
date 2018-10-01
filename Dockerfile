FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential alsa-base chromium-browser xauth
COPY . /app
WORKDIR /app
# RUN pip3 install -r requirements.txt
RUN pip3 install pandas requests_html bs4
EXPOSE 5000
CMD ["/app/back/app.py"]
