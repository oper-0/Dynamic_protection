import math
import typing

from PyQt6 import QtWidgets
from PyQt6.QtCore import QRect, Qt, QPointF, QPoint, QSize, QRectF, QDate, QLineF
from PyQt6.QtGui import QPainter, QBrush, QPen, QTransform
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QCheckBox, QDateEdit, QDial, QDoubleSpinBox, QSpinBox, QSlider, \
    QLineEdit

from ui_v2.infrastructure.cusom_widgets import LabelAndSlider, LabelAndSpin, DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty


def NEW_CustomizableSell(property_displayer: typing.Callable[[dict], None]):
    return lambda :CustomizableSell(property_displayer)


class CustomizableSell():
    """Calculation parameters"""

    _jet_material_density: float = 8.96
    _jet_dynamic_yield_stress: float = 824
    _jet_diameter: float = 45
    _jet_velocity: float = 9
    _jet_diameter_increase_factor: float = 1.2

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

def NEW_ExplosiveReactiveArmourPlate(property_displayer: typing.Callable[[dict], None]):
    return lambda :ExplosiveReactiveArmourPlate(property_displayer)
    # return ExplosiveReactiveArmourPlate(property_displayer) # fixme раньше ретунил класс, но тпеерь инстанс -> сингл


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
    # _scale_coefficient = 3
    #
    # _element_length_2draw: float = _element_length * _scale_coefficient
    # _element_width_2draw: float = _element_width * _scale_coefficient
    # _face_plate_thickness_2draw: float = _face_plate_thickness * _scale_coefficient
    # _rear_plate_thickness_2draw: float = _rear_plate_thickness * _scale_coefficient
    # _explosive_layer_thickness_2draw: float = _explosive_layer_thickness * _scale_coefficient

    position: QPointF = QPointF(0, 0)
    pen: QPen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
    brush: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.Dense6Pattern)

    """Closures to MainWindow"""
    # Функция виджета основного окна для отображения свойств элемента. {'Эмпирический коэффициент': _empirical_coefficient, ...}
    _show_properties: typing.Callable[[dict], None]

    def __init__(self, property_displayer: typing.Callable[[dict], None]):
        super().__init__()
        self.property_displayer = property_displayer

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.line = QLineF(-1,0,1,0)

        self.rect = self._get_rect()

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
        painter.setPen(self.pen)
        # painter.drawRect(self._get_rect())
        painter.drawRect(self.rect)

    def get_half_height(self):
        return self.rect.height()*math.cos(self._tilt_angle)/2

    def get_center(self) -> QPointF:
        return QPointF(self.scenePos().x(), 0)
        # return self.scenePos()
        # return self.pos()

    def _get_rect(self):
        return QRectF(
            QPointF(self.position.x() - self._explosive_layer_thickness / 2 - self._face_plate_thickness,
                    self.position.y() - self._element_length / 2),
            QPointF(self.position.x() + self._explosive_layer_thickness / 2 - self._rear_plate_thickness,
                    self.position.y() + self._element_length / 2))


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

