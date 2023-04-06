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
        """Объект хранит значения входных данных
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
        :param coeff_nu: эмпирический коэффициент
        :param pl_front_thickness: толщина пластины (лицевой)
        """
        self.coeff_nu = coeff_nu
        self.pl_front_thickness = pl_front_thickness
        self.pl_back_thickness = pl_back_thickness
        self.angle = angle
        self.pl_front_density = pl_front_density
        self.pl_back_density = pl_back_density
        self.pl_lim_fluidity = pl_lim_fluidity
        self.pl_length = pl_length
        self.pl_width = pl_width
        self.explosive_layer_height = explosive_layer_height
        self.explosive_density = explosive_density
        self.detonation_velocity = detonation_velocity
        self.crit_dim_detonation = crit_dim_detonation
        self.stream_density = stream_density
        self.stream_lim_fluidity = stream_lim_fluidity
        self.stream_dim = stream_dim
        self.stream_velocity = stream_velocity
        self.polytropy_index = polytropy_index
        self.ksi_z = ksi_z
        self.ksi_r = ksi_r
        self.detonation_pressure = detonation_pressure
        self.coeff_avr_pressure = coeff_avr_pressure
        self.coeff_stream_dim_extension = coeff_stream_dim_extension




