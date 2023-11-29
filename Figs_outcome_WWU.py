# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:42:22 2021

    InnoBRI Emergency Department Simulation Platform
    Functions figures

@author: Gustavo Hernandez Mejia
"""

# import random
import matplotlib.pyplot as plt
# import math  
# import time
import numpy as np
import pandas as pd
# import csv
# import statistics
# import scipy.stats
import seaborn as sns

# import numpy as np


Base_case_TOT = pd.read_excel('15_Fom_Base/Base_Total.xlsx', index_col=0)
Base_case_Pat = pd.read_excel('15_Fom_Base/Base_Total_Pat.xlsx', index_col=0)
Base_case_HCW = pd.read_excel('15_Fom_Base/Base_Total_HCW.xlsx', index_col=0)
Base_case_WHO = pd.read_excel('15_Fom_Base/Base_from_whom.xlsx', index_col=0)
Base_case_FOM = pd.read_excel('15_Fom_Base/Base_fomite.xlsx', index_col=0)

# Base_case_TOT = pd.read_excel('10_TESTS\Base_Total.xlsx', index_col=0)
# Base_case_Pat = pd.read_excel('10_TESTS\Base_Total_Pat.xlsx', index_col=0)
# Base_case_HCW = pd.read_excel('10_TESTS\Base_Total_HCW.xlsx', index_col=0)
# Base_case_WHO = pd.read_excel('10_TESTS\Base_from_whom.xlsx', index_col=0)

Curtains_TOT = pd.read_excel('16_Fom_FP\Base_Total.xlsx', index_col=0)
Curtains_Pat = pd.read_excel('16_Fom_FP\Base_Total_Pat.xlsx', index_col=0)
Curtains_HCW = pd.read_excel('16_Fom_FP\Base_Total_HCW.xlsx', index_col=0)
Curtains_WHO = pd.read_excel('16_Fom_FP\Base_from_whom.xlsx', index_col=0)
Curtains_FOM = pd.read_excel('16_Fom_FP/Base_fomite.xlsx', index_col=0)

FFP_TOT = pd.read_excel('17_Fom_HS_2\Base_Total.xlsx', index_col=0)
FFP_Pat = pd.read_excel('17_Fom_HS_2\Base_Total_Pat.xlsx', index_col=0)
FFP_HCW = pd.read_excel('17_Fom_HS_2\Base_Total_HCW.xlsx', index_col=0)
FFP_WHO = pd.read_excel('17_Fom_HS_2\Base_from_whom.xlsx', index_col=0)
FFP_FOM = pd.read_excel('17_Fom_HS_2\Base_fomite.xlsx', index_col=0)

NB_max_TOT = pd.read_excel('18_Fom_AS\Base_Total.xlsx', index_col=0)
NB_max_Pat = pd.read_excel('18_Fom_AS\Base_Total_Pat.xlsx', index_col=0)
NB_max_HCW = pd.read_excel('18_Fom_AS\Base_Total_HCW.xlsx', index_col=0)
NB_max_WHO = pd.read_excel('18_Fom_AS\Base_from_whom.xlsx', index_col=0)
NB_max_FOM = pd.read_excel('18_Fom_AS\Base_fomite.xlsx', index_col=0)



        # Base_TOT, 
        # Curt_TOT,
        # N_VC_TOT,  N_VC_TOT = FFP_TOT          HS
        # NB_TOT,    NB_TOT = NB_max_TOT         AS
        # NB_sppit, 
        # NB_vol,
        # scre_TOT,  scre_TOT = screenin_TOT     HS_AS
        # A_NB_TOT

# Ventilat_TOT = pd.read_excel('3_VENTILATION\Base_Total.xlsx', index_col=0)
# Ventilat_Pat = pd.read_excel('3_VENTILATION\Base_Total_Pat.xlsx', index_col=0)
# Ventilat_HCW = pd.read_excel('3_VENTILATION\Base_Total_HCW.xlsx', index_col=0)
# Ventilat_WHO = pd.read_excel('3_VENTILATION\Base_from_whom.xlsx', index_col=0)

# Vet_Curt_TOT = pd.read_excel('4_CURT_VENTIL\Base_Total.xlsx', index_col=0)
# Vet_Curt_Pat = pd.read_excel('4_CURT_VENTIL\Base_Total_Pat.xlsx', index_col=0)
# Vet_Curt_HCW = pd.read_excel('4_CURT_VENTIL\Base_Total_HCW.xlsx', index_col=0)
# Vet_Curt_WHO = pd.read_excel('4_CURT_VENTIL\Base_from_whom.xlsx', index_col=0)




screenin_TOT = pd.read_excel('19_Fom_HS_AS\Base_Total.xlsx', index_col=0)
screenin_Pat = pd.read_excel('19_Fom_HS_AS\Base_Total_Pat.xlsx', index_col=0)
screenin_HCW = pd.read_excel('19_Fom_HS_AS\Base_Total_HCW.xlsx', index_col=0)
screenin_WHO = pd.read_excel('19_Fom_HS_AS\Base_from_whom.xlsx', index_col=0)
screenin_FOM = pd.read_excel('19_Fom_HS_AS\Base_fomite.xlsx', index_col=0)


NB_sppit_TOT = pd.read_excel('20_Fom_EBS_2\Base_Total.xlsx', index_col=0)
NB_sppit_Pat = pd.read_excel('20_Fom_EBS_2\Base_Total_Pat.xlsx', index_col=0)
NB_sppit_HCW = pd.read_excel('20_Fom_EBS_2\Base_Total_HCW.xlsx', index_col=0)
NB_sppit_WHO = pd.read_excel('20_Fom_EBS_2\Base_from_whom.xlsx', index_col=0)
NB_sppit_FOM = pd.read_excel('20_Fom_EBS_2\Base_fomite.xlsx', index_col=0)


NB_volm_TOT = pd.read_excel('21_Fom_EBE\Base_Total.xlsx', index_col=0)
NB_volm_Pat = pd.read_excel('21_Fom_EBE\Base_Total_Pat.xlsx', index_col=0)
NB_volm_HCW = pd.read_excel('21_Fom_EBE\Base_Total_HCW.xlsx', index_col=0)
NB_volm_WHO = pd.read_excel('21_Fom_EBE\Base_from_whom.xlsx', index_col=0)
NB_volm_FOM = pd.read_excel('21_Fom_EBE\Base_fomite.xlsx', index_col=0)

# screenin_TOT = pd.read_excel('10_AS_Vent\Base_Total.xlsx', index_col=0)
# screenin_Pat = pd.read_excel('10_AS_Vent\Base_Total_Pat.xlsx', index_col=0)
# screenin_HCW = pd.read_excel('10_AS_Vent\Base_Total_HCW.xlsx', index_col=0)
# screenin_WHO = pd.read_excel('10_AS_Vent\Base_from_whom.xlsx', index_col=0)


#                    INTERVENTIONS   COMBINED

# AS_Vent_TOT = pd.read_excel('10_AS_Vent\Base_Total.xlsx', index_col=0)
# AS_Vent_Pat = pd.read_excel('10_AS_Vent\Base_Total_Pat.xlsx', index_col=0)
# AS_Vent_HCW = pd.read_excel('10_AS_Vent\Base_Total_HCW.xlsx', index_col=0)
# AS_Vent_WHO = pd.read_excel('10_AS_Vent\Base_from_whom.xlsx', index_col=0)

# NBV_Vent_TOT = pd.read_excel('11_NBV_Vent\Base_Total.xlsx', index_col=0)
# NBV_Vent_Pat = pd.read_excel('11_NBV_Vent\Base_Total_Pat.xlsx', index_col=0)
# NBV_Vent_HCW = pd.read_excel('11_NBV_Vent\Base_Total_HCW.xlsx', index_col=0)
# NBV_Vent_WHO = pd.read_excel('11_NBV_Vent\Base_from_whom.xlsx', index_col=0)

AS_NBV_Vent_TOT = pd.read_excel('22_Fom_AS_EBE\Base_Total.xlsx', index_col=0) # was 12_AS_NBV_Vent
AS_NBV_Vent_Pat = pd.read_excel('22_Fom_AS_EBE\Base_Total_Pat.xlsx', index_col=0)
AS_NBV_Vent_HCW = pd.read_excel('22_Fom_AS_EBE\Base_Total_HCW.xlsx', index_col=0)
AS_NBV_Vent_WHO = pd.read_excel('22_Fom_AS_EBE\Base_from_whom.xlsx', index_col=0)
AS_NBV_Vent_FOM = pd.read_excel('22_Fom_AS_EBE\Base_fomite.xlsx', index_col=0)



Base_TOT = Base_case_TOT['Total_inf']
# F_co_TOT = Far_cont_TOT['Total_inf']
Curt_TOT = Curtains_TOT['Total_inf']
# Vent_TOT = Ventilat_TOT['Total_inf']
# V_Cu_TOT = Vet_Curt_TOT['Total_inf']
NB_TOT = NB_max_TOT['Total_inf']                  
N_VC_TOT = FFP_TOT['Total_inf']                  
scre_TOT = screenin_TOT['Total_inf']              
NB_sppit = NB_sppit_TOT['Total_inf']              
NB_vol = NB_volm_TOT['Total_inf']                 
# AS_TOT = AS_Vent_TOT['Total_inf']
# NBV_TOT = NBV_Vent_TOT['Total_inf']
A_NB_TOT = AS_NBV_Vent_TOT['Total_inf']            #  AS_EBE

Base_TOT_P = Base_case_Pat['Total_inf_P']
# # F_co_TOT_P = Far_cont_Pat['Total_inf_P']
Curt_TOT_P = Curtains_Pat['Total_inf_P']
# Vent_TOT_P = Ventilat_Pat['Total_inf_P']
# V_Cu_TOT_P = Vet_Curt_Pat['Total_inf_P']
N_VC_TOT_P = FFP_Pat['Total_inf_P']
scre_TOT_P = screenin_Pat['Total_inf_P']
NB_TOT_P = NB_max_Pat['Total_inf_P']
NB_sppit_P = NB_sppit_Pat['Total_inf_P']
NB_volum_P = NB_volm_Pat['Total_inf_P']
# AS_TOT_P = AS_Vent_Pat['Total_inf_P']
# NBV_TOT_P = NBV_Vent_Pat['Total_inf_P']
A_NB_TOT_P = AS_NBV_Vent_Pat['Total_inf_P']


Base_TOT_H = Base_case_HCW['Total_inf_H']
# # F_co_TOT_H = Far_cont_HCW['Total_inf_H']
Curt_TOT_H = Curtains_HCW['Total_inf_H']
# Vent_TOT_H = Ventilat_HCW['Total_inf_H']
# V_Cu_TOT_H = Vet_Curt_HCW['Total_inf_H']
N_VC_TOT_H = FFP_HCW['Total_inf_H']
scre_TOT_H = screenin_HCW['Total_inf_H']
NB_TOT_H = NB_max_HCW['Total_inf_H']
NB_sppit_H = NB_sppit_HCW['Total_inf_H']
NB_volum_H = NB_volm_HCW['Total_inf_H']
# AS_TOT_H = AS_Vent_HCW['Total_inf_H']
# NBV_TOT_H = NBV_Vent_HCW['Total_inf_H']
A_NB_TOT_H = AS_NBV_Vent_HCW['Total_inf_H']


Base_FOM = Base_case_FOM['Total_fomites']
Curt_FOM = Curtains_FOM['Total_fomites']
NB_FOM = NB_max_FOM['Total_fomites']                  
N_VC_FOM = FFP_FOM['Total_fomites']                  
scre_FOM = screenin_FOM['Total_fomites']              
NB_s_FOM = NB_sppit_FOM['Total_fomites']              
NB_v_FOM = NB_volm_FOM['Total_fomites']                 
A_NB_FOM = AS_NBV_Vent_FOM['Total_fomites']   


palettes = iter(sns.husl_palette(9))

lette = 22
labels = 16
mark_s = "6"
# cols = sns.color_palette("Set2")
# # cols = sns.color_palette("Set2",8)
# cols.append((0.5, 0.6 , 0.55))
# cols.append((0.9, 0.6 , 0.65))
# cols.append((0.5, 0.9 , 0.55))
# cols.append((0.5, 0.8 , 0.9))

cols = sns.color_palette("Set2",8)
# cols = sns.color_palette("Set2",8)
# cols.append((0.5, 0.6 , 0.55))
# cols.append((0.9, 0.6 , 0.65))
# cols.append((0.5, 0.9 , 0.55))
# cols.append((0.5, 0.8 , 0.9))


names = ['Base\n Case', 
          'Curt', 
          'Vent', 
          'WS',
          'AS',
          'NBS',
          'NBA',
          'Curt +\nVent', 
          'WS + AS', 
          'AS +\nVent',
          'NBA +\nVent',
          'AS + NBA\n+ Vent']

names = ['Base\n Case', 
          'FP', 
          'HS',
          'AS',
          'EBS',
          'EBE', 
          'HS + AS',
          'AS + EBE', 
          # 'Curt +\nVent', 
          # 'AS +\nVent',
          # 'NBA +\nVent',
          # 'AS + NBA\n+ Vent'
          ]
# names = ['Base\n Case', 'Waiting N-Urg\nDivision (WD)', 
#           'Attention N-Urg\nDivision (AD)', 'WD + AD']
f, ax3 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
# ax3.set_yscale("log")
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total of newly infected (pat + HCW)', fontsize = labels +1)
plt.rc('ytick', labelsize = 17) 

sns.boxplot(data=[

        
        Base_TOT,       
        Curt_TOT,
        N_VC_TOT,    # HS
        NB_TOT,      # AS
        NB_sppit, 
        NB_vol,
        scre_TOT,    # HS + AS
        A_NB_TOT
        
        
        ], 
        palette = cols,
        # palette="Set3",
        # Vent_TOT, V_Cu_TOT], palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})   
# plt.xticks(np.arange(12), names, rotation = 35) 
plt.xticks(np.arange(8), names) 
plt.ylim(top=30) 
# plt.title('Total of newly infected', fontsize = lette)
# plt.savefig('24_Fom_figs/totals.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/totals.svg', format='svg', dpi=1400)

#----------------------------------------------------------------




names2 = ['Base Case', 
          'Curtains (Curt)', 
          'Ventilation (Vent)', 
          'Waiting Sep. (WS)',
          'Attention Sep. (AS)',
          'Nursing Base Sep. (NBS)',
          'Nursing Base Area (NBA)',
          'Curt + Vent', 
          'WS + AS', 
          'AS + Vent',
          'NBA + Vent',
          'AS + NBA + Vent']

# cols = sns.color_palette("Set2",14)
f, ax7 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total of newly infected patients', fontsize = labels +1)
plt.rc('ytick', labelsize = 17) 
# ax7.set_yscale("log") 
# sns.boxplot(data=[Base_TOT_P, Curt_TOT_P, Vent_TOT_P,
#     # V_Cu_TOT_P,NB_TOT_P,N_VC_TOT_P,scre_TOT_P], palette = cols,
#     V_Cu_TOT_P,NB_TOT_P, N_VC_TOT_P], palette = cols,
sns.boxplot(data=[
                # Base_TOT_P, 
                # Curt_TOT_P, 
                # N_VC_TOT_P, 
                # NB_TOT_P, 
                # NB_sppit_P,
                # NB_volum_P,
                # Vent_TOT_P,
                # scre_TOT_P,
                # V_Cu_TOT_P, 
                # AS_TOT_P, 
                # NBV_TOT_P, 
                # A_NB_TOT_P
                Base_TOT_P, 
                Curt_TOT_P, 
                N_VC_TOT_P, 
                NB_TOT_P, 
                NB_sppit_P,
                NB_volum_P,
                scre_TOT_P,
                A_NB_TOT_P
                ], 

    # palette = "Set3",
    # V_Cu_TOT_P], 
    palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})  
plt.xticks(np.arange(8), names) 
# plt.legend(names2, fontsize = 15)
plt.ylim(top = 15)  
# plt.title('Total of newly infected patients', fontsize = lette)
# plt.savefig('24_Fom_figs/totals_pat.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/totals_Pat.svg', format='svg', dpi=1400)


# # violinplot
# cols = sns.color_palette("Set2",14)
f, ax8 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total of newly infected HCWs', fontsize = labels +1)
plt.rc('ytick', labelsize = 17) 

sns.boxplot(data=[

    
    Base_TOT_H, 
    Curt_TOT_H, 
    N_VC_TOT_H, 
    NB_TOT_H, 
    NB_sppit_H,
    NB_volum_H,
    scre_TOT_H, 
    A_NB_TOT_H
    ],     
    # palette = "Set3",
    # V_Cu_TOT_H], 
    palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})  
plt.xticks(np.arange(8), names) 
plt.ylim(top=15) 
# plt.title('Total of newly infected HCW', fontsize = lette)
# plt.savefig('24_Fom_figs/totals_hcw.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/totals_HCW.svg', format='svg', dpi=1400)




#                           Areas


TOT_BC = Base_case_TOT['Base1'] + Base_case_TOT['Base2'] + Base_case_TOT['Base3']
TO_Cur = Curtains_TOT['Base1'] + Curtains_TOT['Base2'] + Curtains_TOT['Base3']
# TO_Ven = Ventilat_TOT['Base1'] + Ventilat_TOT['Base2'] + Ventilat_TOT['Base3']
# TO_V_C = Vet_Curt_TOT['Base1'] + Vet_Curt_TOT['Base2'] + Vet_Curt_TOT['Base3']
TON_VC = FFP_TOT['Base1'] + FFP_TOT['Base2'] + FFP_TOT['Base3']
TO_scr = screenin_TOT['Base1'] + screenin_TOT['Base2'] + screenin_TOT['Base3'] 
TO_NB = NB_max_TOT['Base1'] + NB_max_TOT['Base2'] + NB_max_TOT['Base3']
TO_NBS = NB_sppit_TOT['Base1'] + NB_sppit_TOT['Base2'] + NB_sppit_TOT['Base3']
TO_NBV = NB_volm_TOT['Base1'] + NB_volm_TOT['Base2'] + NB_volm_TOT['Base3'] 
# TO_ASV = AS_Vent_TOT['Base1'] + AS_Vent_TOT['Base2'] + AS_Vent_TOT['Base3']
# TO_NVV = NBV_Vent_TOT['Base1'] + NBV_Vent_TOT['Base2'] + NBV_Vent_TOT['Base3']
TO_NBV = AS_NBV_Vent_TOT['Base1'] + AS_NBV_Vent_TOT['Base2'] + AS_NBV_Vent_TOT['Base3']



# TOT_BC, TO_Cur, TO_Ven, TO_V_C, TO_NCM, TO_ROM


HCW_BC = Base_case_HCW['Base1'] + Base_case_HCW['Base2'] + Base_case_HCW['Base3']
HW_Cur = Curtains_HCW['Base1'] + Curtains_HCW['Base2'] + Curtains_HCW['Base3']
# HW_Ven = Ventilat_HCW['Base1'] + Ventilat_HCW['Base2'] + Ventilat_HCW['Base3']
# HW_V_C = Vet_Curt_HCW['Base1'] + Vet_Curt_HCW['Base2'] + Vet_Curt_HCW['Base3']
HW_ROM = FFP_HCW['Base1'] + FFP_HCW['Base2'] + FFP_HCW['Base3']
HW_ALL = screenin_HCW['Base1'] + screenin_HCW['Base2'] + screenin_HCW['Base3']
HW_NCM = NB_max_HCW['Base1'] + NB_max_HCW['Base2'] + NB_max_HCW['Base3']
HW_NBS = NB_sppit_HCW['Base1'] + NB_sppit_HCW['Base2'] + NB_sppit_HCW['Base3']
HW_NBV = NB_volm_HCW['Base1'] + NB_volm_HCW['Base2'] + NB_volm_HCW['Base3']
# HW_ASV = AS_Vent_HCW['Base1'] + AS_Vent_HCW['Base2'] + AS_Vent_HCW['Base3']
# HW_NVV = NBV_Vent_HCW['Base1'] + NBV_Vent_HCW['Base2'] + NBV_Vent_HCW['Base3']
HW_ABV = AS_NBV_Vent_HCW['Base1'] + AS_NBV_Vent_HCW['Base2'] + AS_NBV_Vent_HCW['Base3'] 




# HCW_BC, HW_Cur, HW_Ven, HW_V_C, HW_ROM, HW_ALL, HW_NCM, HW_NBS, HW_NBV

# cols = sns.color_palette("Set2",9)
# names2 = ['Base Case', 'Curtains', 
#           'Ventilation', 'Curt + Ventil', 'HCW Base', 
#           'Screening']
names2 = ['Base Case', 'Curtains', 
          'Ventilation', 'Curt + Ventil', 'HCW Base']
names2 = ['Base\n Case', 'Waiting N-Urg\nDivision (WD)', 
          'Attention N-Urg\nDivision (AD)', 'WD + AD']
names2 = ['Base Case', 'Curtains (Curt)', 
          'Ventilation (Ven)', 'Curt + Ven', 'Waiting Split (WS)',
  'Attention Split (AS)', 'WS + AS', 'NB Split'
          , 'NB Vol']
names2 = ['Base Case', 'Curtains (Curt)', 
          'Ventilation (Vent)', 'Curt + Vent', 'Wait Sep.(WS) + Vent',
  'Atte. Sep.(AS) + Vent', 'WS + AS + Vent', 'NB Sep. + AS + Vent'
          , 'NB Vol + AS + Vent']

names2 = ['Base Case', 'Curtains (Curt)', 
          'Ventilation (Vent)', 'Curt + Vent', 
          'Wait. N. U. Sep. (WS)',
  'Atte. N. U. Sep. (AS)', 'WS + AS', 
  'Nurse Base Sep. (NBS)'
          , 'Nurse Base Vol. (NBV)']
names2 = ['Base Case', 'Curtains (Curt)', 
          'Ventilation (Vent)', 'Curt + Vent', 
          'Wait. N. U. Sep. (WS)',
  'Atte. N. U. Sep. (AS)', 'WS + AS', 
  'Nurse Base Sep. (NBS)'
          , 'Nurse Base Vol. (NBV)',
          'AS + Vent',
          'NBV + Vent',
          'AS + NBV + Vent']

areas = ['Reception', 'Triage', 'Waiting\nUrgent', 
          'Waiting\nNon-urgt', 'Attention\nUrgent', 
          'Attention\nNon-urgt', 'Imaging',
          'Laboratory', 'Nurse\nBase']
areas = ['Reception', 
         'Holding Area', 
          'Attention\nUrgent', 
          'Attention\nNon-urgt',
          'Imaging',
          'Laboratory', 
          'ED\nBase']
# plase = [3, 10, 17, 24, 31, 38, 45, 52, 59, 66, 73, 80]
# plase = [2.5, 5, 7.5, 10, 12.5, 
#          15, 17.5, 20, 22.5, 25, 27.5, 30]
plase = [3,6,9,12,15,18,21,24,27,30,33,36]
plase = [2.5, 8.5, 14.5, 17, 22, 27, 32, 37, 42, 47, 52]
# plase = np.arange(2.5, 65, 6)
plase = [2.5,  8.5, 14.5, 20.5, 26.5, 32.5, 38.5, 
         44.5, 50.5, 56.5, 62.5]
plase = [2.5,  8.5, 14.5, 20.5, 26.5, 32.5, 38.5, 
         44.5]
plase = [1.5,  5.5, 9.5, 13.5, 17.5, 21.5, 25.5, 
         29.5]
plase = [4,  13, 22, 31, 40, 49, 58, 
         67, 76]
plase = [5.5,  17.5, 29.5, 41.5, 53.5, 65.5, 77.5, 
         89.5, 101.5]
plase = [5.5,  17.5, 29.5, 41.5, 53.5, 65.5, 77.5]

plase = [3.5, 11.5, 19.5, 27.5, 35.5, 43.5, 51.5]

# plase = [3, 7, 11, 15, 19, 23, 45, 52, 59, 66, 73, 80]
f, ax4 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
# ax4.set_yscale("symlog") 
sns.boxplot(data=[
    
    
    Base_case_TOT['Recep'], 
    Curtains_TOT['Recep'], 
    FFP_TOT['Recep'],  
    NB_max_TOT['Recep'],
    NB_sppit_TOT['Recep'],
    NB_volm_TOT['Recep'],
    screenin_TOT['Recep'], 
    AS_NBV_Vent_TOT['Recep'],
                  
                  
    Base_case_TOT['WaitN'], 
    Curtains_TOT['WaitN'],
    FFP_TOT['WaitN'], 
    NB_max_TOT['WaitN'],
    NB_sppit_TOT['WaitN'],
    NB_volm_TOT['WaitN'],
    # Ventilat_TOT['WaitN'],  
    screenin_TOT['WaitN'], 
    # Vet_Curt_TOT['WaitN'], 
    # AS_Vent_TOT['WaitN'],
    # NBV_Vent_TOT['WaitN'],
    AS_NBV_Vent_TOT['WaitN'],
                  
    Base_case_TOT['AtteU'], 
    Curtains_TOT['AtteU'],
    FFP_TOT['AtteU'], 
    NB_max_TOT['AtteU'],
    NB_sppit_TOT['AtteU'],
    NB_volm_TOT['AtteU'],
    # Ventilat_TOT['AtteU'],  
    screenin_TOT['AtteU'], 
    # Vet_Curt_TOT['AtteU'], 
    # AS_Vent_TOT['AtteU'],
    # NBV_Vent_TOT['AtteU'],
    AS_NBV_Vent_TOT['AtteU'],

                   
    Base_case_TOT['AtteN'], 
    Curtains_TOT['AtteN'],
    FFP_TOT['AtteN'], 
    NB_max_TOT['AtteN'],
    NB_sppit_TOT['AtteN'],
    NB_volm_TOT['AtteN'],
    # Ventilat_TOT['AtteN'],  
    screenin_TOT['AtteN'],
    # Vet_Curt_TOT['AtteN'], 
    # AS_Vent_TOT['AtteN'],
    # NBV_Vent_TOT['AtteN'],
    AS_NBV_Vent_TOT['AtteN'],
                  
    
    Base_case_TOT['Imagi'], 
    Curtains_TOT['Imagi'],
    FFP_TOT['Imagi'],
    NB_max_TOT['Imagi'],
    NB_sppit_TOT['Imagi'],
    NB_volm_TOT['Imagi'],
    # Ventilat_TOT['Imagi'],  
    screenin_TOT['Imagi'], 
    # Vet_Curt_TOT['Imagi'], 
    # AS_Vent_TOT['Imagi'],
    # NBV_Vent_TOT['Imagi'],
    AS_NBV_Vent_TOT['Imagi'],
                  
    Base_case_TOT['Labot'], 
    Curtains_TOT['Labot'],
    FFP_TOT['Labot'], 
    NB_max_TOT['Labot'],
    NB_sppit_TOT['Labot'],
    NB_volm_TOT['Labot'],
    # Ventilat_TOT['Labot'],  
    screenin_TOT['Labot'], 
    # Vet_Curt_TOT['Labot'], 
    # AS_Vent_TOT['Labot'],
    # NBV_Vent_TOT['Labot'],
    AS_NBV_Vent_TOT['Labot'],
    
    
    HCW_BC, 
    HW_Cur, 
    HW_ROM,  
    HW_NCM, 
    HW_NBS, 
    HW_NBV,
    # HW_Ven, 
    HW_ALL,
    # HW_V_C, 
    # HW_ASV, HW_NVV,
    HW_ABV,

                  ], 
    palette = cols,
    # palette="Set3", 
    showfliers = False,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas, fontsize=16) 
plt.ylabel('Total of newly infected \nper area (pat + HCWs)', fontsize = labels +2)
# plt.legend(names2, fontsize = 14)
# plt.ylim(top=30) 
plt.ylim(top=15) 
# plt.title('Total of newly infected per ED area', fontsize = 22)
# plt.savefig('24_Fom_figs/Areas_total.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/areas_totals.svg', format='svg', dpi=1400)


#------------------------------------------------------------



# cols = sns.color_palette("Set2",9)
areas = ['Reception', 'Triage', 'Waiting\nUrgent', 
          'Waiting\nNon-urgent', 'Attention\nUrgent', 
          'Attention\nNon-urgent', 'Imaging', 'Laboratory', 
          'HCW\nBase 1', 'HCW\nBase 2', 'HCW\nBase 3']
areas = ['Reception', 'Triage', 'Waiting\nUrgent', 
          'Waiting\nNon-urgent', 'Attention\nUrgent', 
          'Attention\nNon-urgent', 'Imaging', 'Laboratory']
areas = ['Waiting\nUrgent', 
          'Waiting\nNon-urgent', 'Attention\nUrgent', 
          'Attention\nNon-urgent']#
areas = ['Holding Area', 'Attention\nUrgent', 
          'Attention\nNon-urgent']
areas = ['Reception',
         'Holding Area', 
         'Attention\nUrgent', 
         'Attention\nNon-urgent']
names2 = ['Base Case', 
          'Curtains (Curt)', 
          'Ventilation (Vent)', 
          'Waiting Sep. (WS)',
          'Attention Sep. (AS)',
          'Nursing Base Sep. (NBS)',
          'Nursing Base Area (NBA)',
          'Curt + Vent', 
          'WS + AS', 
          'AS + Vent',
          'NBA + Vent',
          'AS + NBA + Vent']
names2 = ['Base Case', 
          'Curtains (Curt)', 
          'Attention Sep. (AS)',
          'Waiting Sep. (WS)',
          'Nursing Base Sep. (NBS)',
          'Nursing Base Area (NBA)',
          'Ventilation (Vent)', 
          'WS + AS', 
          'Curt + Vent', 
          'AS + Vent',
          'NBA + Vent',
          'AS + NBA + Vent']
plase = [3, 10, 17, 24, 31, 38, 45, 52]
plase = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52]
plase = [2, 7, 12, 17, 22, 27, 32, 37]
plase = [2.5,  8.5, 14.5, 20.5, 26.5, 32.5, 38.5, 
         44.5]
plase = [1.5,  5.5, 9.5, 13.5, 17.5, 21.5, 25.5, 
         29.5]
plase = [4,  13, 22, 31, 40, 49, 58, 
         67]
plase = [5.5,  17.5, 29.5, 41.5, 53.5, 65.5, 77.5, 
         89.5]
plase = [5.5,  17.5, 29.5, 41.5]
plase = [3.5, 11.5, 19.5, 27.5]
f, ax3 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
# plt.title('Total of newly infected patients per area', fontsize = 22)
# ax3.set_yscale("symlog") 
sns.boxplot(data=[

     
     Base_case_Pat['Recep_P'], 
     Curtains_Pat['Recep_P'],
     FFP_Pat['Recep_P'],
     NB_max_Pat['Recep_P'],
     NB_sppit_Pat['Recep_P'],
     NB_volm_Pat['Recep_P'],  
     screenin_Pat['Recep_P'],
     AS_NBV_Vent_Pat['Recep_P'],
    
                  
                  
    Base_case_Pat['WaitN_P'], 
    Curtains_Pat['WaitN_P'],
    FFP_Pat['WaitN_P'],
    NB_max_Pat['WaitN_P'],
    NB_sppit_Pat['WaitN_P'],
    NB_volm_Pat['WaitN_P'],
    # Ventilat_Pat['WaitN_P'],  
    screenin_Pat['WaitN_P'],
    # Vet_Curt_Pat['WaitN_P'],
    # AS_Vent_Pat['WaitN_P'],
    # NBV_Vent_Pat['WaitN_P'],
    AS_NBV_Vent_Pat['WaitN_P'],
                  
    Base_case_Pat['AtteU_P'], 
    Curtains_Pat['AtteU_P'],
    FFP_Pat['AtteU_P'], 
    NB_max_Pat['AtteU_P'],
    NB_sppit_Pat['AtteU_P'],
    NB_volm_Pat['AtteU_P'],
    # Ventilat_Pat['AtteU_P'],
    screenin_Pat['AtteU_P'],
    # Vet_Curt_Pat['AtteU_P'], 
    # AS_Vent_Pat['AtteU_P'],
    # NBV_Vent_Pat['AtteU_P'],
    AS_NBV_Vent_Pat['AtteU_P'],
                   
    Base_case_Pat['AtteN_P'], 
    Curtains_Pat['AtteN_P'],
    FFP_Pat['AtteN_P'],  
    NB_max_Pat['AtteN_P'], 
    NB_sppit_Pat['AtteN_P'],
    NB_volm_Pat['AtteN_P'],
    # Ventilat_Pat['AtteN_P'],  
    screenin_Pat['AtteN_P'],
    # Vet_Curt_Pat['AtteN_P'], 
    # AS_Vent_Pat['AtteN_P'],
    # NBV_Vent_Pat['AtteN_P'],
    AS_NBV_Vent_Pat['AtteN_P'],
                  

                  ], 
    palette = cols ,
      showmeans = True, 
      showfliers = False,
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas, fontsize = 16)
plt.ylabel('Total of newly infected patients \nper area', fontsize = labels +2)
# plt.legend(names2, fontsize = 16)
# plt.ylim(top=30) 
plt.ylim(top = 12)
# plt.savefig('24_Fom_figs/Areas_pat.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/areas_total_pat.svg', format='svg', dpi=1400)

 

areas2 = ['Reception', 'Triage', 'Attention\nUrgent', 
          'Attention\nNon-urgent', 'Imaging', 'Laboratory', 
          'Nurse\nBase']
areas2 = ['Attention\nUrgent', 
          'Attention\nNon-urgent', 'Imaging', 'Laboratory', 
          'Nurse\nBase']
plase = [3, 10, 17, 24, 31, 38, 45, 52, 59]
plase = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52]
plase = [2, 7, 12, 17, 22, 27, 32, 37, 42]
plase = [2.5,  8.5, 14.5, 20.5, 26.5, 32.5, 38.5, 
         44.5, 50.5]
plase = [2.5,  8.5, 14.5, 20.5, 26.5, 32.5, 38.5]
plase = [1.5,  5.5, 9.5, 13.5, 17.5, 21.5, 25.5]
plase = [4,  13, 22, 31, 40, 49, 58]
plase = [5.5,  17.5, 29.5, 41.5, 53.5, 65.5, 77.5]
plase = [5.5,  17.5, 29.5, 41.5, 53.5]
plase = [5.5,  17.5, 29.5, 41.5, 53.5]
plase = [3.5, 11.5, 19.5, 27.5, 35.5]
f, ax5 = plt.subplots(figsize=(19,6), facecolor='w', edgecolor='k')
# plt.title('Total of newly infected HCWs per area', fontsize = 22)
# ax5.set_yscale("symlog") 
sns.boxplot(data=[
                  
    Base_case_HCW['AtteU_H'], 
    Curtains_HCW['AtteU_H'],
    FFP_HCW['AtteU_H'], 
    NB_max_HCW['AtteU_H'], 
    NB_sppit_HCW['AtteU_H'],
    NB_volm_HCW['AtteU_H'],
    # Ventilat_HCW['AtteU_H'],  
    screenin_HCW['AtteU_H'],
    # Vet_Curt_HCW['AtteU_H'],  
    # AS_Vent_HCW['AtteU_H'],
    # NBV_Vent_HCW['AtteU_H'],
    AS_NBV_Vent_HCW['AtteU_H'],
                   
    Base_case_HCW['AtteN_H'], 
    Curtains_HCW['AtteN_H'],
    FFP_HCW['AtteN_H'],  
    NB_max_HCW['AtteN_H'], 
    NB_sppit_HCW['AtteN_H'],
    NB_volm_HCW['AtteN_H'],
    # Ventilat_HCW['AtteN_H'],  
    screenin_HCW['AtteN_H'],
    # Vet_Curt_HCW['AtteN_H'], 
    # AS_Vent_HCW['AtteN_H'],
    # NBV_Vent_HCW['AtteN_H'],
    AS_NBV_Vent_HCW['AtteN_H'],
                  
    Base_case_HCW['Imagi_H'], 
    Curtains_HCW['Imagi_H'],
    FFP_HCW['Imagi_H'], 
    NB_max_HCW['Imagi_H'], 
    NB_sppit_HCW['Imagi_H'],
    NB_volm_HCW['Imagi_H'],
    # Ventilat_HCW['Imagi_H'],  
    screenin_HCW['Imagi_H'],
    # Vet_Curt_HCW['Imagi_H'],  
    # AS_Vent_HCW['Imagi_H'],
    # NBV_Vent_HCW['Imagi_H'],
    AS_NBV_Vent_HCW['Imagi_H'],
                  
    Base_case_HCW['Labot_H'], 
    Curtains_HCW['Labot_H'],
    FFP_HCW['Labot_H'],  
    NB_max_HCW['Labot_H'], 
    NB_sppit_HCW['Labot_H'],
    NB_volm_HCW['Labot_H'],
    # Ventilat_HCW['Labot_H'],  
    screenin_HCW['Labot_H'],
    # Vet_Curt_HCW['Labot_H'], 
    # AS_Vent_HCW['Labot_H'],
    # NBV_Vent_HCW['Labot_H'],
    AS_NBV_Vent_HCW['Labot_H'],
    
    
    HCW_BC, 
    HW_Cur, 
    HW_ROM, 
    HW_NCM,
    HW_NBS, 
    HW_NBV,
    # HW_Ven, 
    HW_ALL,
    # HW_V_C,
    # HW_ASV, 
    # HW_NVV, 
    HW_ABV,
    

                  ],  
    palette = cols,
      showmeans = True, 
      showfliers = False,
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s}) 
plt.xticks(plase, areas2, fontsize=16)
plt.ylabel('Total of newly infected HCWs \nper area', fontsize = labels +2)
# plt.ylim(top=30) 
plt.ylim(top=12)
# plt.legend(names2, fontsize=16)
# plt.savefig('24_Fom_figs/Areas_hcw.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/areas_total_HCW.svg', format='svg', dpi=1400)



'''           Fomites

'''
f, ax4 = plt.subplots(figsize=(17,6), facecolor='w', edgecolor='k')
# ax3.set_yscale("log")
plt.rc('xtick', labelsize = labels) 
plt.ylabel('Total of contamination events\n in fomites (complete ED)', fontsize = labels +1)
plt.rc('ytick', labelsize = 17) 

sns.boxplot(data=[

        
        Base_FOM, 
        Curt_FOM, 
        N_VC_FOM, 
        NB_FOM  ,   
        NB_s_FOM,  
        NB_v_FOM,          
        scre_FOM,  
        A_NB_FOM 
        
        # Base_TOT,       
        # Curt_TOT,
        # N_VC_TOT,    # HS
        # NB_TOT,      # AS
        # NB_sppit, 
        # NB_vol,
        # scre_TOT,    # HS + AS
        # A_NB_TOT
        
        
        ], 
        palette = cols,
        # palette="Set3",
        # Vent_TOT, V_Cu_TOT], palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})   
# plt.xticks(np.arange(12), names, rotation = 35) 
plt.xticks(np.arange(8), names) 
# plt.ylim(top=60) 
# plt.title('Total of newly infected', fontsize = lette)
# plt.savefig('24_Fom_figs/fomites.pdf', format='pdf', dpi=1400)
# plt.savefig('figures/5_drft_upd/totals.svg', format='svg', dpi=1400)

#----------------------------------------------------------------


