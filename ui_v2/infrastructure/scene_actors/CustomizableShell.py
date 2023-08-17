import typing

from PyQt6.QtWidgets import QLineEdit

from ui_v2.infrastructure.cusom_widgets import DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty, CatalogItemTypes
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface


def NEW_CustomizableSell(property_displayer: typing.Callable[[dict], None]):
    # TODO: (проверить) надо шел возвращать как инстанс класса а не генераторная функция тк шел всегда единственный
    #  должен быть
    return lambda :CustomizableShell(property_displayer)


class CustomizableShell(ActorInterface):
    """Calculation parameters"""

    _jet_material_density: float = 8.96
    _jet_dynamic_yield_stress: float = 824
    _jet_diameter: float = 45
    _jet_velocity: float = 9
    _jet_diameter_increase_factor: float = 1.2

    # TODO: надо это свойство сделать общим для всех объектов (все объекты
    #  сцены должны наследовать так же общий интерфейс):
    CONST_ITEM_TYPE = CatalogItemTypes.shell

    def __init__(self, property_displayer: typing.Callable[[dict], None]):
        self.property_displayer = property_displayer

    def set_props(self):
        props = self._get_props_dict()
        self.property_displayer(props)

    def _get_props_dict(self) -> list[SceneObjProperty]:

        wgt_jet_material_density = DoubleSpinBoxMod1()
        wgt_jet_material_density.setValue(self._jet_material_density)
        wgt_jet_material_density.valueChanged.connect(self.set_jet_material_density)



        wgt_jet_dynamic_yield_stress = DoubleSpinBoxMod1()
        wgt_jet_dynamic_yield_stress.setValue(self._jet_dynamic_yield_stress)
        wgt_jet_dynamic_yield_stress.valueChanged.connect(self.set_dynamic_yield_stress)

        wgt_jet_diameter = DoubleSpinBoxMod1()
        wgt_jet_diameter.setValue(self._jet_diameter)
        wgt_jet_diameter.valueChanged.connect(self.set_jet_diameter)

        wgt_jet_velocity = QLineEdit(str(self._jet_velocity))
        wgt_jet_velocity.textChanged.connect(self.set_jet_velocity)

        wgt_jet_diameter_increase_factor = DoubleSpinBoxMod1()
        wgt_jet_diameter_increase_factor.setValue(self._jet_diameter_increase_factor)
        wgt_jet_diameter_increase_factor.valueChanged.connect(self.set_jet_diameter_increase_factor)

        result = [
            SceneObjProperty(key='Плотность материала КС [P, г/см3]', widget=wgt_jet_material_density),
            SceneObjProperty(key='Динамический предел текучести материала КС [Q, МПа]', widget=wgt_jet_dynamic_yield_stress),
            SceneObjProperty(key='Диаметр КС [d, мм]', widget=wgt_jet_diameter),
            SceneObjProperty(key='Скорость КС [V, км/]', widget=wgt_jet_velocity),
            SceneObjProperty(key='Коэффициент увеличения диаметра КС [æ]', widget=wgt_jet_diameter_increase_factor),
        ]
        return result

    def set_jet_material_density(self, value):
        self._jet_material_density = value

    def set_dynamic_yield_stress(self, value):
        self._dynamic_yield_stress = value

    def set_jet_diameter(self, value):
        self._jet_diameter = value

    def set_jet_velocity(self, value):
        self._jet_velocity = value

    def set_jet_diameter_increase_factor(self, value):
        self._jet_diameter_increase_factor = value































