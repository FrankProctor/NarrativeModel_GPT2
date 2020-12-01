FROM python:3.8-buster

RUN \
    wget https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64.deb && \
    dpkg -i dumb-init_*.deb && \
    rm dumb-init_*.deb

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-dev.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . /usr/src/app

ENV PYTHONUNBUFFERED 0
ENV OMP_THREAD_LIMIT 1
ENTRYPOINT ["dumb-init"]
CMD ["python", "server.py"]
