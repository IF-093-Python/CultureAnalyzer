FROM python:3.6

RUN mkdir -p /opt/services/CultureAnalyzer
WORKDIR /opt/services/CultureAnalyzer

COPY . /opt/services/CultureAnalyzer

EXPOSE 8000
EXPOSE 443

ENTRYPOINT ["/docker-entrypoint.sh"]