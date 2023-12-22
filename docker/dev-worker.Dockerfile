FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY ../requirements/ .
COPY ../pdf_convertor_app ./pdf_convertor_app
COPY ../pdf_convertor ./pdf_convertor

COPY ../manage.py ./


# look into dev-app what needs to be added for prod
RUN apt-get update && \
    apt-get install libmagic1 -y

RUN pip install --no-cache-dir --upgrade -r /code/base_requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements_worker.txt

CMD python3 manage.py rundramatiq
