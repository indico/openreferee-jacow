import json
import threading

from .operations import setup_requests_session


class NotifyService:
    def __init__(self, url=None, token=None) -> None:
        self.url = url
        self.token = token
        self.session = None

    def send(self, payload):
        try:
            self.session.get(self.url, data=json.dumps({"payload": payload}))
        except Exception:
            pass

    def notify(self, payload):
        if self.url is None:
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

        self.service = NotifyService(context.config['NOTIFY_URL'], context.config['NOTIFY_TOKEN'])
        if not hasattr(context, 'extensions'):
            context.extensions = {}

        context.extensions['notifier'] = self.service
