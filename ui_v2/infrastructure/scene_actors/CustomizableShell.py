import typing

from PyQt6.QtWidgets import QLineEdit, QLabel, QComboBox

from ui_v2.infrastructure.cusom_widgets import DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty, CatalogItemTypes, CumulativeLiningMaterials
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface


def NEW_CustomizableSell(property_displayer: typing.Callable[[dict], None]):
    # TODO: (проверить) надо шел возвращать как инстанс класса а не генераторная функция тк шел всегда единственный
    #  должен быть
    return lambda :CustomizableShell(property_displayer)


class CustomizableShell(ActorInterface):
    """Calculation parameters"""

    explosive_charge_density: float = 1.25
    explosive_charge_detonation_velocity: float = 6.66
    explosive_charge_length: float = 130

    cumulative_lining_length: float = 70
    cumulative_lining_diameter: float = 61
    cumulative_lining_wessel_thickness: float = 0.03
    cumulative_lining_dh: float = 7
    cumulative_lining_material: float = CumulativeLiningMaterials.Steel

    wessel_diameter: float = 74
    wessel_density: float = 7.8

    # jet_material_density: float = 8.96
    # jet_dynamic_yield_stress: float = 824
    # jet_diameter: float = 45
    # jet_velocity: float = 9
    # jet_diameter_increase_factor: float = 1.2

    """Render parameters"""
    closure_updater_f: typing.Callable[[None], None] = lambda x: print(f'{x} assign closure updater func')

    # TODO: надо это свойство сделать общим для всех объектов (все объекты
    #  сцены должны наследовать так же общий интерфейс):
    CONST_ITEM_TYPE = CatalogItemTypes.shell

    def __init__(self, property_displayer: typing.Callable[[dict], None]):
        self.property_displayer = property_displayer

    def set_props(self):
        props = self._get_props_dict()
        self.property_displayer(props)

    def _get_props_dict(self) -> list[SceneObjProperty]:

        wgt_label_main = QLabel("Параметры снаряда")
        wgt_label_main.setStyleSheet('background-color: white')

        wgt_label_explosive_charge = QLabel("Заряд ВВ:")
        wgt_label_explosive_charge.setStyleSheet('background-color: white')

        wgt_explosive_charge_density = DoubleSpinBoxMod1()
        wgt_explosive_charge_density.setValue(self.explosive_charge_density)
        wgt_explosive_charge_density.valueChanged.connect(self.set_explosive_charge_density)

        wgt_explosive_charge_detonation_velocity = DoubleSpinBoxMod1()
        wgt_explosive_charge_detonation_velocity.setValue(self.explosive_charge_detonation_velocity)
        wgt_explosive_charge_detonation_velocity.valueChanged.connect(self.set_explosive_charge_detonation_velocity)

        wgt_explosive_charge_length = DoubleSpinBoxMod1()
        wgt_explosive_charge_length.setValue(self.explosive_charge_length)
        wgt_explosive_charge_length.valueChanged.connect(self.set_explosive_charge_length)

        wgt_label_cunulative_lining = QLabel("Кумулятивная облицовка")
        wgt_label_cunulative_lining.setStyleSheet('background-color: white')

        wgt_cumulative_lining_length = DoubleSpinBoxMod1()
        wgt_cumulative_lining_length.setValue(self.cumulative_lining_length)
        wgt_cumulative_lining_length.valueChanged.connect(self.set_cumulative_lining_length)

        wgt_cumulative_lining_diameter = DoubleSpinBoxMod1()
        wgt_cumulative_lining_diameter.setValue(self.cumulative_lining_diameter)
        wgt_cumulative_lining_diameter.valueChanged.connect(self.set_cumulative_lining_diameter)

        wgt_cumulative_lining_wessel_thikness = DoubleSpinBoxMod1()
        wgt_cumulative_lining_wessel_thikness.setValue(self.cumulative_lining_wessel_thickness)
        wgt_cumulative_lining_wessel_thikness.valueChanged.connect(self.set_cumulative_lining_wessel_thickness)

        wgt_cumulative_lining_dh = DoubleSpinBoxMod1()
        wgt_cumulative_lining_dh.setValue(self.cumulative_lining_dh)
        wgt_cumulative_lining_dh.valueChanged.connect(self.set_cumulative_lining_dh)

        wgt_cumulative_lining_material = QComboBox()
        wgt_cumulative_lining_material.addItem(CumulativeLiningMaterials.Steel)
        wgt_cumulative_lining_material.addItem(CumulativeLiningMaterials.Copper)
        wgt_cumulative_lining_material.addItem(CumulativeLiningMaterials.Duralumin)
        wgt_cumulative_lining_material.currentTextChanged.connect(self.set_cumulative_lining_material)

        wgt_label_wessel = QLabel('Оболочка:')
        wgt_label_wessel.setStyleSheet('background-color: white')

        wgt_wessel_diameter = DoubleSpinBoxMod1()
        wgt_wessel_diameter.setValue(self.wessel_diameter)
        wgt_wessel_diameter.valueChanged.connect(self.set_wessel_diameter)

        wgt_wessel_density = DoubleSpinBoxMod1()
        wgt_wessel_density.setValue(self.wessel_density)
        wgt_wessel_density.valueChanged.connect(self.set_wessel_density)

        result = [
            SceneObjProperty(key='', widget=wgt_label_main),
            # SceneObjProperty(key=wgt_label_main.text(), widget=QLabel()),
            SceneObjProperty(key='', widget=wgt_label_explosive_charge),
            # SceneObjProperty(key=wgt_label_explosive_charge.text(), widget=QLabel()),
            SceneObjProperty(key='Плотность ВВ [ρ вв, г/см3]', widget=wgt_explosive_charge_density),
            SceneObjProperty(key='Скорость детонации [D, км/с]', widget=wgt_explosive_charge_detonation_velocity),
            SceneObjProperty(key='Общая длина заряда [H, мм]', widget=wgt_explosive_charge_length),
            SceneObjProperty(key='', widget=wgt_label_cunulative_lining),
            # SceneObjProperty(key=wgt_label_cunulative_lining.text(), widget=QLabel()),
            SceneObjProperty(key='Длина КО [h, мм]', widget=wgt_cumulative_lining_length),
            SceneObjProperty(key='Диаметр КО [dko, мм]', widget=wgt_cumulative_lining_diameter),
            SceneObjProperty(key='Толщина стенки [δ, мм]', widget=wgt_cumulative_lining_wessel_thikness),
            SceneObjProperty(key='dh [dh, мм]', widget=wgt_cumulative_lining_dh),
            SceneObjProperty(key='Материал', widget=wgt_cumulative_lining_material),
            SceneObjProperty(key='', widget=wgt_label_wessel),
            # SceneObjProperty(key=wgt_label_wessel.text(), widget=QLabel()),
            SceneObjProperty(key='Диаметр оболочки [d об, мм]', widget=wgt_wessel_diameter),
            SceneObjProperty(key='Плотность оболочки [ρ об, г/см3]', widget=wgt_wessel_density),
        ]
        return result

    def _get_props_dict_old(self) -> list[SceneObjProperty]:

        wgt_jet_material_density = DoubleSpinBoxMod1()
        wgt_jet_material_density.setValue(self.jet_material_density)
        wgt_jet_material_density.valueChanged.connect(self.set_jet_material_density)



        wgt_jet_dynamic_yield_stress = DoubleSpinBoxMod1()
        wgt_jet_dynamic_yield_stress.setValue(self.jet_dynamic_yield_stress)
        wgt_jet_dynamic_yield_stress.valueChanged.connect(self.set_dynamic_yield_stress)

        wgt_jet_diameter = DoubleSpinBoxMod1()
        wgt_jet_diameter.setValue(self.jet_diameter)
        wgt_jet_diameter.valueChanged.connect(self.set_jet_diameter)

        wgt_jet_velocity = QLineEdit(str(self.jet_velocity))
        wgt_jet_velocity.textChanged.connect(self.set_jet_velocity)

        wgt_jet_diameter_increase_factor = DoubleSpinBoxMod1()
        wgt_jet_diameter_increase_factor.setValue(self.jet_diameter_increase_factor)
        wgt_jet_diameter_increase_factor.valueChanged.connect(self.set_jet_diameter_increase_factor)

        result = [
            SceneObjProperty(key='Плотность материала КС [P, г/см3]', widget=wgt_jet_material_density),
            SceneObjProperty(key='Динамический предел текучести материала КС [Q, МПа]', widget=wgt_jet_dynamic_yield_stress),
            SceneObjProperty(key='Диаметр КС [d, мм]', widget=wgt_jet_diameter),
            SceneObjProperty(key='Скорость КС [V, км/]', widget=wgt_jet_velocity),
            SceneObjProperty(key='Коэффициент увеличения диаметра КС [æ]', widget=wgt_jet_diameter_increase_factor),
        ]
        return result

    def set_explosive_charge_density(self, value):
        self.explosive_charge_density = value
        self.closure_updater_f()

    def set_jet_material_density(self, value):
        self.jet_material_density = value
        self.closure_updater_f()

    def set_dynamic_yield_stress(self, value):
        self._dynamic_yield_stress = value
        self.closure_updater_f()

    def set_jet_diameter(self, value):
        self.jet_diameter = value
        self.closure_updater_f()

    def set_jet_velocity(self, value):
        self.jet_velocity = value
        self.closure_updater_f()

    def set_jet_diameter_increase_factor(self, value):
        self.jet_diameter_increase_factor = value
        self.closure_updater_f()

    def set_explosive_charge_detonation_velocity(self, value):
        self.explosive_charge_detonation_velocity = value
        self.closure_updater_f()

    def set_explosive_charge_length(self, value):
        self.explosive_charge_length = value
        self.closure_updater_f()

    def set_cumulative_lining_length(self, value):
        self.cumulative_lining_length = value
        self.closure_updater_f()

    def set_cumulative_lining_diameter(self, value):
        self.cumulative_lining_diameter = value
        self.closure_updater_f()

    def set_cumulative_lining_wessel_thickness(self, value):
        self.cumulative_lining_wessel_thickness = value
        self.closure_updater_f()

    def set_cumulative_lining_dh(self, value):
        self.cumulative_lining_dh = value
        self.closure_updater_f()

    def set_cumulative_lining_material(self, value):  # FIXME bm face some trule here because of Enum tipe. mb no 😁
        self.cumulative_lining_material = value
        self.closure_updater_f()

    def set_wessel_diameter(self, value):
        self.wessel_diameter = value
        self.closure_updater_f()

    def set_wessel_density(self, value):
        self.wessel_density = value
        self.closure_updater_f()















