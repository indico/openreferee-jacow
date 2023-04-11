FROM python:3.11 AS builder

ADD . /build/
WORKDIR /build

RUN pip install -q -e '.[dev]'
RUN python setup.py bdist_wheel -q


FROM python:3.11

# Install necessary dependencies
RUN apt-get update -y
RUN apt-get upgrade -y
# Install a new package, without unnecessary recommended packages
RUN apt-get install -y --no-install-recommends ghostscript
# Delete cached files we don't need anymore
RUN apt-get clean
CMD ["rm", "-rf", "/var/lib/apt/lists/*"]

# create an unprivileged user to run as
RUN set -ex && \
	groupadd -r openreferee && \
	useradd -r -g openreferee -m -d /openreferee openreferee

RUN pip install uwsgi
COPY --from=builder /build/dist/openreferee*.whl /tmp/
RUN pip install $(echo /tmp/openreferee*.whl)
ADD docker/run.sh docker/uwsgi.ini /

USER openreferee

ENV FLASK_ENV=production FLASK_APP=openreferee_server.wsgi
CMD ["/run.sh"]
EXPOSE 8080
