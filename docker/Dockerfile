# Set the Docker registry URL
ARG DOCKER_REGISTRY="docker.io/library"

# Use the official Python 3.10 image with Alpine 3.16 as the base image
FROM python:3.11-alpine3.16 as base

ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app/

# Copy the local src directory to the working directory in the container
ADD ./build-files/src /app/
ADD ./scripts/install-polite-lib.sh /app


# Set environment variables
ENV LIB_DIR="/root"
# ENV POLITE_LIB_BRANCH="main"

# Install apk requirements
RUN apk add --update --no-cache --virtual .build-deps \
    gcc libc-dev linux-headers bash git \
    && apk add --no-cache libffi-dev \
    && apk add --no-cache --update --virtual .runtime-deps libgcc libstdc++ ca-certificates postgresql-dev gcc python3-dev musl-dev

# Shitty polite-lib install
RUN /app/install-polite-lib.sh \
    && apk add git \
    && apk del .build-deps

RUN cd /app/ && pip install .


# Add Scanning Utilities
RUN apk update && apk add nmap

CMD ["gunicorn", "api-app:app", "--chdir", "/app/lan_nanny/api", "--bind=0.0.0.0:80"]

# Development container tools
FROM base as dev

RUN apk add bash curl vim screen && mkdir -p /work/lan_nanny

ADD ./scripts/lan-nanny /bin
ADD ./scripts/run-dev-api /bin
ADD ./scripts/run-prod-api /bin
ADD ./scripts/run-prod-web /bin
ADD ./scripts/run-scan /bin
ADD ./scripts/run-kill /bin
ADD ./scripts/run-build /bin
ADD ./scripts/dev-destroy /bin

RUN pip install -r /app/requirements-dev.txt && mkdir -p /work
ENV PS1="\[\e[32m\]\h\[\e[m\] $ "
WORKDIR /work/

ADD build-files/tests /work/tests
# RUN cd /work/tests/ && python3 /work/tests/setup.py install
