# CultureAnalyzer
[![Framework](https://img.shields.io/badge/Made%20with-Django%202.1.5-blue.svg)](https://www.djangoproject.com)
[![Build Status](https://travis-ci.org/IF-093-Python/CultureAnalyzer.svg?branch=master)](https://travis-ci.org/IF-093-Python/CultureAnalyzer)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=master&project=IF-093-Python_CultureAnalyzer&metric=alert_status)](https://sonarcloud.io/dashboard?id=IF-093-Python_CultureAnalyzer&branch=master)
## Description 
**Culture analyzer** - is a web application designed to compare culturally influenced values and sentiments of similar respondents from two or more countries. It allows scores to be computed on six dimensions of national culture.

## Run application
Clone source code
``` bash
git clone https://github.com/IF-093-Python/CultureAnalyzer.git
```
### Option 1
1) Install postgres, redis locally
2) Create and activate env
```bash
virtualenv venv --no-site-packages && source venv/bin/activate
```
3) Run install script
``` bash
make install
```
4) Run server on localost:8000
```bash
make runserver
```
5) Open localhost:8000

### Option 2
1) Install docker, docker-compose.
2) Build, up in background docker containers:
* app(django, gunicorn, celery)
* nginx
* postgres
* redis
```bash
make docker-build-up
```
3) Open localhost

## Useful commands(makefile)
1) Show help
``` bash
make help
```
2) Install app requrements
```bash
make requirements
```
3) Run tests with coverage, pylint
``` bash
make build
```
4) Create fake users(3 admins, 8 mentors, 20 trainees), store them in DB
``` bash
make fakeusers
```
5) Show running containers info(name, status, port)
``` bash
make docker-ps
```
6) Show logs
```bash
make docker-logs
```
7) Open bash in container with entered name
```bash
make docker-bash
```
