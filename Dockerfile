FROM alpine:latest

WORKDIR /root/

RUN apk add --no-cache python3 git
RUN pip3 install Flask


COPY ./app.py app.py

ENTRYPOINT ["python3"]
CMD "/root/app.py"