class DynamicProtectionElement(QGraphicsItem):

    """Calculation parameters"""
    _scale_coefficient = 3

    _empirical_coefficient: float = 4.5
    _tilt_angle: float = 68
    _face_plate_density: float = 7.85
    _rear_plate_density: float = 7.85
    _dynamic_yield_stress: float = 500

    _element_length: float = 260#*_scale_coefficient
    _element_width: float = 138#*_scale_coefficient
    _face_plate_thickness: float = 1.5#*_scale_coefficient
    _rear_plate_thickness: float = 1.5#*_scale_coefficient
    _explosive_layer_thickness: float = 10#*_scale_coefficient

    _element_length_2draw: float = _element_length*_scale_coefficient
    _element_width_2draw: float = _element_width*_scale_coefficient
    _face_plate_thickness_2draw: float = _face_plate_thickness*_scale_coefficient
    _rear_plate_thickness_2draw: float = _rear_plate_thickness*_scale_coefficient
    _explosive_layer_thickness_2draw: float = _explosive_layer_thickness*_scale_coefficient

    _explosive_density: float = 1.6
    _explosive_detonation_velocity: float = 8000
    _explosive_detonation_critical_diameter: float = 0.5

    _detonation_products_polytropic_index: float = 3
    _detonation_product_velocity_parameter_z: float = 0.16667
    _detonation_product_velocity_parameter_r: float = 0.08333
    _detonation_pressure: float = 20000

    _average_pressure_coefficient: float = 0.8

    _distance: float = 0

    """Drawing parameters"""
    # position: QPointF

    border_pen: QPen = QPen(Qt.GlobalColor.black, 1)

    face_plate_brush: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.Dense3Pattern)
    rear_plate_brush: QBrush = QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.Dense3Pattern)
    explosion_brush: QBrush = QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.Dense6Pattern)
    face_plate_brush_highlight: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.SolidPattern)
    rear_plate_brush_highlight: QBrush = QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern)
    explosion_brush_highlight: QBrush = QBrush(Qt.GlobalColor.yellow, Qt.BrushStyle.SolidPattern)

    def __init__(self, position: QPointF = QPointF(0, 0)):
        super().__init__()
        # self.setRotation(45)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        # self.checked_effect = QtWidgets.QGraphicsBlurEffect()
        # self.checked_effect = QtWidgets.QGraphicsColorizeEffect()
        # self.checked_effect.setEnabled(False)
        # self.setGraphicsEffect(self.checked_effect)

        # self.position = position

        self.highlight_flag = False

    def mouseMoveEvent(self, event):
        # print('mouse moving')
        # self.position=event.scenePos()
        super(DynamicProtectionElement, self).mouseMoveEvent(event)

    def boundingRect(self) -> QRectF:
        return self.getBoundingRect

    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     # self.checked_effect.setEnabled(True)
    #     ...
    #
    # def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     self.highlight_flag = True
    #
    # def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
    #     # self.checked_effect.setEnabled(False)
    #     # self.position = event.pos()
    #     # print(f"psition is {self.position}")
    #     ...

    # def itemChange(self, change: 'QGraphicsItem.GraphicsItemChange', value: typing.Any) -> typing.Any:
    #     if change==QGraphicsItem.GraphicsItemChange.ItemPositionChange:
    #         print(11111)

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...) -> None:

        # positon = QPointF(0, 0)
        # self.painter = painter

        # positon = QPointF(0, 0)
        # self.position = QPointF(0, self.position.y())
        positon = self.scenePos()
        # positon = self.pos()
        # print(f"pos is {self.position}")
        painter.setPen(self.border_pen)

        # face_plate_rect = QRect(
        #     QPoint(int(positon.x() - self.explosive_layer_thickness / 2 - self.face_plate_thickness),
        #            int(positon.y() - self.element_length / 2)),
        #     QSize(int(self.face_plate_thickness), int(self.element_length)))
        #
        # explosion_layer_rect = QRect(QPoint(int(positon.x() - self.explosive_layer_thickness / 2),
        #                                     int(positon.y() - self.element_length / 2)),
        #                              QSize(int(self.explosive_layer_thickness), int(self.element_length)))
        #
        # rear_plate_rect = QRect(QPoint(int(positon.x() + self.explosive_layer_thickness / 2),
        #                                int(positon.y() - self.element_length / 2)),
        #                         QSize(int(self.rear_plate_thickness), int(self.element_length)))

        face_plate_rect = QRect(
            QPoint(int(positon.x() - self._explosive_layer_thickness_2draw / 2 - self._face_plate_thickness_2draw),
                   int(positon.y() - self._element_length_2draw / 2)),
            QSize(int(self._face_plate_thickness_2draw), int(self._element_length_2draw)))

        explosion_layer_rect = QRect(QPoint(int(positon.x() - self._explosive_layer_thickness_2draw / 2),
                                            int(positon.y() - self._element_length_2draw / 2)),
                                     QSize(int(self._explosive_layer_thickness_2draw), int(self._element_length_2draw)))

        rear_plate_rect = QRect(QPoint(int(positon.x() + self._explosive_layer_thickness_2draw / 2),
                                       int(positon.y() - self._element_length_2draw / 2)),
                                QSize(int(self._rear_plate_thickness_2draw), int(self._element_length_2draw)))

        if self.highlight_flag:
            painter.fillRect(face_plate_rect, self.face_plate_brush_highlight)
            painter.fillRect(explosion_layer_rect, self.explosion_brush_highlight)
            painter.fillRect(rear_plate_rect, self.rear_plate_brush_highlight)
            painter.drawRect(face_plate_rect)
            painter.drawRect(explosion_layer_rect)
            painter.drawRect(rear_plate_rect)
        else:
            painter.fillRect(face_plate_rect, self.face_plate_brush)
            painter.fillRect(explosion_layer_rect, self.explosion_brush)
            painter.fillRect(rear_plate_rect, self.rear_plate_brush)
            painter.drawRect(face_plate_rect)
            painter.drawRect(explosion_layer_rect)
            painter.drawRect(rear_plate_rect)




        painter.drawEllipse(self.scenePos(), 10, 10)
        # painter.drawEllipse(self.position)
        # painter.drawEllipse(self.position)
        # tmp_pen = QPen(Qt.GlobalColor.green, 1)
        # painter.setPen(tmp_pen)
        # self.border_pen.setColor(Qt.GlobalColor.green)

    # def scale_x_in(self):
    #     self._face_plate_thickness *= self._scale_x_coef[0]  # *3
    #     self._rear_plate_thickness *= self._scale_x_coef[0]  # *3
    #     self._explosive_layer_thickness *= self._scale_x_coef[0]  # *3
    #
    # def scale_x_out(self):
    #     self._face_plate_thickness *= self._scale_x_coef[1]  # *3
    #     self._rear_plate_thickness *= self._scale_x_coef[1]  # *3
    #     self._explosive_layer_thickness *= self._scale_x_coef[1]  # *3
    #
    # def scale_y_in(self):
    #     self._element_length *= self._scale_y_coef[0]
    #
    # def scale_y_out(self):
    #     self._element_length *= self._scale_y_coef[1]

    def scale_object(self, coef: float):
        self._face_plate_thickness *= coef
        self._rear_plate_thickness *= coef
        self._explosive_layer_thickness *= coef

        self._element_length *= coef


    # def mack_thicker(self, coeff) -> None:
    #     self._face_plate_thickness *= coeff  # *3
    #     self._rear_plate_thickness *= coeff  # *3
    #     self._explosive_layer_thickness *= coeff  # *3
    #
    # def mack_longer(self, coeff) -> None:
    #     self._element_length *= coeff

    @property
    def getBoundingRect(self):
        # return QRectF(QPointF(self.pos().x() - self.explosive_layer_thickness / 2 - self.face_plate_thickness,
        #                       self.pos().y() - self.element_length / 2),
        #               QPointF(self.pos().x() + self.explosive_layer_thickness / 2 - self.rear_plate_thickness,
        #                       self.pos().y() + self.element_length / 2))

        # return QRectF(QPointF(self.position.x() - self._explosive_layer_thickness_2draw / 2 - self._face_plate_thickness_2draw,
        #                       self.position.y() - self._element_length_2draw / 2),
        #               QPointF(self.position.x() + self._explosive_layer_thickness_2draw / 2 - self._rear_plate_thickness_2draw,
        #                       self.position.y() + self._element_length_2draw / 2))

        return QRectF(
            QPointF(self.scenePos().x() - self._explosive_layer_thickness_2draw / 2 - self._face_plate_thickness_2draw,
                    self.scenePos().y() - self._element_length_2draw / 2),
            QPointF(self.scenePos().x() + self._explosive_layer_thickness_2draw / 2 - self._rear_plate_thickness_2draw,
                    self.scenePos().y() + self._element_length_2draw / 2))

    @property
    def empirical_coefficient(self):
        """
        Эмпирический коэффициент
        """
        return self._empirical_coefficient

    @empirical_coefficient.setter
    def empirical_coefficient(self, new):
        self._empirical_coefficient = new

    @property
    def face_plate_thickness(self):
        """
        Толщина лицевой пластины (мм)
        """
        return self._face_plate_thickness

    @face_plate_thickness.setter
    def face_plate_thickness(self, new):
        self._face_plate_thickness = new

    @property
    def rear_plate_thickness(self):
        """
        Толщина тыльной пластины (мм)
        """
        return self._rear_plate_thickness

    @rear_plate_thickness.setter
    def rear_plate_thickness(self, new):
        self._rear_plate_thickness = new

    @property
    def tilt_angle(self):
        """
        Угол между кумулятивной струей и нормалью к пластине (градусы)
        """
        return self._tilt_angle

    @tilt_angle.setter
    def tilt_angle(self, new):
        self._tilt_angle = new

    @property
    def face_plate_density(self):
        """
        Плотность материала лицевой пластины (г/см3)
        """
        return self._face_plate_density

    @face_plate_density.setter
    def face_plate_density(self, new):
        self._face_plate_density = new

    @property
    def rear_plate_density(self):
        """
        Плотность материала тыльной пластины (г/см3)
        """
        return self._rear_plate_density

    @rear_plate_density.setter
    def rear_plate_density(self, new):
        self._rear_plate_density = new

    @property
    def dynamic_yield_stress(self):
        """
        Динамический предел текучести материала пластины (МПа)
        """
        return self._dynamic_yield_stress

    @dynamic_yield_stress.setter
    def dynamic_yield_stress(self, new):
        self._dynamic_yield_stress = new

    @property
    def element_length(self):
        """
        Длина пластины (мм)
        """
        return self._element_length

    @element_length.setter
    def element_length(self, new):
        self._element_length = new

    @property
    def element_width(self):
        """
        Ширина пластины (мм)
        """
        return self._element_width

    @element_width.setter
    def element_width(self, new):
        self._element_width = new

    @property
    def explosive_layer_thickness(self):
        """
        Толщина слоя взрывчатого вещества (мм)
        """
        return self._explosive_layer_thickness

    @explosive_layer_thickness.setter
    def explosive_layer_thickness(self, new):
        self._explosive_layer_thickness = new

    @property
    def explosive_density(self):
        """
        Плотность взрывчатого вещества (г/см3)
        """
        return self._explosive_density

    @explosive_density.setter
    def explosive_density(self, new):
        self._explosive_density = new

    @property
    def explosive_detonation_velocity(self):
        """
        Скорость детонации заряда взрывчатого вещества (м/с)
        """
        return self._explosive_detonation_velocity

    @explosive_detonation_velocity.setter
    def explosive_detonation_velocity(self, new):
        self._explosive_detonation_velocity = new

    @property
    def explosive_detonation_critical_diameter(self):
        """
        Критический диаметр детонации взрывчатого вещества (мм)
        """
        return self._explosive_detonation_critical_diameter

    @explosive_detonation_critical_diameter.setter
    def explosive_detonation_critical_diameter(self, new):
        self._explosive_detonation_critical_diameter = new

    @property
    def detonation_products_polytropic_index(self):
        """
        Показатель политропы продуктов детонации
        """
        return self._detonation_products_polytropic_index

    @detonation_products_polytropic_index.setter
    def detonation_products_polytropic_index(self, new):
        self._detonation_products_polytropic_index = new

    @property
    def detonation_product_velocity_parameter_z(self):
        """
        Параметр z распределения скоростей продуктов детонации
        """
        return self._detonation_product_velocity_parameter_z

    @detonation_product_velocity_parameter_z.setter
    def detonation_product_velocity_parameter_z(self, new):
        self._detonation_product_velocity_parameter_z = new

    @property
    def detonation_product_velocity_parameter_r(self):
        """
        Параметр r распределения скоростей продуктов детонации
        """
        return self._detonation_product_velocity_parameter_r

    @detonation_product_velocity_parameter_r.setter
    def detonation_product_velocity_parameter_r(self, new):
        self._detonation_product_velocity_parameter_r = new

    @property
    def detonation_pressure(self):
        """
        Давление детонации (МПа)
        """
        return self._detonation_pressure

    @detonation_pressure.setter
    def detonation_pressure(self, new):
        self._detonation_pressure = new

    @property
    def average_pressure_coefficient(self):
        """
        Коэффициент для среднего давления
        """
        return self._average_pressure_coefficient

    @average_pressure_coefficient.setter
    def average_pressure_coefficient(self, new):
        self._average_pressure_coefficient = new


class test_item(QGraphicsItem):

    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.pen = QPen(Qt.PenStyle.SolidLine)
        self.pen.setColor(Qt.GlobalColor.black)
        self.pen.setWidth(8)
        self.brush = QBrush(Qt.GlobalColor.red)

        self.rect = QRectF(QPointF(0,0),QPointF(15,15))

    def mouseMoveEvent(self, event):
        super(test_item, self).mouseMoveEvent(event)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)


































