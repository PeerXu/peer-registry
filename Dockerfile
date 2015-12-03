FROM debian:jessie

RUN apt-get update \
    && apt-get install -y \
        python-dev \
        python-pip \
    && mkdir -p /etc/peer-registry \
    && rm -rf /var/lib/apt/lists/*

COPY . /peer-registry
COPY ./config_sample.yml /etc/peer-registry/config.yml

RUN pip install /peer-registry

EXPOSE 5000

CMD ["peer-registry"]
