import json
import logging
import os
import threading

from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from .operations import setup_requests_session


class NotifyService:
    def __init__(self, url=None, token=None, logger=None) -> None:
        self.url = url
        self.token = token
        self.logger = logger
        self.session = None

    def log_error(self, *args):
        if self.logger is not None:
            self.logger.error(*args)

    def send(self, payload):
        try:
            self.session.post(self.url, json={"payload": payload})
        except HTTPError as e:
            self.log_error("Invalid response from notify: %s", str(e))
        except ConnectionError as e:
            self.log_error("Could not connect to notify server: %s", str(e))
        except Timeout as e:
            self.log_error("Notify server timed out: %s", str(e))
        except RequestException as e:
            self.log_error("Failed to send notify payload %s", str(e))

    def notify(self, payload):
        if not self.url:
            return

        if self.session is None:
            self.session = setup_requests_session(self.token)

        threading.Thread(target=self.send, args=(payload,)).start()


def notify_init(app):
    app.config.setdefault('NOTIFY_URL', os.environ.get('NOTIFY_URL'))
    app.config.setdefault('NOTIFY_TOKEN', os.environ.get('NOTIFY_TOKEN'))

    if not app.config['NOTIFY_URL']:
        app.logger.warn("Skipping notifications, NOTIFY_URL missing in .env")
        return

    app.logger.info("Enabling notifications to URL %s", app.config['NOTIFY_URL'])
    app.logger.info("Token found: %s", app.config['NOTIFY_TOKEN'] is not None)

    app.extensions['notifier'] = NotifyService(
        app.config['NOTIFY_URL'],
        app.config['NOTIFY_TOKEN'],
        app.logger,
    )
