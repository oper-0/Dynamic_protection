class InData:

    def __init__(self, coeff_nu: float = None,
                 pl_front_thickness: float = None,
                 pl_back_thickness: float = None,
                 angle: float = None,
                 pl_front_density: float = None,
                 pl_back_density: float = None,
                 pl_lim_fluidity: float = None,
                 pl_length: float = None,
                 pl_width: float = None,
                 explosive_layer_height: float = None,
                 explosive_density: float = None,
                 detonation_velocity: float = None,
                 crit_dim_detonation: float = None,
                 stream_density: float = None,
                 stream_lim_fluidity: float = None,
                 stream_dim: float = None,
                 stream_velocity: float = None,
                 polytropy_index: float = None,
                 ksi_z: float = None,
                 ksi_r: float = None,
                 detonation_pressure: float = None,
                 coeff_avr_pressure: float = None,
                 coeff_stream_dim_extension: float = None) -> None:
        """Объект хранит значения входных данных.
         Все данные передающиеся классу из формы сохраняются в системе СИ.

        :param coeff_nu:
        :param pl_front_thickness:
        :param pl_back_thickness:
        :param angle:
        :param pl_front_density:
        :param pl_back_density:
        :param pl_lim_fluidity:
        :param pl_length:
        :param pl_width:
        :param explosive_layer_height:
        :param explosive_density:
        :param detonation_velocity:
        :param crit_dim_detonation:
        :param stream_density:
        :param stream_lim_fluidity:
        :param stream_dim:
        :param stream_velocity:
        :param polytropy_index:
        :param ksi_z:
        :param ksi_r:
        :param detonation_pressure:
        :param coeff_avr_pressure:
        :param coeff_stream_dim_extension:
        """

        self.coeff_nu = coeff_nu
        if pl_front_thickness is not None:
            self.pl_front_thickness = pl_front_thickness / 1000
        if pl_back_thickness is not None:
            self.pl_back_thickness = pl_back_thickness / 1000
        self.angle = angle
        if pl_front_density is not None:
            self.pl_front_density = pl_front_density * 1000
        if pl_back_density is not None:
            self.pl_back_density = pl_back_density * 1000
        if pl_lim_fluidity is not None:
            self.pl_lim_fluidity = pl_lim_fluidity * 1e6
        if pl_length is not None:
            self.pl_length = pl_length / 1000
        if pl_width is not None:
            self.pl_width = pl_width / 1000
        if explosive_layer_height is not None:
            self.explosive_layer_height = explosive_layer_height / 1000
        if explosive_density is not None:
            self.explosive_density = explosive_density * 1000
        if detonation_velocity is not None:
            self.detonation_velocity = detonation_velocity
        if crit_dim_detonation is not None:
            self.crit_dim_detonation = crit_dim_detonation / 1000
        if stream_density is not None:
            self.stream_density = stream_density * 1000
        if stream_lim_fluidity is not None:
            self.stream_lim_fluidity = stream_lim_fluidity * 1e6
        if stream_dim is not None:
            self.stream_dim = stream_dim / 1000
        if stream_velocity is not None:
            self.stream_velocity = stream_velocity * 1000
        self.polytropy_index = polytropy_index
        self.ksi_z = ksi_z
        self.ksi_r = ksi_r
        if detonation_pressure is not None:
            self.detonation_pressure = detonation_pressure * 1e6
        self.coeff_avr_pressure = coeff_avr_pressure
        self.coeff_stream_dim_extension = coeff_stream_dim_extension


class DPPlate:
    def __init__(self, asymmetric_speed: dict = None,
                 acceleration_time: float = None,
                 rotation_angle: float = None) -> None:
        """Объект хранит расчетные параметры пластины динамической защиты.
        :param asymmetric_speed: Скорости метания лицевой и тыльной пластин
            (несимметричное метание) [м/с].
        :param acceleration_time: Время разгона пластины до максимальной
            скорости [мкс].
        :param rotation_angle: Угол поворота пластины [градус].
        """
        self.asymmetric_speed = asymmetric_speed
        self.acceleration_time = acceleration_time
        self.rotation_angle = rotation_angle
