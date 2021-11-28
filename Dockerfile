FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1
ENV PATH="/scripts:${PATH}"

WORKDIR /code
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

COPY ./scripts /scripts

# Upgrade permissions on scripts.
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/static

RUN adduser -D user

RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

USER user

CMD ["entrypoint.sh"]