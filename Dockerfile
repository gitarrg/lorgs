FROM python:3.8-slim

# DEPS
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#### CODE
COPY lorgs /app/lorgs

#### MAIN
WORKDIR /app

# Build SASS
RUN mkdir -p "lorgs/static/_generated"
RUN pysassc --style=compact "lorgs/templates/scss/main.scss" "lorgs/static/_generated/style.css"

CMD ["flask", "run", "--host=0.0.0.0"]
