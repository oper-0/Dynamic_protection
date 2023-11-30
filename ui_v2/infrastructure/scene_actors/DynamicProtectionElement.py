import typing

from PyQt6.QtCore import QRect, Qt, QPointF, QPoint, QSize, QRectF
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QGraphicsOpacityEffect

from ui_v2.infrastructure.helpers import CatalogItemTypes
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface


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

    # общее свойство для всех объектов сцены
    CONST_ITEM_TYPE = CatalogItemTypes.armor

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

        # if item is not fully implemented uncomment next:
        # self.setGraphicsEffect(QGraphicsOpacityEffect())

    def mouseMoveEvent(self, event):
        # print('mouse moving')
        # self.position=event.scenePos()
        super(DynamicProtectionElement, self).mouseMoveEvent(event)

    def boundingRect(self) -> QRectF:
        return self.getBoundingRect

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...) -> None:

        positon = self.scenePos()
        painter.setPen(self.border_pen)

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

    def scale_object(self, coef: float):
        self._face_plate_thickness *= coef
        self._rear_plate_thickness *= coef
        self._explosive_layer_thickness *= coef

        self._element_length *= coef

    @property
    def getBoundingRect(self):
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

    def unfocus(self):
        pass

    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.pen = QPen(Qt.PenStyle.SolidLine)
        self.pen.setColor(Qt.GlobalColor.black)
        self.pen.setWidth(8)
        self.brush = QBrush(Qt.GlobalColor.red)

        self.rect = QRectF(QPointF(0,0),QPointF(15,15))

        # if item is not fully implemented uncomment next:
        # self.setGraphicsEffect(QGraphicsOpacityEffect())


    def mouseMoveEvent(self, event):
        super(test_item, self).mouseMoveEvent(event)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)