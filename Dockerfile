FROM python:3.11

WORKDIR /code
 
COPY . /code
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

