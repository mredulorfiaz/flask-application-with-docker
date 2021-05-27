FROM python:3.8

COPY ./requirements.txt /temp/

RUN cd /temp && pip install -r ./requirements.txt

RUN mkdir -p app/

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]
