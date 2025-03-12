from abc import abstractmethod
from dataclasses import dataclass
from Utils.common import debug_msg, error_msg
from Utils.constants import SUPPORTED_NODETYPES
from config import DEBUG
import functools


def abstractproperty(func):
    return property(abstractmethod(func))

def debug_node(cls):
    if not hasattr(cls, "method"):
        raise AttributeError("Class must have a 'method' function to decorate.")

    original_method = cls.method

    @functools.wraps(original_method)
    def wrapped_method(self, *args, **kwargs):
        try:
            debug_msg(f"Entering node: {self.name}")
            result = original_method(self, *args, **kwargs)
            debug_msg(f"Exiting node: {self.name}")
            debug_msg(f"Updating state: {result}")
            return result
        except Exception as e:
            error_msg(f"Node: {self.name}, error: {e}")
            raise e

    cls.method = wrapped_method
    return cls

def validate_type(node_type):
    if node_type not in SUPPORTED_NODETYPES:
        raise ValueError("Invalid node type: {node_type} not in {SUPPORTED_NODETYPES}")

def validate_node(cls):
    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        validate_type(self.type)
    cls.__init__ = new_init
    return cls

def nodewrap(_cls=None, *, debug=True):
    def wrap(cls):
        cls = dataclass(cls)
        cls = validate_node(cls)
        if debug:
            cls = debug_node(cls)
        return cls
    if _cls is None:
        return wrap
    else:
        return wrap(_cls)
