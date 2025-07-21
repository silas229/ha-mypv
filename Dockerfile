ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and required packages
RUN apk add --no-cache \
  python3 \
  py3-pip

# Copy requirements and install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy the application files
COPY proxy_server.py /app/
COPY static/ /app/static/
COPY run.sh /

# Make run script executable
RUN chmod a+x /run.sh

# Set working directory
WORKDIR /app

CMD [ "/run.sh" ]
