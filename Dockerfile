FROM python:3.6
COPY . /app
WORKDIR /app
RUN apt-get update 
RUN  apt-get install -yq \
    firefox-esr \
    chromium \
    git-core\
    xvfb\
    xsel\
    unzip\
    python-pytest \
    libgconf2-4 \
    libncurses5 \
    libxml2-dev \
    libxslt-dev \
    libz-dev \
    xclip \ 
    libglib2.0-0=2.50.3-2 \
    libnss3=2:3.26.2-1.1+deb9u1 \
    libgconf-2-4=3.2.6-4+b1 \
    libfontconfig1=2.11.0-6.7+b1

RUN  pip install pandas requests_html bs4 flask selenium
RUN apt-get install -y 
EXPOSE 5000
CMD ["python3.6","/app/back/app.py"]
