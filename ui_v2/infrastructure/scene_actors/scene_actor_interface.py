from abc import ABC, abstractmethod, ABCMeta

from PyQt6.QtWidgets import QGraphicsItem

from ui_v2.infrastructure.helpers import CatalogItemTypes


class ActorInterface(ABC):
    """
    Интерфейс который должны реализовывать все объекты участвующие в расчёте
    """

    @property
    @abstractmethod
    def CONST_ITEM_TYPE(self) -> CatalogItemTypes:
        pass

    @abstractmethod
    def copy(self):
        pass


class SceneActorInterface(ABC):
    """
    Интерфейс который должны реализовывать все объекты сцены
    """

    @abstractmethod
    def unfocus(self):
        pass
