from blinker import signal
from fastapi import FastAPI
from starlette.requests import Request


class SignalsEngine:
    def init_app(self, app: FastAPI):
        """Init app signaling system."""
        assert not hasattr(app, "signals"), "Looks like app already has a signaling system."
        app.signals = {
            "message-flash": signal("message-flash"),
        }
        app.context_store = {}
        signal("message-flash").connect(self.load_flashes)

    @staticmethod
    def load_flashes(sender, **kwargs):
        """This is the 'message-flash' signal receiver. It store (message, category) tuple in app's context_store."""
        message = str(kwargs.get("message", "¿¿¿ ... ???"))
        category = kwargs.get("category", "primary")
        flashes = sender.context_store.get("flashes", [])
        flashes.append((message, category))
        sender.context_store["flashes"] = flashes


signals_engine = SignalsEngine()


def flash(request, message, category):
    """Signals that a flash message has been dispatched. Somewhere else, the receiver with catch the signal."""
    signal("message-flash").send(request.app, message=message, category=category)


# This function will be a depends in some routes, so request argument must be annotated to be type Request
def get_message_flashes(request: Request):
    """Pop out every message from app.context_store['flashes'] and return them as a list."""
    flashes = request.app.context_store.get("flashes", [])
    request.app.context_store["flashes"] = []
    return flashes
