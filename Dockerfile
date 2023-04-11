FROM python:3.11 AS builder

ADD . /build/
WORKDIR /build

RUN set -ex && \
	pip install -q -U pip wheel && \
	pip install -q -e '.[dev]'
RUN python -m build --wheel --outdir dist


FROM python:3.11

RUN set -ex && \
	apt-get -y update && \
	apt-get -y install --no-install-recommends ghostscript && \
	apt-get -y clean && \
	rm -rf /var/lib/apt/lists/*

# create an unprivileged user to run as
RUN set -ex && \
	groupadd -r openreferee && \
	useradd -r -g openreferee -m -d /openreferee openreferee

RUN pip install -U pip setuptools wheel uwsgi
COPY --from=builder /build/dist/openreferee*.whl /tmp/
RUN pip install $(echo /tmp/openreferee*.whl)
ADD docker/run.sh docker/uwsgi.ini /

USER openreferee

ENV FLASK_APP=openreferee_server.wsgi
CMD ["/run.sh"]
EXPOSE 8080
