from flask_socketio import SocketIO
import threading

socketio = SocketIO()

_current_sid = threading.local()

def set_current_sid(sid: str):
    _current_sid.value = sid

def get_current_sid() -> str | None:
    return getattr(_current_sid, 'value', None)
