import math
import random
import typing

from PyQt6 import QtWidgets
from PyQt6.QtCore import QRect, Qt, QPointF, QPoint, QSize, QRectF, QDate, QLineF
from PyQt6.QtGui import QPainter, QBrush, QPen, QTransform, QPolygon, QPolygonF
from PyQt6.QtWidgets import QGraphicsItem, QWidget, QCheckBox, QDateEdit, QDial, QDoubleSpinBox, QSpinBox, QSlider, \
    QLineEdit

from ui_v2.infrastructure.cusom_widgets import LabelAndSlider, LabelAndSpin, DoubleSpinBoxMod1
from ui_v2.infrastructure.helpers import SceneObjProperty


def NEW_SemiInfIsotropicElement(property_displayer: typing.Callable[[dict], None],
                                f_get_scene_rect: typing.Callable[[None], QRectF]):
    return lambda: SemiInfIsotropicElement(property_displayer, f_get_scene_rect)
    # return ExplosiveReactiveArmourPlate(property_displayer) # fixme раньше ретунил класс, но тпеерь инстанс -> сингл.


class SemiInfIsotropicElement(QGraphicsItem):
    """Drawing parameters"""
    _is_focused: bool = True
    pen_on_focus: QPen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashLine)
    # brush_on_focus: QBrush = QBrush(Qt.GlobalColor.green, Qt.BrushStyle.Dense6Pattern)
    # position: QPointF = QPointF(0, 0)
    pen: QPen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine)
    brush: QBrush = QBrush(Qt.GlobalColor.darkBlue, Qt.BrushStyle.Dense3Pattern)

    """Closures to MainWindow"""
    # Функция виджета основного окна для отображения свойств элемента. {key: value, ...}
    _show_properties: typing.Callable[[dict], None]

    # hole_depth: float = 200
    # hole_radius: float = 50
    hole_points: list[QPointF] = []

    def __init__(self,
                 property_displayer: typing.Callable[[dict], None],
                 f_get_scene_rect: typing.Callable[[None], QRectF]):
        super().__init__()
        self.property_displayer = property_displayer
        self.f_get_scene_rect = f_get_scene_rect

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.make_hole(30, 200) #FIXME

        # self.line = QLineF(-1,0,1,0)

        # self.rect = self._get_rect()
        # self.polygon = self._get_polygon()

    # def itemChange(self, change, value):
    #     if (
    #             change == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemPositionChange
    #             and self.isSelected()
    #             and not self.line.isNull()
    #     ):
    #         p1 = self.line.p1()
    #         p2 = self.line.p2()
    #         e1 = p2 - p1
    #         e2 = value - p1
    #         dp = QPointF.dotProduct(e1, e2)
    #         l = QPointF.dotProduct(e1, e1)
    #         p = p1 + dp * e1 / l
    #         return p
    #     return super().itemChange(change, value)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self._is_focused = True
        props = self._get_props_dict()
        self.property_displayer(props)
        super().mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)

    # def set_position(self,pos:QPointF):
    #     # self.position=pos
    #     # self.setPos(pos)
    #     print(f"ITEM POSITION IS {pos}")
    #     self.setPos(pos)
    #     # self.rect.moveTo(pos)

    def paint(self, painter, option, widget: typing.Optional[QWidget] = ...) -> None:
        painter.setBrush(self.brush)
        if self._is_focused:
            painter.setPen(self.pen_on_focus)
        else:
            painter.setPen(self.pen)
        painter.drawPolygon(self._get_polygon())

    def unfocus(self):
        self._is_focused = False

    # def get_half_height(self):
    #     return self.rect.height()*math.cos(self._tilt_angle)/2

    # def get_center(self) -> QPointF:
    #     return QPointF(self.scenePos().x(), 0)
    #     # return self.scenePos()
    #     # return self.pos()

    def make_hole(self, radius, depth):  # [(x0,y0),(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5),..]
        step = 10
        max_deviation = radius * 0.1

        points_head = []
        for x in [p * step for p in range(int(depth / step))]:
            points_head.append(QPointF(x, max_deviation * 0.1 * (radius + random.randint(0, 10) - 5)))

        points_tale = []
        for x in reversed(points_head):
            points_tale.append(QPointF(x.x(), x.y()*-1))

        self.hole_points = points_head+points_tale

    def _get_polygon(self):
        rect = self.f_get_scene_rect()

        polygon = QPolygonF([
            QPointF(0, rect.topLeft().y()),
            QPointF(rect.topRight()),
            QPointF(rect.bottomRight()),
            QPointF(0, rect.bottomLeft().y()),
            # hole area
            # *self.get_hole_points(self.hole_radius, self.hole_depth)
            *self.hole_points
        ])

        # polygon = QPolygonF([
        #     QPointF(0, rect.topLeft().y()),
        #     QPointF(rect.topRight()),
        #     QPointF(rect.bottomRight()),
        #     QPointF(0, rect.bottomLeft().y()),
        #     # hole area
        #     QPointF(0, self.hole_radius),
        #     QPointF(self.hole_depth, self.hole_radius),
        #     QPointF(self.hole_depth, -self.hole_radius),
        #     QPointF(0, -self.hole_radius),
        # ])

        return polygon
        # return QPolygonF([
        #     QPointF(0,-100),
        #     QPointF(-100,200),
        #     QPointF(100,200),
        #     QPointF(100,0),
        # ])

    def _get_props_dict(self) -> list[SceneObjProperty]:

        result = [
            # SceneObjProperty(key='Толщина лицевой пластины [δ1, мм]', widget=wgt_face_plate_thickness),
            SceneObjProperty(key='Some vale', widget=QLineEdit('some content')),
        ]

        return result

    """PROPERTIES"""
    # def set_empirical_coefficient(self, value):
    #     self._empirical_coefficient = value
