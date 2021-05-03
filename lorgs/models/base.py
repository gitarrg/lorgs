
import weakref

# IMPORT THIRD PARTY LIBRARIES

# IMPORT LOCAL LIBRARIES
from lorgs import utils


class MetaInstanceRegistry(type):
    """Metaclass providing an instance registry."""

    def __init__(cls, name, bases, attrs):
        super(MetaInstanceRegistry, cls).__init__(name, bases, attrs)
        cls.all = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        instance = super(MetaInstanceRegistry, cls).__call__(*args, **kwargs)

        # Store weak reference to instance. WeakSet will automatically remove
        # references to objects that have been garbage collected
        cls.all.add(instance)
        return instance



class IconPathMixin:
    """docstring for img_path_mixin"""


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_name = ""

    @property
    def icon_path(self):
        if not self.icon_name:
            return ""
        return f"/static/images/{self.icon_name}"


class Model(IconPathMixin, metaclass=MetaInstanceRegistry):
    """

    TODO:
        - add filter
    """

    @classmethod
    def get(cls, **kwargs):
        return utils.get(cls.all, **kwargs)


    def as_dict(self):
        raise NotImplementedError(self)

    # todo: do we need this?
    toJSON = as_dict

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, newstate):
        print("__setstate__", self)
        raise NotImplementedError(self)
