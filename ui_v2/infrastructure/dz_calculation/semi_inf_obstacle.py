


"""
Полу-бесканечая преграда
"""
import math

import pandas as pd
from PyQt6.QtCore import QRectF

from ui_v2.infrastructure.helpers import some_coefficient
from ui_v2.infrastructure.scene_actors.CustomizableShell import CustomizableShell, NEW_CustomizableSell
from ui_v2.infrastructure.scene_actors.semi_inf_isotropic_element import SemiInfIsotropicElement, \
    NEW_SemiInfIsotropicElement


def calculation_semi_inf_obst(shell: CustomizableShell, obst: SemiInfIsotropicElement):
    element_count = 7  # must be more than 3
    z = shell.cumulative_lining_length / element_count
    tan_a = (shell.cumulative_lining_diameter-shell.cumulative_lining_dh)/2/shell.cumulative_lining_length
    delta = shell.cumulative_lining_wessel_thickness*shell.cumulative_lining_diameter
    hi = 1
    l0i_pr = math.atan(tan_a)*180/math.pi
    l0i = math.cos(math.radians(l0i_pr))
    A = 1.6
    B = 8
    crit_break_velocity = 2200
    explosive_charge_density_0 = 1.65
    detonation_velocity_0 = 8.1
    beta = (shell.explosive_charge_density*shell.explosive_charge_detonation_velocity**2)/(explosive_charge_density_0*detonation_velocity_0**2)
    Aw = 2.9

    calc_df_1 = pd.DataFrame({
        'section_number': [],
        'wessel_volume': [],
        'wessel_mass': [],
        'explosive_charge_volume': [],
        'explosive_charge_mass': [],
        'cumulative_lining_volume': [],
        'cumulative_lining_mass': [],
        'active_mass': [],
        'beta_i': [],
        'collapse_velocity': [],
        'jet_velocity': [],
        'jet_mass': [],
        'jet_kinetic_energy': [],
        'z0i': [],
        'delta_ti': [],
        'zi': [],
        'F': [],
    })
    section_number = 0
    for i in range(element_count):
        section_number += 1
        wessel_volume = (math.pi/4)*z*(shell.wessel_diameter**2-shell.cumulative_lining_diameter**2)
        wessel_mass = wessel_volume*shell.wessel_density/1000
        explosive_charge_volume = -math.pi/6*z**2*tan_a*(3*shell.cumulative_lining_diameter-6*shell.cumulative_lining_diameter*section_number+2*z*tan_a-6*section_number*z*tan_a+6*section_number**2*z*tan_a)
        explosive_charge_mass = (explosive_charge_volume*shell.explosive_charge_density)/1000
        cumulative_lining_volume = -math.pi*delta*z*(delta-2*shell.cumulative_lining_diameter-2*z*tan_a+4*section_number*z*tan_a)
        cumulative_lining_mass = (cumulative_lining_volume*7.9)/1000

        active_mass = (explosive_charge_mass/2)*(1+((wessel_mass-cumulative_lining_mass)/(cumulative_lining_mass+wessel_mass+explosive_charge_mass)))
        beta_i = active_mass/cumulative_lining_mass
        collapse_velocity = 0.5*hi*shell.explosive_charge_detonation_velocity*math.sqrt(beta_i/(beta_i+2))
        # jet_velocity = abs(collapse_velocity*(1/math.tan(l0i_pr/2)))
        jet_velocity = collapse_velocity*(1/math.tan(l0i_pr/2))
        jet_mass = cumulative_lining_mass*(math.sin(l0i_pr/2))**2
        jet_kinetic_energy =  (jet_mass*jet_velocity**2)/2
        z0i = shell.cumulative_lining_length-section_number*z
        delta_ti = (z0i*1e-06)/shell.explosive_charge_detonation_velocity
        zi = 100 # ???
        F = zi - z0i - l0i

        some_coef = some_coefficient(shell.cumulative_lining_material)

        tmp_df = pd.DataFrame({
            'section_number':[section_number],
            'wessel_volume':[wessel_volume],
            'wessel_mass':[wessel_mass],
            'explosive_charge_volume':[explosive_charge_volume],
            'explosive_charge_mass':[explosive_charge_mass],
            'cumulative_lining_volume':[cumulative_lining_volume],
            'cumulative_lining_mass':[cumulative_lining_mass],
            'active_mass':[active_mass],
            'beta_i':[beta_i],
            'collapse_velocity':[collapse_velocity],
            'jet_velocity':[jet_velocity],
            'jet_mass':[jet_mass],
            'jet_kinetic_energy':[jet_kinetic_energy],
            'z0i':[z0i],
            'delta_ti':[delta_ti],
            'zi':[zi],
            'F':[F],
        })
        calc_df_1 = pd.concat([calc_df_1, tmp_df], axis=0)

    calc_df_1 = calc_df_1.reset_index(drop=True)
    calc_df_2 = pd.DataFrame({
        'jet_velocity_grad':[],
        'delta_li':[],
        'li':[],
        'R_jet_0i':[],
        'n_bi':[],
        'l_mi':[],
        'csi_i':[],
        'Li':[],
        'penetration_velocity':[],
        'hole_diameter':[],
    })


    # for idx, row in calc_df_1.iterrows():
    for idx in range(len(calc_df_1.index)):
        if idx == 0:  # its 1st section
            jet_velocity_grad = 3 * calc_df_1.iloc[0]['jet_velocity'] - 3 * calc_df_1.iloc[1]['jet_velocity']+calc_df_1.iloc[2]['jet_velocity']
        elif idx == len(calc_df_1.index)-1:  # its last section
            jet_velocity_grad = 3 * calc_df_1.iloc[-1]['jet_velocity'] - 3 * calc_df_1.iloc[-2]['jet_velocity']+calc_df_1.iloc[-3]['jet_velocity']
        else:
            jet_velocity_grad = 0.5*(calc_df_1.iloc[idx-1]['jet_velocity']-calc_df_1.iloc[idx+1]['jet_velocity'])/l0i
            # jet_velocity_grad = 0.5*(calc_df_1.iloc[idx-1]['jet_velocity']-calc_df_1.iloc[idx+1]['jet_velocity'])/l0i

        delta_li = l0i * (calc_df_1.iloc[idx]['F'] / calc_df_1.iloc[idx]['jet_velocity']) * math.sqrt(jet_velocity_grad ** 2)
        li = l0i+delta_li
        # R_jet_0i = math.sqrt(calc_df_1.iloc[idx]['jet_mass']/(math.pi*l0i*some_coef)) # TODO density pf steel

        tmp = calc_df_1.iloc[idx]['jet_mass']/(math.pi*l0i*some_coef)
        if tmp<0:
            ...
        R_jet_0i = math.sqrt(tmp) # TODO density pf steel

        n_bi = A+B*R_jet_0i*math.sqrt(jet_velocity_grad**2)
        l_mi = n_bi*l0i
        csi_i = abs(calc_df_1.iloc[idx]['jet_velocity']-(crit_break_velocity*0.001))/(crit_break_velocity*0.001)
        Li = beta * csi_i * li * math.sqrt(some_coef/shell.wessel_density)  # TODO density of steel
        penetration_velocity = calc_df_1.iloc[idx]['jet_velocity']*math.sqrt(some_coef/shell.wessel_density)/(math.sqrt(some_coef/shell.wessel_density)+1)  # TODO density of steel
        hole_diameter = math.sqrt(4*calc_df_1.iloc[idx]['jet_kinetic_energy']/(Aw*math.pi*Li*0.001))

        # delta_li = l0i * (F / jet_velocity) * math.sqrt(jet_velocity_grad ** 2)
        # li = l0i + delta_li
        # R_jet_0i = math.sqrt(jet_mass / (math.pi * l0i * some_coef))  # TODO density pf steel
        # n_bi = A + B * R_jet_0i * math.sqrt(jet_velocity_grad ** 2)
        # l_mi = n_bi * l0i
        # csi_i = abs(jet_velocity - (crit_break_velocity * 0.001)) / (crit_break_velocity * 0.001)
        # Li = beta * csi_i * li * math.sqrt(some_coef / shell.wessel_density)  # TODO density of steel
        # penetration_velocity = jet_velocity * math.sqrt(some_coef / shell.wessel_density) / (
        #             math.sqrt(some_coef / shell.wessel_density) + 1)  # TODO density of steel
        # hole_diameter = math.sqrt(4 * jet_kinetic_energy / (Aw * math.pi * Li))

        tmp_df = pd.DataFrame({
            'jet_velocity_grad': [jet_velocity_grad],
            'delta_li': [delta_li],
            'li': [li],
            'R_jet_0i': [R_jet_0i],
            'n_bi': [n_bi],
            'l_mi': [l_mi],
            'csi_i': [csi_i],
            'Li': [Li],
            'penetration_velocity': [penetration_velocity],
            'hole_diameter': [hole_diameter],
        })

        calc_df_2 = pd.concat([calc_df_2, tmp_df], axis=0)

    calc_df_2 = calc_df_2.reset_index()
    calc_df = pd.concat([calc_df_1, calc_df_2], axis=1)
    calc_df=calc_df.T

    # from tabulate import tabulate
    # print(tabulate(calc_df, headers='keys', tablefmt='psql'))
    # print(1)

    return calc_df.loc['hole_diameter'][0], sum(calc_df.loc['Li'])


if __name__ == "__main__":
    depth, diameter = calculation_semi_inf_obst(NEW_CustomizableSell(lambda x: None)(),
                              NEW_SemiInfIsotropicElement(lambda x: None, lambda : QRectF(0,0,0,0)))
    print(depth, diameter)