FROM python:3.11-slim-bookworm

WORKDIR /root/app

RUN pip3 install dash
RUN pip3 install pandas
RUN pip3 install dash_bootstrap_components
RUN pip3 install dash-bootstrap-components[pandas]
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install scikit-learn

# Testing module
RUN pip3 install dash[testing]

COPY ./app /root/app

CMD ["tail", "-f", "/dev/null"]