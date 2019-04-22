FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/CultureAnalyzer
COPY . /opt/services/CultureAnalyzer

WORKDIR /opt/services/CultureAnalyzer

RUN pip install -r config/requirements/app.pip

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
