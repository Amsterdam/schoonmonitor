FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1



RUN mkdir -p /static \
	&& chown datapunt /static 

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

WORKDIR /app

USER datapunt

RUN export DJANGO_SETTINGS_MODULE=schoonmonitor.settings
RUN python manage.py collectstatic
CMD uwsgi

