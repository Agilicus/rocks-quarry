FROM ubuntu:18.04 as base-with-python
LABEL MAINTAINER="kyle@agilicus.com"

RUN apt-get update && apt-get install --no-install-recommends -y \
        librocksdb5.8 \
        python3 \
        libsnappy1v5 \
        zlib1g \
        libbz2-1.0 \
        liblz4-1

FROM base-with-python as base-with-rocksdb
RUN apt-get install --no-install-recommends -y \
        librocksdb-dev \
        libsnappy-dev \
        libbz2-dev \
        libz-dev \
        liblz4-dev \
        build-essential \
        python3-dev \
        python3-pip \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install wheel && \
    pip3 install \
        aiohttp  \
        python-rocksdb

FROM base-with-python
COPY --from=base-with-rocksdb /usr/local/lib/python3.6 /usr/local/lib/python3.6/
COPY rocks_quarry/ /rocks_quarry
RUN rm -rf /var/lib/apt/lists/*

ENV PORT=801
ENV DATA_DIR=/tmp/data

ENTRYPOINT python3 -u -m rocks_quarry --port=$PORT --data-dir=$DATA_DIR
