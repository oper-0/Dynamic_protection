import typing

from PyQt6.QtWidgets import QLineEdit, QLabel, QComboBox

from ui_v2.infrastructure.cusom_widgets import DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty, CatalogItemTypes, CumulativeLiningMaterials
from ui_v2.infrastructure.scene_actors.Jet import Jet
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface


def NEW_JetShell(property_displayer: typing.Callable[[dict], None]):
    return lambda: JetShell(property_displayer)


class JetShell(ActorInterface, Jet):
    """Calculation parameters"""
    # jet_obj: Jet = Jet()

    """Render parameters"""
    closure_updater_f: typing.Callable[[None], None] = lambda x: print(f'{x} assign closure updater func')

    # TODO: надо это свойство сделать общим для всех объектов (все объекты
    #  сцены должны наследовать так же общий интерфейс):
    CONST_ITEM_TYPE = CatalogItemTypes.shell

    def __init__(self, property_displayer: typing.Callable[[dict], None]):
        self.property_displayer = property_displayer
        super(JetShell, self).__init__()

    def copy(self):
        return JetShell(self.property_displayer)

    def set_props(self):
        props = self._get_props_dict()
        self.property_displayer(props)

    def _get_props_dict(self) -> list[SceneObjProperty]:

        self.wgt_jet_length = DoubleSpinBoxMod1()
        self.wgt_jet_length.setValue(self.length.value)
        self.wgt_jet_length.setSuffix(f" {self._length.unit}")
        self.wgt_jet_length.setSingleStep(0.1)
        self.wgt_jet_length.valueChanged.connect(self.set_jet_length)

        self.wgt_jet_velocity = DoubleSpinBoxMod1()
        self.wgt_jet_velocity.setValue(self.velocity.value)
        self.wgt_jet_velocity.valueChanged.connect(self.set_jet_velocity)

        result = [
            SceneObjProperty(key=self.length.description, widget=self.wgt_jet_length),
            SceneObjProperty(key=self.velocity.description, widget=self.wgt_jet_velocity),
            # SceneObjProperty(key=self.jet_obj.length.description, widget=wgt_jet_length),
            # SceneObjProperty(key=self.jet_obj.velocity.description, widget=wgt_jet_velocity),
        ]
        return result

    def set_jet_length(self, value):
        if value <= 0.1:
            self.wgt_jet_length.setValue(self.length.value)
            self.closure_updater_f()
            return
        self.length.value = value
        self.closure_updater_f()

    def set_jet_velocity(self, value):
        self.velocity.last_value = self.velocity.value
        self.velocity.value = value
        self.closure_updater_f()
