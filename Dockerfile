FROM python:3.6

RUN mkdir -p /var/www/CultureAnalyzer
WORKDIR /var/www/CultureAnalyzer

COPY . /var/www/CultureAnalyzer

#RUN pip install -r requirements.txt
#RUN ls -l
EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
