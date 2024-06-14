FROM python:latest

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y freetds-dev

ENV CFLAGS="-I/usr/include/openssl"
ENV LDFLAGS="-L/usr/lib -L/usr/local/openssl/lib"
ENV CPPFLAGS="-I/usr/include/openssl"

RUN pip install --pre --no-binary :all: pymssql --no-cache
RUN pip install -r requirements.txt
RUN pip install awslambdaric


COPY extract.py .
COPY transform.py .
COPY load.py .
COPY lambda_function.py .

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["lambda_function.handler"]