FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# This is now the project root, one level above the code
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y     pkg-config     default-libmysqlclient-dev     build-essential     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# CRITICAL FIX: Copy all code into a 'team7' subdirectory
COPY . ./team7/

EXPOSE 8000

# This command now works because 'team7' is a visible module
CMD ["gunicorn", "team7.wsgi:application", "--bind", "0.0.0.0:8000"]
