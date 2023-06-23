import os.path

from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from ui_v2.infrastructure.SceneObjects import SceneItemWidget


class ERA_KONTAKT_1_SQ(SceneItemWidget):
    """
    Explosive reactive armor "kontakt-1" square
    """
    def __init__(self, img_dir_path: str):
        super().__init__(title='Контакт-1',
                         description = 'Комплекс динамической защиты первого поколения (4С20)',
                         img_path = os.path.join(img_dir_path, 'kontakt-1_squ.png'))


class ERA_KONTAKT_1_TR(SceneItemWidget):
    """
    Explosive reactive armor "kontakt-1" cone
    """

    def __init__(self, img_dir_path: str):
        super().__init__(title='Контакт-1',
                         description='Комплекс динамической защиты первого поколения (4С20)',
                         img_path=os.path.join(img_dir_path, 'kontakt-1_tri.png'))


class ERAE_4S20(SceneItemWidget):
    """
    Explosive reactive armor element "4С20"
    """

    def __init__(self, img_dir_path: str):
        super().__init__(title='ЭДЗ 4С20',
                         description='Элемент динамической защиты 4С20',
                         img_path=os.path.join(img_dir_path, '4s20.png'))




class RUBBER_BAR(SceneItemWidget):
    """
    just some rubber bar
    """

    def __init__(self, img_dir_path: str):
        super().__init__(title='Резина',
                         description='Случайный кусок резины ¯\_(ツ)_/¯. Тестовый item, потом удалить',
                         img_path=os.path.join(img_dir_path, 'rubber_bar.png'))


class STEEL_SHEET(SceneItemWidget):
    """
    just some steel sheet
    """

    def __init__(self, img_dir_path: str):
        super().__init__(title='Сталь',
                         description='Случайный кусок стальной пластины ¯\_(ツ)_/¯. Тестовый item, потом удалить',
                         img_path=os.path.join(img_dir_path, 'steel_sheet.png'))


def generate_catalog(img_dir_path: str) -> list[SceneItemWidget]:
    item_list = [ERA_KONTAKT_1_SQ(img_dir_path),
                 ERA_KONTAKT_1_TR(img_dir_path),
                 ERAE_4S20(img_dir_path),
                 RUBBER_BAR(img_dir_path),
                 STEEL_SHEET(img_dir_path)]
    return item_list
