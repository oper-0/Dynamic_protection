import typing
from typing import Callable

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QPointF, QLineF, QRectF
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem

from ui_v2.infrastructure.dz_calculation.semi_inf_obstacle import calculation_semi_inf_obst
from ui_v2.infrastructure.helpers import ItemsCollectionInterface, TextOnScene, CatalogItemTypes
from ui_v2.infrastructure.scene_actors.scene_actor_interface import ActorInterface, SceneActorInterface
from ui_v2.infrastructure.scene_actors.semi_inf_isotropic_element import NEW_SemiInfIsotropicElement
from ui_v2.infrastructure.scene_actors.semi_inf_isotropic_element_simplifyed import \
    NEW_SemiInfIsotropicElementSimplified


class ObjectKeeper:
    """keeps and maintain consistency of the scene actors"""
    _objs: list[ActorInterface] = []
    addItem_callback: typing.Callable[[QGraphicsItem], None]

    def __init__(self, addItem_callback: typing.Callable[[QGraphicsItem], None]):
        self.addItem_callback = addItem_callback

    def add_obj(self, obj: ActorInterface):
        """
        adds obj to the container, if CONST_ITEM_TYPE property of obj equals to CatalogItemTypes.shell -> pops (if
        exist) previous then adds current obj
        :param obj:
        """
        if obj.CONST_ITEM_TYPE == CatalogItemTypes.shell:  # объекты снарядов должны быть единственными
            # delete all shell objects among actors
            self._objs = [o for o in self._objs if o.CONST_ITEM_TYPE != CatalogItemTypes.shell]

        self._objs.append(obj)  # adding to container
        # adding to scene if it's not shell.
        if obj.CONST_ITEM_TYPE != CatalogItemTypes.shell:
            self.addItem_callback(obj)  # adding to scene

    def get_shell_obj(self):
        for i in self._objs:
            if i.CONST_ITEM_TYPE == CatalogItemTypes.shell:
                return i

    def get_obstacle_obj(self):
        """
        :return: Объект последнего препятствия - на чем образуется каверна
        """
        for i in self._objs:
            if i.CONST_ITEM_TYPE == CatalogItemTypes.obstacle:
                return i

    def get_all_obstacles(self) -> list:
        """
        :return: Отсортированные объекты препятствий сцены, начиная с ближних к летящей КС
        """
        result_arr = []
        for i in self._objs:
            if i.CONST_ITEM_TYPE == CatalogItemTypes.armor:
                result_arr.append(i)

        result_arr.sort(key=lambda o: o.scenePos().x())  # Sorting elements

        return result_arr


