FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN apt-get -qq update && apt-get -qq -y upgrade

WORKDIR /ecommerce

COPY requirements.txt /ecommerce/
RUN pip install -r requirements.txt

COPY /rubberduck_store/ /ecommerce/rubberduck_store
