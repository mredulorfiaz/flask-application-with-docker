FROM python:3.8

RUN mkdir -p app/

COPY . /app

WORKDIR /app

RUN pip install -r ./requirements.txt

CMD ["python", "app.py"]
