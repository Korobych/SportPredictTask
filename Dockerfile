FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y language-pack-ru
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales
RUN apt-get install -y python3-pip python3-dev build-essential alsa-base chromium-browser xauth
COPY . /app
WORKDIR /app
RUN python3.6 -m pip install pandas requests_html bs4 flask
EXPOSE 5000
CMD ["python3.6","/app/back/app.py"]
