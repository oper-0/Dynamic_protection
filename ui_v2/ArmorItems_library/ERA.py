import os.path
from typing import Callable

from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from ui_v2.infrastructure.SceneObjects import SceneItemWidget, SceneItemWidgetSHELL
from ui_v2.infrastructure.graphicObjects import DynamicProtectionElement, test_item, ExplosiveReactiveArmourPlate, \
    NEW_ExplosiveReactiveArmourPlate, NEW_CustomizableSell


class ERA_KONTAKT_1_SQ(SceneItemWidget):
    """
    Explosive reactive armor "kontakt-1" square
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='Контакт-1',
                         description='Комплекс динамической защиты первого поколения (4С20)',
                         img_path=os.path.join(img_dir_path, 'kontakt-1_squ.png'),
                         actor=DynamicProtectionElement())  # TODO make protocol for this


class ERA_KONTAKT_1_TR(SceneItemWidget):
    """
    Explosive reactive armor "kontakt-1" cone
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='Контакт-1 (2)',
                         description='Комплекс динамической защиты первого поколения (4С20)',
                         img_path=os.path.join(img_dir_path, 'kontakt-1_tri.png'),
                         actor=test_item())  # fixme


class ERAE_4S20(SceneItemWidget):
    """
    Explosive reactive armor element "4С20"
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='ЭДЗ 4С20',
                         description='Элемент динамической защиты 4С20',
                         img_path=os.path.join(img_dir_path, '4s20.png'),
                         actor=NEW_ExplosiveReactiveArmourPlate(property_displayer))
        # actor=ExplosiveReactiveArmourPlate)


class RUBBER_BAR(SceneItemWidget):
    """
    just some rubber bar
    """
    
    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='Резина',
                         description='Случайный кусок резины ¯\_(ツ)_/¯. Тестовый item, потом удалить',
                         img_path=os.path.join(img_dir_path, 'rubber_bar.png'))


class STEEL_SHEET(SceneItemWidget):
    """
    just some steel sheet
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='Сталь',
                         description='Случайный кусок стальной пластины ¯\_(ツ)_/¯. Тестовый item, потом удалить',
                         img_path=os.path.join(img_dir_path, 'steel_sheet.png'))


class SHELL_CUSTOMIZABLE(SceneItemWidget):
    """
    ПГ-7В
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='НАСТРАИВАЕМЫЙ',
                         description='Снаряд с случайными параметрами',
                         img_path=os.path.join(img_dir_path, 'shell_ghost.png'),
                         column_count=1,
                         actor=NEW_CustomizableSell(property_displayer))


class SHELL_PG_7V(SceneItemWidget):
    """
    ПГ-7В
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='ПГ-7В',
                         description='40-мм выстрел динамо-реактивного типа ПГ-7В с кумулятивной противотанковой гранатой ПГ-7',
                         img_path=os.path.join(img_dir_path, 'PG_7V_v3.png'),
                         column_count=1)


class SHELL_KORNET(SceneItemWidget):
    """
    ПГ-7В
    """

    def __init__(self, img_dir_path: str, property_displayer: Callable[[dict], None]):
        super().__init__(title='Корнет',
                         description='противотанковая ракета',
                         img_path=os.path.join(img_dir_path, 'kornet_ptrk.png'),
                         column_count=1)


def generate_catalog_shield(img_dir_path: str, property_displayer: Callable[[dict], None]) -> list[
    SceneItemWidget]:
    item_list = [ERA_KONTAKT_1_SQ(img_dir_path, property_displayer),
                 ERA_KONTAKT_1_TR(img_dir_path, property_displayer),
                 ERAE_4S20(img_dir_path, property_displayer),
                 RUBBER_BAR(img_dir_path, property_displayer),
                 STEEL_SHEET(img_dir_path, property_displayer)]
    return item_list


def generate_catalog_shell(img_dir_path: str, property_displayer: Callable[[dict], None]) -> list[SceneItemWidget]:
    item_list = [
        SHELL_CUSTOMIZABLE(img_dir_path, property_displayer),
        SHELL_PG_7V(img_dir_path, property_displayer),
        SHELL_KORNET(img_dir_path, property_displayer)
    ]
    return item_list
