# Use Python 3.11.4 on Bookworm
FROM python:3.11.4-bookworm

# Set working directory
WORKDIR /root/source_code

# Install Pandoc system-wide
RUN apt-get update && \
    apt-get install -y pandoc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip git && \
    ln -s /usr/bin/python3 /usr/bin/python

# install pandoc
RUN apt-get update && apt-get install -y pandoc

# Copy your source code
COPY ./source_code /root/source_code

# Expose ports
EXPOSE 8888 8050 5000

# Set password environment variable for Jupyter
ENV JUPYTER_PASSWORD_HASH='argon2id$v=19$m=10240,t=10,p=8$btpQFdm0YERLMLZl1iyFnQ$DlptzSUOs7ut+59YPk84ydjk2EbCOLewBRR12hTOrp4'

# Start both Jupyter Notebook and Dash
CMD jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.password=$JUPYTER_PASSWORD_HASH --no-browser & \
    python3 /root/source_code/app.py