class GraphicsScene(QGraphicsScene):

    status_bar: Callable[[str], None]
    logger: Callable[[str,str], None]
    item_catalog: ItemsCollectionInterface

    scene_obj_distance_lines: list[QLineF]
    scene_obj_distance_vertical_lines: list[QLineF]
    scene_obj_distance_text: list[TextOnScene]
    # scene_obj_distance_text_options: QTextOption = QTextOption(Qt.AlignmentFlag.AlignCenter)

    distance_lines_pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
    distance_vertical_lines_pen = QPen(Qt.GlobalColor.darkRed, 1, Qt.PenStyle.DashLine)

    rect_area: QRectF = QRectF(0, 0, 0, 0)  # FIXME лучше б получать эту арею из вью а не сцены

    v_line_delta = 150

    object_keeper: ObjectKeeper  # контейнер для объектов: защитные элементы, полу-бесконечная преграда и снаряд

    def __init__(self):
        """ wraps self.addItems() method to maintain consistency according scene logic. Means wherever you want to
        use self.addItem() instead use self.objectKeeper.add_obj() """
        super(GraphicsScene, self).__init__()
        self.object_keeper = ObjectKeeper(lambda x: self.addItem(x))

    def get_rect_area(self) -> QRectF:
        return QRectF(
            self.rect_area.topLeft().x(),
            self.rect_area.topLeft().y()*1.5,
            self.rect_area.width()*1.5,
            self.rect_area.height()*1.5,
        )

    # def addItem(self, item: QGraphicsItem) -> None:
    #     self.object_keeper.add_obj(item)

    def drawForeground(self, painter, rect):
        super(GraphicsScene, self).drawForeground(painter, rect)
        painter.save()

        # save rect for closure call when drawing semi infinte isoropic item
        self.rect_area = rect

        # DRAW DISTANCE-LINES BETWEEN OBJECTS ON THE SCENE
        self.scene_obj_distance_lines = []
        self.scene_obj_distance_vertical_lines = []
        self.scene_obj_distance_text = []
        obj_positions: list[QPointF] = self._get_obj_positions(y_delta=self.v_line_delta)
        obj_positions.sort(key=lambda p: p.x())
        if len(obj_positions)>1:
            prev_pos = obj_positions[0]

            # first vertical line
            # v_line = QLineF(prev_pos, QPointF(prev_pos.x(), prev_pos.y() + self.v_line_delta))
            v_line = QLineF(QPointF(prev_pos.x(), 0), prev_pos)
            self.scene_obj_distance_vertical_lines.append(v_line)

            for obj_pos in obj_positions[1:]:
                # horizontal line
                line = QLineF(prev_pos, obj_pos)
                self.scene_obj_distance_lines.append(line)

                # vertical line
                # v_line = QLineF(obj_pos, QPointF(obj_pos.x(), obj_pos.y()+self.v_line_delta))
                v_line = QLineF(QPointF(obj_pos.x(), 0), obj_pos)
                self.scene_obj_distance_vertical_lines.append(v_line)

                text_item = TextOnScene(
                    position=QPointF(line.p1().x()+line.length()/2, line.p1().y()+15),
                    text=f'{int(line.length())}'
                )
                self.scene_obj_distance_text.append(text_item)

                prev_pos = obj_pos
            # v lines
            painter.setPen(self.distance_vertical_lines_pen)
            painter.drawLines(self.scene_obj_distance_vertical_lines)
            # h lines
            painter.setPen(self.distance_lines_pen)
            painter.drawLines(self.scene_obj_distance_lines)
            # text
            for ti in self.scene_obj_distance_text:
                painter.drawText(ti.position, ti.text)

        #  DRAW CROSS UNDER MOUSE
        if not hasattr(self, "cursor_position"):
            return
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(1)
        painter.setPen(pen)
        linex = QtCore.QLineF(
            rect.left(),
            self.cursor_position.y(),
            rect.right(),
            self.cursor_position.y(),
        )
        liney = QtCore.QLineF(
            self.cursor_position.x(),
            rect.top(),
            self.cursor_position.x(),
            rect.bottom(),
        )
        for line in (linex, liney):
            painter.drawLine(line)
        painter.restore()

    def mouseMoveEvent(self, event):
        self.cursor_position = event.scenePos()
        self.update()
        super(GraphicsScene, self).mouseMoveEvent(event)
        # print(self.cursor_position)
        self.status_bar(f"x:{int(self.cursor_position.x())} y:{int(self.cursor_position.y())}")

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self._unfocus_items()
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        # MAKE HOLE IN SEMI_INF_OBSTACLE
        self.calculate()
        super(GraphicsScene, self).mouseReleaseEvent(event)

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        pass

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()


    # def dropEvent(self, event: QtGui.QDropEvent) -> None:
    def dropEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
        self._unfocus_items()
        name = event.mimeData().text()
        item = self.item_catalog.get_item(name)
        scene_item = item.get_scene_item()

        # 💩 magic code, do not touch:
        if hasattr(scene_item, 'get_half_height') and callable(scene_item.get_half_height):
            # item_pos = QPointF(event.scenePos().x(), 0-scene_item.get_half_height())
            item_pos = QPointF(event.scenePos().x(), 0)
            self.logger(f"item dropped on [{int(item_pos.x())}; {int(item_pos.y())}]", 'info')

        if not item:
            self.logger(f"Отсутствует соответствие названия в каталоге для {name}", 'error')
            event.acceptProposedAction()
            return

        # 💩 magic code, do not touch:
        # если дропаемый объект это shell:
        if hasattr(scene_item, 'set_props') and callable(scene_item.set_props):
            # TODO: надо удалять предыдущий шел
            scene_item.set_props()
            scene_item.closure_updater_f = lambda : self.calculate()  # 💩💩💩
            self.object_keeper.add_obj(scene_item)
        else:
            scene_item.set_position(item_pos)
            # self.addItem(scene_item)
            self.object_keeper.add_obj(scene_item)

        event.acceptProposedAction()

    def _get_obj_positions(self, y_delta = 0):
        itms = self.items(Qt.SortOrder.AscendingOrder)
        poss = []
        for i in itms:
            # poss.append(QPointF(i.get_center().x(), i.get_center().y()+y_delta))
            poss.append(QPointF(i.scenePos().x(), i.scenePos().y()+y_delta))
        return poss

    def _unfocus_items(self):
        itm: SceneActorInterface
        for itm in self.items():
            itm.unfocus()

    def wrapper_make_hole(self, radius, depth) -> bool:
        """
        :param radius: радиус каверны в мм
        :param depth: глубина каверны в мм
        :return:
        """
        obstacle = self.object_keeper.get_obstacle_obj()
        if not obstacle:
            return False
        if hasattr(obstacle, 'make_hole') and callable(obstacle.make_hole):
            obstacle.make_hole(radius, depth)
            return True
        raise AttributeError('Объект полу-бесконечного препятствия должен иметь метод make_hole()')

    def get_shell_item(self):
        for itm in self.items():
            if not hasattr(itm, 'CONST_ITEM_TYPE') :
                raise AttributeError('Все объекты сцены должны иметь свойство CONST_ITEM_TYPE со значением из CatalogItemTypes')
            if itm.CONST_ITEM_TYPE == CatalogItemTypes.shell:
                return itm #???????
        return None

    def calculate(self):

        if not self.object_keeper.get_shell_obj():
            self.logger('Невозможно произвести расчёт. Нет выбран снаряд.', 'error')
            return

        armor_objs = self.object_keeper.get_all_obstacles()
        init_shell = self.object_keeper.get_shell_obj()

        for o in armor_objs:
            init_shell = o.calc_jet_impact(init_shell)

        diameter, depth = self.object_keeper.get_obstacle_obj().calculate_hole(init_shell)


        # diameter, depth = calculation_semi_inf_obst(self.object_keeper.get_shell_obj(),
        #                           self.object_keeper.get_obstacle_obj())

        if not self.wrapper_make_hole(diameter/2, depth*1000):  # calculs result displaying
            self.logger('Невозможно произвести расчёт', 'error')

        self.update()


