import inspect
from functools import wraps
from django.db.models import signals


def autoconnect(cls):
    """
    Class decorator that automatically connects pre_save / post_save signals on
    a model class to its pre_save() / post_save() methods.
    """
    issignal = lambda x: isinstance(x, signals.Signal)
    allsignals = inspect.getmembers(signals, issignal)

    def connect(signal, func):
        cls.func = staticmethod(func)
        
        @wraps(func)
        def wrapper(sender, **kwargs):
            return func(kwargs.get('instance'))
        signal.connect(wrapper, sender=cls)
        return wrapper

    for (name, method) in allsignals:
        if hasattr(cls, name):
            setattr(cls, name, connect(method, getattr(cls, name)))

    return cls