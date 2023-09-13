from ui_v2.infrastructure.helpers import CalcParameter


def _check_value(value, field: CalcParameter):
    if value < 0:
        raise ValueError(f'Недопустимое значение {value} для свойства {field.description}')


class Jet:

    def __init__(self, length: float = 1, velocity: float = 10):
        self._length = CalcParameter(name='Длина',
                                     value=length,
                                     unit='м.',
                                     description='Длина кумулятивной струи [м.]')
        self._velocity = CalcParameter(name='Скорость',
                                       value=velocity,
                                       unit='км/с.',
                                       description='Скорость кумулятивной струи [км/с.]')

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        _check_value(value, self._length)
        self._length = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        _check_value(value, self._velocity)
        self._velocity = value

    def __str__(self):
        return f'Кумулятивная струя с параметрами:\n' \
               f'\t{self._length.name}: {self._length.value} {self._length.unit}\n' \
               f'\t{self._velocity.name}: {self._velocity.value} {self._velocity.unit}'

