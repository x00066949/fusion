FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/

RUN pip install -r /app/requirements.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 5000
CMD ["python", "-u", "/app/main.py"]