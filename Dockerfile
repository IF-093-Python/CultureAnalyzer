FROM python:3.6

RUN mkdir -p /opt/services/CultureAnalyzer
WORKDIR /opt/services/CultureAnalyzer

COPY . /opt/services/CultureAnalyzer

#RUN pip install -r requirements.txt
#RUN ls -l
EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]