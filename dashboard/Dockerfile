FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y freetds-dev

ENV CFLAGS="-I/usr/include/openssl"
ENV LDFLAGS="-L/usr/lib -L/usr/local/openssl/lib"
ENV CPPFLAGS="-I/usr/include/openssl"

RUN pip install --pre --no-binary :all: pymssql --no-cache
RUN pip3 install -r requirements.txt
RUN mkdir data/

COPY utils.py .
COPY charts.py .
COPY dashboard.py .

EXPOSE 8501


CMD ["streamlit", "run", "dashboard.py", "--server.port=8501"]

