from typing import Callable


class path_keeper(object):
    """
    класс, хранящий все пути, необходимые UI
    """
    abs_root_dir : str = ''  # абсолютный путь до директории приложения
    abs_icons_dir : str = ''  # абсолютный путь до директории с иконками
    abs_img_dir: str = ''  # абсолютный путь до директории с изображениями

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(path_keeper, cls).__new__(cls)
        return cls.instance


class INTERACTOR(object):
    """
    Singleton класс, содержащий необходимую информацию для использования программой
    """
    paths: path_keeper = None
    UsersLogger: Callable[[str, str], None]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(INTERACTOR, cls).__new__(cls)
        return cls.instance