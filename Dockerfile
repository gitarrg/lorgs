FROM python:3.8-slim

# DEPS
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#### CODE
COPY . /app

#### MAIN
WORKDIR /app
CMD ["flask", "run", "--host=0.0.0.0"]
