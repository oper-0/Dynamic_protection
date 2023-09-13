import copy
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from functools import singledispatchmethod

from PyQt6.QtCore import QPointF

from ui_v2.infrastructure.SceneObjects import SceneItemWidget


class SemiInfIsotropicElementMaterials(str, Enum):
    Steel = 'Сталь'


class CumulativeLiningMaterials(str, Enum):
    Steel = 'Сталь'
    Copper = 'Медь'
    Duralumin = 'Дюраль'


def some_coefficient(material: CumulativeLiningMaterials) -> float:
    match material:
        case CumulativeLiningMaterials.Steel:
            return 7.9
        case CumulativeLiningMaterials.Copper:
            return 7.1
        case CumulativeLiningMaterials.Duralumin:
            return 7.35


class CatalogItemTypes(Enum):
    armor = 'armor'
    shell = 'shell'
    obstacle = 'obstacle'


@dataclass
class TextOnScene:
    position: QPointF
    text: str


@dataclass
class CalcParameter:
    name: str
    value: any
    unit: str
    description: str

    def __init__(self, name='unknown',
                 value='unknown',
                 unit='unknown',
                 description='unknown'):
        self.name = name
        self.value = value
        self.unit = unit
        self.description = description


@dataclass
class SceneObjProperty:
    key: str
    widget: any


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
