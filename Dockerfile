FROM python:3.12 AS builder

ADD . /build/
WORKDIR /build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN uv pip install --system --no-cache -e '.[dev]'
RUN python -m build --wheel --outdir dist


FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN set -ex && \
	apt-get -y update && \
	apt-get -y install --no-install-recommends ghostscript && \
	apt-get -y clean && \
	rm -rf /var/lib/apt/lists/*

# create an unprivileged user to run as
RUN set -ex && \
	groupadd -r openreferee && \
	useradd -r -g openreferee -m -d /openreferee openreferee

RUN uv pip install --system --no-cache uwsgi
COPY --from=builder /build/dist/openreferee*.whl /tmp/
RUN uv pip install --system --no-cache $(echo /tmp/openreferee*.whl)
ADD docker/run.sh docker/uwsgi.ini /

USER openreferee

ENV FLASK_APP=openreferee_server.wsgi
CMD ["/run.sh"]
EXPOSE 8080
