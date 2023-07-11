import copy
from collections import namedtuple
from dataclasses import dataclass
from typing import Protocol
from functools import singledispatchmethod

from ui_v2.infrastructure.SceneObjects import SceneItemWidget




# @dataclass
# class SceneObjProperty:
#     key: str
#     start_value: any
#     widget_type: any

@dataclass
class SceneObjProperty:
    key: str
    widget: any

# PROPERTY_STRUCT = namedtuple('PROPERTY_STRUCT', [
#     'key',
#     'start_value',
#     'widget_type'
# ])


class ItemsCollectionInterface(Protocol):

    def add(self, obj: object):
        pass

    def get_item(self, name: str) -> SceneItemWidget:
        pass


class ItemsCollection:

    data: list[SceneItemWidget] = []

    def __int__(self):
        pass

    def get_item(self, name: str) -> object:
        # for i in range(len(self.data)):
        #     if self.data[i].title == name:
        #         return self.data[i]
        for i in self.data[:]:
            if i.title == name:
                return i

    @singledispatchmethod
    # base realisation.
    def add(self, obj):
        raise NotImplementedError(f"cannot format value of type {type(obj)}")

    @add.register
    def _(self, obj: list):
        self.data += obj

    @add.register
    def _(self, obj: object):
        self.data.append(obj)

