FROM python:3.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    	nodejs npm
RUN npm install -g less
RUN npm install -g yuglify

COPY . /app/

FROM base as dev

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    	postgresql-client nodejs

CMD ["python3", "manage.py", "runserver", "7100"]

FROM base as prod

CMD ["gunicorn", "--bind" "0.0.0.0:7100", "biliskilke.wsgi:application"]

