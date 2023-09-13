import math
import typing

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QPointF, QRectF, QLineF
from PyQt6.QtGui import  QBrush, QPen, QTransform
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QLineEdit

from ui_v2.infrastructure.cusom_widgets import LabelAndSlider, DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty, CatalogItemTypes
from ui_v2.infrastructure.scene_actors.Jet import Jet
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface


def NEW_ExplosiveReactiveArmourPlate(property_displayer: typing.Callable[[dict], None]):
    return lambda :ExplosiveReactiveArmourPlate(property_displayer)


class ExplosiveReactiveArmourPlate(QGraphicsItem):
    """Calculation parameters"""

    _empirical_coefficient: float = 4.5
    _tilt_angle: float = 0
    _face_plate_density: float = 7.85
    _rear_plate_density: float = 7.85
    _dynamic_yield_stress: float = 500

    _element_length: float = 260
    _element_width: float = 138
    _face_plate_thickness: float = 1.5
    _rear_plate_thickness: float = 1.5
    _explosive_layer_thickness: float = 10

    _explosive_density: float = 1.6
    _explosive_detonation_velocity: float = 8000
    _explosive_detonation_critical_diameter: float = 0.5

    _detonation_products_polytropic_index: float = 3
    _detonation_product_velocity_parameter_z: float = 0.16667
    _detonation_product_velocity_parameter_r: float = 0.08333
    _detonation_pressure: float = 20000

    _average_pressure_coefficient: float = 0.8

    # _distance: float = 0

    """Drawing parameters"""
    _is_focused: bool = True
    pen_on_focus: QPen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashLine)
    # brush_on_focus: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.Dense6Pattern)
    position: QPointF = QPointF(0, 0)
    pen: QPen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
    brush: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.Dense6Pattern)

    """Closures to MainWindow"""
    # Функция виджета основного окна для отображения свойств элемента. {'Эмпирический коэффициент': _empirical_coefficient, ...}
    _show_properties: typing.Callable[[dict], None]

    # общее свойство для всех объектов сцены
    CONST_ITEM_TYPE = CatalogItemTypes.armor

    def __init__(self, property_displayer: typing.Callable[[dict], None]):
        super().__init__()
        self.property_displayer = property_displayer

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.line = QLineF(-1,0,1,0)

        self.rect = self._get_rect()
        # self.rect.setFlag

    def itemChange(self, change, value):
        if (
                change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
                and self.isSelected()
                and not self.line.isNull()
        ):
            p1 = self.line.p1()
            p2 = self.line.p2()
            e1 = p2 - p1
            e2 = value - p1
            dp = QPointF.dotProduct(e1, e2)
            l = QPointF.dotProduct(e1, e1)
            p = p1 + dp * e1 / l
            return p
        return super().itemChange(change, value)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self._is_focused = True
        props = self._get_props_dict()
        self.property_displayer(props)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def boundingRect(self):
        return self.rect

    def set_position(self,pos:QPointF):
        # self.position=pos
        # self.setPos(pos)
        print(f"ITEM POSITION IS {pos}")
        self.setPos(pos)
        # self.rect.moveTo(pos)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(self.brush)
        if self._is_focused:
            painter.setPen(self.pen_on_focus)
        else:
            painter.setPen(self.pen)
        # painter.drawRect(self._get_rect())
        painter.drawRect(self.rect)

    def unfocus(self):
        self._is_focused = False

    def get_half_height(self):
        return self.rect.height()*math.cos(self._tilt_angle)/2

    def get_center(self) -> QPointF:
        return QPointF(self.scenePos().x(), 0)

    def _get_rect(self):
        return QRectF(
            QPointF(self.position.x() - self._explosive_layer_thickness / 2 - self._face_plate_thickness,
                    self.position.y() - self._element_length / 2),
            QPointF(self.position.x() + self._explosive_layer_thickness / 2 - self._rear_plate_thickness,
                    self.position.y() + self._element_length / 2))

    """Calculator. Общий метод для всех объектов брони на сцене"""
    def calc_jet_impact(self, jet: Jet) -> Jet:
        if hasattr(jet, "cursor_position"):
            jet.length.value *= 0.5   # FIXME temp solution
        return jet

    def _get_props_dict(self) -> list[SceneObjProperty]:

        wgt_empirical_coefficient = QLineEdit(str(self._empirical_coefficient))
        wgt_empirical_coefficient.textChanged.connect(self.set_empirical_coefficient)

        wgt_face_plate_thickness = DoubleSpinBoxMod1()
        wgt_face_plate_thickness.setValue(self._face_plate_thickness)
        wgt_face_plate_thickness.valueChanged.connect(self.set_face_plate_thickness)

        wgt_rear_plate_thickness = DoubleSpinBoxMod1()
        wgt_rear_plate_thickness.setValue(self._rear_plate_thickness)
        wgt_rear_plate_thickness.valueChanged.connect(self.set_rear_plate_thickness)

        wgt_tilt_angle = LabelAndSlider(min_val=-90, max_val=90, val=self._tilt_angle, postfix='°')
        wgt_tilt_angle.slider.valueChanged.connect(self.set_tilt_angle)

        wgt_face_plate_density = QLineEdit(str(self._face_plate_density))
        wgt_face_plate_density.textChanged.connect(self.set_face_plate_density)

        wgt_rear_plate_density = QLineEdit(str(self._rear_plate_density))
        wgt_rear_plate_density.textChanged.connect(self.set_rear_plate_density)

        wgt_dynamic_yield_stress = QLineEdit(str(self._dynamic_yield_stress))
        wgt_dynamic_yield_stress.textChanged.connect(self.set_dynamic_yield_stress)

        wgt_element_length = DoubleSpinBoxMod1()
        wgt_element_length.setValue(self._element_length)
        wgt_element_length.valueChanged.connect(self.set_element_length)

        wgt_element_width = DoubleSpinBoxMod1()
        wgt_element_width.setValue(self._element_width)
        wgt_element_width.valueChanged.connect(self.set_element_width)

        wgt_explosive_layer_thickness = DoubleSpinBoxMod1()
        wgt_explosive_layer_thickness.setValue(self._explosive_layer_thickness)
        wgt_explosive_layer_thickness.valueChanged.connect(self.set_explosive_layer_thickness)

        wgt_explosive_density = QLineEdit(str(self._explosive_density))
        wgt_explosive_density.textChanged.connect(self.set_explosive_density)

        wgt_explosive_detonation_velocity = QLineEdit(str(self._explosive_detonation_velocity))
        wgt_explosive_detonation_velocity.textChanged.connect(self.set_explosive_detonation_velocity)

        wgt_explosive_detonation_critical_diameter = QLineEdit(str(self._explosive_detonation_critical_diameter))
        wgt_explosive_detonation_critical_diameter.textChanged.connect(self.set_explosive_detonation_critical_diameter)

        wgt_detonation_products_polytropic_index = QLineEdit(str(self._detonation_products_polytropic_index))
        wgt_detonation_products_polytropic_index.textChanged.connect(self.set_detonation_products_polytropic_index)

        wgt_detonation_product_velocity_parameter_z = QLineEdit(str(self._detonation_product_velocity_parameter_z))
        wgt_detonation_product_velocity_parameter_z.textChanged.connect(self.set_detonation_product_velocity_parameter_z)

        wgt_detonation_product_velocity_parameter_r = QLineEdit(str(self._detonation_product_velocity_parameter_r))
        wgt_detonation_product_velocity_parameter_r.textChanged.connect(self.set_detonation_product_velocity_parameter_r)

        wgt_detonation_pressure = QLineEdit(str(self._detonation_pressure))
        wgt_detonation_pressure.textChanged.connect(self.set_detonation_pressure)

        wgt_average_pressure_coefficient = QLineEdit(str(self._average_pressure_coefficient))
        wgt_average_pressure_coefficient.textChanged.connect(self.set_average_pressure_coefficient)


        result = [
            SceneObjProperty(key='Эмпирический коэффициент [ν]:', widget=wgt_empirical_coefficient),
            SceneObjProperty(key='Толщина лицевой пластины [δ1, мм]', widget=wgt_face_plate_thickness),
            SceneObjProperty(key='Толщина тыльной пластины [δ2, мм]', widget=wgt_rear_plate_thickness),
            SceneObjProperty(key='Угол атаки [θ, град.]:', widget=wgt_tilt_angle),
            SceneObjProperty(key='Плотность лицевой пластины [ρ1, г/см3]', widget=wgt_face_plate_density),
            SceneObjProperty(key='Плотность тыльной пластины [ρ2, г/см3]', widget=wgt_rear_plate_density),
            SceneObjProperty(key='Динамический предел текучести материала пластин [Q, МПа]', widget=wgt_dynamic_yield_stress),
            SceneObjProperty(key='Длина пластины [a, мм]', widget=wgt_element_length),
            SceneObjProperty(key='Ширина пластины [b, мм]', widget=wgt_element_width),
            SceneObjProperty(key='Толщина слоя ВВ [h, мм]', widget=wgt_explosive_layer_thickness),
            SceneObjProperty(key='Плотность ВВ [ρ, г/см3]', widget=wgt_explosive_density),
            SceneObjProperty(key='Скорость детонации заряда ВВ [D, м/с]', widget=wgt_explosive_detonation_velocity),
            SceneObjProperty(key='Критический диаметр детонации ВВ [dкр, мм]', widget=wgt_explosive_detonation_critical_diameter),
            SceneObjProperty(key='Показатель политропы продутов детонации [k]', widget=wgt_detonation_products_polytropic_index),
            SceneObjProperty(key='Распределение z скоростей продуктов детонации [ξz]', widget=wgt_detonation_product_velocity_parameter_z),
            SceneObjProperty(key='Распределение r скоростей продуктов детонации [ξr]', widget=wgt_detonation_product_velocity_parameter_r),
            SceneObjProperty(key='Давление детонации [Pн, МПа]', widget=wgt_detonation_pressure),
            SceneObjProperty(key='Коэффициент для среднего давления [σ]', widget=wgt_average_pressure_coefficient)
        ]
        return result

    """PROPERTIES"""
    def set_empirical_coefficient(self, value):
        self._empirical_coefficient = value

    def set_face_plate_thickness(self, value):
        self._face_plate_thickness = value
        self.rect = self._get_rect()
        self.update()

    def set_rear_plate_thickness(self, value):
        self._rear_plate_thickness = value
        self.rect = self._get_rect()
        self.update()

    def set_tilt_angle(self, value):
        self._tilt_angle = value
        transform = QTransform()
        transform.translate(self.rect.center().x(), self.rect.center().y()).rotate(value).translate(-self.rect.center().x(), -self.rect.center().y())
        self.setTransform(transform)

    def set_face_plate_density(self, value):
        self._face_plate_density = value

    def set_rear_plate_density(self, value):
        self._rear_plate_density = value

    def set_dynamic_yield_stress(self, value):
        self._dynamic_yield_stress = value

    def set_element_length(self, value):
        self._element_length = value
        self.rect = self._get_rect()
        self.update()

    def set_element_width(self, value):
        self._element_width = value

    def set_explosive_layer_thickness(self, value):
        self._explosive_layer_thickness = value
        self.rect = self._get_rect()
        self.update()

    def set_explosive_density(self, value):
        self._explosive_density = value

    def set_explosive_detonation_velocity(self, value):
        self._explosive_detonation_velocity = value

    def set_explosive_detonation_critical_diameter(self, value):
        self._explosive_detonation_critical_diameter = value

    def set_detonation_products_polytropic_index(self, value):
        self._detonation_products_polytropic_index = value

    def set_detonation_product_velocity_parameter_z(self, value):
        self._detonation_product_velocity_parameter_z = value

    def set_detonation_product_velocity_parameter_r(self, value):
        self._detonation_product_velocity_parameter_r = value

    def set_detonation_pressure(self, value):
        self._detonation_pressure = value

    def set_average_pressure_coefficient(self, value):
        self._average_pressure_coefficient = value