class ControlView(QGraphicsView):
    cell_size = 80
    grid_pen = QPen(Qt.GlobalColor.lightGray, 1, Qt.PenStyle.DashDotDotLine)
    axis_pen = QPen(Qt.GlobalColor.white, 1, Qt.PenStyle.SolidLine)
    axis_pen_x = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.DashLine)
    _zoom = 0

    _isPanning = False
    _mousePressed = False
    def __init__(self,
                 item_catalog: ItemsCollectionInterface,
                 logger_fun: Callable[[str,str], None],
                 status_bar: Callable[[str], None],
                 SemiInfIsotropicElement_property_displayer_fun: typing.Callable[[dict], None]):
        super().__init__()

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        # self.setCacheMode(QGraphicsView.CacheModeFlag.CacheBackground)
        # self.viewport().setMouseTracking(True)
        self.change_pos_mouse_button = Qt.MouseButton.MiddleButton
        self.change_pos_mouse_button_pressed = False
        self.last_mouse_pos = None
        self.start_scene_rect = self.sceneRect()

        self.CVScene = GraphicsScene()
        self.CVScene.status_bar = status_bar
        self.CVScene.logger = logger_fun
        self.CVScene.item_catalog = item_catalog

        # Элемент полу-бесконечной брони
        # self.semi_inf_isotropic_element = NEW_SemiInfIsotropicElement(
        #     property_displayer = SemiInfIsotropicElement_property_displayer_fun,
        #     f_get_scene_rect = self.CVScene.get_rect_area)
        self.semi_inf_isotropic_element = NEW_SemiInfIsotropicElementSimplified(
            property_displayer=SemiInfIsotropicElement_property_displayer_fun,
            f_get_scene_rect=self.CVScene.get_rect_area)
        self.CVScene.object_keeper.add_obj(self.semi_inf_isotropic_element())  # <-wrapper about addItem()

        self.item_catalog = item_catalog
        self.logger = logger_fun

        # self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


        self.setBackgroundBrush(Qt.GlobalColor.lightGray)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setObjectName('ControlView')
        self.setScene(self.CVScene)
        # self.setRenderHint(QPainter.RenderHint.Antialiasing)
        # self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setAcceptDrops(True)
        self.dragOver = False

    def mousePressEvent(self, event):
        # self.CVScene.update()
        if event.button() == self.change_pos_mouse_button:
            self.change_pos_mouse_button_pressed = True
            self.last_mouse_pos = event.pos()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        # self.CVScene.update()
        if event.button() == self.change_pos_mouse_button:
            self.change_pos_mouse_button_pressed =False

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        # self.CVScene.drawForeground()
        # self.CVScene.drawForeground(QPainter(), self.sceneRect())
        if self.change_pos_mouse_button_pressed:
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()

            # Изменяем размер сцены на основе направления движения мыши
            new_scene_rect = self.sceneRect().translated(-delta.x(), -delta.y())
            self.setSceneRect(new_scene_rect)

        super().mouseMoveEvent(event)

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        painter.save()
        painter.setPen(self.grid_pen)
        # draw y lines
        y_pos = 0
        while y_pos>rect.top():
            painter.drawLine(QPointF(rect.left(), y_pos),
                             QPointF(rect.right(), y_pos),)
            y_pos-=self.cell_size
        y_pos = 0
        while y_pos<rect.bottom():
            painter.drawLine(QPointF(rect.left(), y_pos),
                             QPointF(rect.right(), y_pos),)
            y_pos+=self.cell_size

        # draw x lines

        x_pos = 0
        while x_pos>rect.left():
            painter.drawLine(QPointF(x_pos, rect.bottom()),
                             QPointF(x_pos, rect.top()),)
            x_pos-=self.cell_size
        x_pos = 0
        while x_pos<rect.right():
            painter.drawLine(QPointF(x_pos, rect.bottom()),
                             QPointF(x_pos, rect.top()),)
            x_pos+=self.cell_size

        # draw axis
        painter.setPen(self.axis_pen_x)
        painter.drawLine(QPointF(rect.left(), 0),QPointF(rect.right(), 0))
        painter.setPen(self.axis_pen)
        painter.drawLine(QPointF(0, rect.bottom()),QPointF(0, rect.top()))

        painter.restore()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y()>0:
            self.scale(1.1,1.1)
        else:
            self.scale(0.9,0.9)