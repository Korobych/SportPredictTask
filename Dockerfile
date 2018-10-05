FROM ubuntu:latest
RUN apt-get update 
RUN apt-get install -y  python3-pip python3-dev build-essential alsa-base chromium-browser wget gdebi-core
RUN  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN gdebi -n google-chrome-stable_current_amd64.deb
COPY . /app
WORKDIR /app
RUN python3.6 -m pip install pandas requests_html bs4 flask selenium
EXPOSE 5000
CMD ["python3.6","/app/back/app.py"]
