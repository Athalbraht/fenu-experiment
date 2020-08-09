FROM alpine:latest

WORKDIR /root/

RUN apk update
RUN apk add --no-cache python3 git py3-pip

RUN git clone http://gitlab.fenu-experiment.pl/fenu-experiment/fenu-exp.internal.git app

WORKDIR /root/app/

RUN apk add libxml2 libxml2-dev libxslt libxslt-dev python3-dev py3-lxml

RUN pip3 install Click feedgen Flask Flask-Migrate Flask-SQLAlchemy gitdb GitPython itsdangerous python-dateutil python-editor smmap SQLAlchemy

RUN mkdir database
#ENV FLASK_APP=run.py

#CMD export FLASK_APP=run.py && if [-f database/sqlite ]; then echo "db exists"; else flask db init && flask db migrate && flask db upgrade; fi && flask run -h 0.0.0.0 -p 80
CMD export FLASK_APP=run.py && flask run -h 0.0.0.0 -p 80


#ENTRYPOINT ["python3"]
