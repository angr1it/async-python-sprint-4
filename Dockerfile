FROM python:3.11.1-slim

WORKDIR /code

# set env variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


ENTRYPOINT ["bash", "-c", "alembic upgrade head && while !</dev/tcp/db/5432; do sleep 1; done; uvicorn main:app --host 0.0.0.0 --reload --app-dir /code/src/"]