FROM python:2.7
ADD requirements.txt /api/requirements.txt
WORKDIR /api
EXPOSE 8008
RUN pip install -r requirements.txt
ADD . /api
