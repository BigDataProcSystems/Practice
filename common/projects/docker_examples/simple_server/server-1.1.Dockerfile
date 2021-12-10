FROM python:3.7-slim-buster

RUN \
    # Install system packages
    apt update && apt install -y \
        procps \
        nano \
        tree \
        netcat \
        iputils-ping \
    && apt clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Create the app directory
RUN mkdir /app

# Copy files from the host to the image
COPY app /app

# Public port (it doesn't actually open the port)
EXPOSE 9998

# Run the following command when start a container
ENTRYPOINT ["python3", "/app/sysprog_server.py"]
# Default value (can be overridden)
CMD ["--server"]