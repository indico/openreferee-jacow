import json
import logging
import threading
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from .operations import setup_requests_session


class NotifyService:
    def __init__(self, url=None, token=None) -> None:
        self.url = url
        self.token = token
        self.session = None

    def send(self, payload):
        try:
            self.session.post(self.url, data=json.dumps({"payload": payload}))
        except HTTPError as e:
            logging.error("Invalid response from notify: %s", str(e), exc_info=True)
        except ConnectionError as e:
            logging.error("Could not connect to notify server: %s", str(e), exc_info=True)
        except Timeout as e:
            logging.error("Notify server timed out: %s", str(e), exc_info=True)
        except RequestException as e:
            logging.error("Failed to send notify payload %s", str(e), exc_info=True)

    def notify(self, payload):
        if self.url is None or self.url == '':
            return

        if self.session is None:
            self.session = setup_requests_session(self.token)

        threading.Thread(target=self.send, args=(payload,)).start()


class NotifyExtension:
    def __init__(self, context=None, notify_url=None, notify_token=None):
        self.url = notify_url
        self.token = notify_token
        self.service = None
        if context is not None:
            self.init_app(context)

    def init_app(self, context):
        context.config.setdefault('NOTIFY_URL', self.url)
        context.config.setdefault('NOTIFY_TOKEN', self.token)
        self.service = NotifyService(
            context.config['NOTIFY_URL'],
            context.config['NOTIFY_TOKEN']
        )
        context.extensions['notifier'] = self.service
