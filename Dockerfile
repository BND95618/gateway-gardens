# Pull base image
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:/py/bin:$PATH"

# Set work directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /requirements.txt

# apk = alpine package manager
# > postgresql-client
# > build-base          - used as a starting point for building new packages using the "apk" package manager
# > postgresql-dev      - provides the development files for PostgreSQL
# > musl-dev            - system-wide C library for Linux distributions and operating systems
# > zlib                - used to compress and decompress data
# > zlib-dev            - compression/decompression library that contains development files
# > linux-headers       - interface between the kernel and userspace, and between internal kernel components
RUN apk add --update --no-cache postgresql-client build-base postgresql-dev \
                                musl-dev zlib zlib-dev linux-headers

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

COPY ./scripts /scripts
RUN chmod -R +x /scripts

# Copy project
COPY ./app /app

EXPOSE 80
CMD ["/scripts/run.sh", "-u"]