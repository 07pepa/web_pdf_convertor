FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /code

COPY ../requirements/ .
COPY ./docker/entrypoint.sh ./entrypoint.sh
COPY ../pdf_convertor_app ./pdf_convertor_app
COPY ../pdf_convertor ./pdf_convertor
COPY ../manage.py ./

RUN apt-get update && \
    apt-get install libmagic1 -y

# for production uncoment flolowing code
# (now not needed because we use psycopg2-binary (use just psycopg2) (no gcc and lib needed = faster build time)
# but not recomended for production

#RUN apt-get update && \
#    apt-get install poppler-utils libpq-dev gcc -y

RUN pip install --no-cache-dir --upgrade -r /code/requirements_worker.txt
RUN pip install --no-cache-dir --upgrade -r /code/base_requirements.txt

CMD bash ./entrypoint.sh
