# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:15:40 2021

    InnoBRI Emergency Department Simulation Platform
    Main file
    Functions driver file 
    
@author: Gustavo Hernandez Mejia

"""
from functions_plat_ED_WWU import *

import random
import matplotlib.pyplot as plt
import math  
import time
import numpy as np
import pandas as pd
import csv
import collections, numpy
# import seaborn as sns

t1 = time.perf_counter()

prop_cycle = plt.rcParams['axes.prop_cycle'] # Colors
colors = prop_cycle.by_key()['color']


M_D = 100  #  100 cm  

Test_var = 1
print("Test variable:",Test_var)

"""---------------------------------------------------------------------------             
                    Users of emergency department 
                             VARIABLES
                              
"""

global Users, V_recep, V_triag, V_nurse_No_Urg, dr_No_Urg_V
global V_nurse_Urg, V_dr_Urg, V_imagin, V_labor, med_test, back_lab, back_time
global invasiv_prob, neg_press_prob
global PB_RECE, P_TRI_R, P_WAT_N, P_WAT_U, P_N_URE, PB_URGE, PB_LABO, PB_IMAG,PB_ARE_test,PB_SYMPTOMS
global ISOLA_R, SHOCK_R, INVASIV, NEGATIV
global Own_Arrive, Suspicion_of_infection, Isolation_needed, Time_scale
global User_track_1, Seat_map, day_current, day
global N_new_day_from_shift_1,N_new_day_from_shift_2, N_new_day_from_shift_3
global Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3
global RECEP, TRIAG, WAI_N, WAI_U,  N_URG, U_URG,IMAGI, LABOR,EXIT_
global AT_UR, At_NU, Num_Aget, ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3
global ROMS_G, ROMS_G_NAM



RECEP = 'RECEPTION'
TRIAG = 'TRIAGE'
TRIAG_U = 'TRIAGE_URGENT'
WAI_N = 'WAIT_NO_URGENT'
WAI_U = 'WAIT_URGENT'
N_URG = 'NOT_URGENT'
U_URG = 'URGENT'
IMAGI = 'IMAGING'
LABOR = 'LABORATORY'
EXIT_ = 'EXIT'
AT_UR = 'ATTEN_URGE'
At_NU = 'ATTE_N_URG'
HCW_B = 'HCW_BASE'
# ARE_test = 'ARE_test'
# HCW_B = 'ATTE_N_URG'


UNDEF = 'UNDEFINED'

ISOLA = 'ISOLATION_ROOM'
SHOCK = 'SHOCK_ROOM'
INVAS = 'INVASIVE_INTERVENTION_ROOM'
NEGAT = 'NEGATIVE_PRESSURE_ROOM'

INFEC = 'INFECTED'
PATIEN = 'PATIENT'
N_URGE = 'N_URGENT'
N_N_URG = 'N_N_URGE'
DR_URGE = 'DR_URGEN'
D_N_URG = 'DR_N_URGE'

SYMP_YES = 'SYMPTOM_YES'
SYMP_NO = 'SYMPTOM_NO'
REPLACE= 'ALREADY REPLACED'
DAY_SPECIFIC = "Day_spec_infec"



"""----------------------------------------------------------------------------
                            ARRIVAL DATA 
"""
# df = pd.read_excel (r'data_arriv\Arriving_data.xlsx', sheet_name='D1')
Df = pd.read_excel (r'data_arriv\Arriving_data.xlsx',sheet_name = None)
Aget_day = Df['Total']

# Tr_Pr = pd.read_excel (r'data_arriv\TP_ED _reduced.xlsx',sheet_name = None)
# TP_pyth = 0.01


# Tr_Pr = pd.read_excel (r'data_arriv\TP_ED_reduced_03_22.xlsx',sheet_name = None)
# TP_pyth = 0.01

Tr_Pr = pd.read_excel (r'data_arriv\1_BASE_TP_end.xlsx',
                                                            sheet_name = None)
TP_pyth = 0.01
# TP_pyth = TP_pyth * 0.052 # 0.062  Reduction General
TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General

Tr_Pr_NEAR = pd.read_excel (r'data_arriv\TP_ED _Near.xlsx',sheet_name = None)
TP_pyth_Near = 0.01
TP_pyth_Near = TP_pyth_Near* 0.052 # 0.062  Reduction General

# TP_pyth_Near = TP_pyth_Near* 0.02 # 0.062  Reduction General

# TP_pyth_Near = TP_pyth_Near* 0
# TP_pyth = TP_pyth * 0.2 # Reduction General

# TP_pyth = TP_pyth * 0.052 # 0.062  Reduction General
# TP_pyth = TP_pyth * 0
# TP_pyth = TP_pyth * 1   # Norm



for i in range(len(Tr_Pr['1_Reception'])):
    Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
    Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
    Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
    Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
    Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
    Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
    Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
    Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
    Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
    Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'] = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
    


# D01 = Df['D1']
# D02 = Df['D2']
# D03 = Df['D3']
# D04 = Df['D4']
# D05 = Df['D5']
# D06 = Df['D6']
# D07 = Df['D7']
# D08 = Df['D8']
# D09 = Df['D9']
# D10 = Df['D10']
# D11 = Df['D11']
# D12 = Df['D12']
# D13 = Df['D13']
# D14 = Df['D14']
# D15 = Df['D15']
# D16 = Df['D16']
# D17 = Df['D17']
# D18 = Df['D18']
# D19 = Df['D19']
# D20 = Df['D20']
# D21 = Df['D21']
# D22 = Df['D22']
# D23 = Df['D23']
# D24 = Df['D24']
# D25 = Df['D25']
# D26 = Df['D26']
# D27 = Df['D27']
# D28 = Df['D28']
# D29 = Df['D29']
# D30 = Df['D30']


# WK_cases = [3, 26, 2, 1]
# WK_cases = [2, 3, 26, 2]
WK_cases = [4, 5, 4, 5] #[0, 0, 0, 0]
WK_7days = 7
WK_8days = 8
WK_1 = np.random.randint(1,WK_7days, size=(WK_cases[0]) )
WK_2 = np.random.randint(1,WK_8days, size=(WK_cases[1]) )
WK_3 = np.random.randint(1,WK_8days, size=(WK_cases[2]) )
WK_4 = np.random.randint(1,WK_7days, size=(WK_cases[3]) )

WK_1_cases = []
for i in range(WK_7days):
    WK_1_cases.append( collections.Counter(WK_1)[i]  )

WK_2_cases = []
for i in range(WK_8days):
    WK_2_cases.append( collections.Counter(WK_2)[i]  )
    
WK_3_cases = []
for i in range(WK_8days):
    WK_3_cases.append( collections.Counter(WK_3)[i]  )

WK_4_cases = []
for i in range(WK_7days):
    WK_4_cases.append( collections.Counter(WK_4)[i]  )

day_cases = WK_1_cases + WK_2_cases + WK_3_cases + WK_4_cases

# cases = day_cases*25
# day_cases = cases


"""--------------------------------------------------------------------------
                            TIME 
"""
h_ranges = []
hrs = 24
for i in range(hrs):
    h_ranges.append([(i*60)+1, (i+1)*60])


Num_Aget = Aget_day.loc[0, "tot"]  # Min 6
N_days = len(Aget_day)  # 30  


# A1 = int(Aget_day.iloc[day])

"""--------------------------------------------------------------------------
                            PATIENTS 
"""

day_current = 0
#                  Time scaling, MINUTES
Time_scale = 60*24*1*1*1   #  ->  minutes, hours, days, month, year
Active_Period = [1, 60*24] #  ->  5 h, 21h 

N_infected = 1   # random.randint(1,3) OPTION

Time_var = 0
med_test = 1
actual_user = 0

# time_area_HCW = 60*2
time_area_HCW = 40

time_area_HCW_Att = 20


# FAR_CONT = 0.05

# CURTAINS = 0.9
# VENTILAT = 0.7
# CURT_VEN = 0.6
# NB_INTER = 0.7

# ATT_NU_H_H = 0.08    # start 0.08


# Prop_P_H_N = 0.25
# Prop_P_H_M = 0.15

Prop_P_H_N = 0.25
Prop_P_H_M = 0.1
Prop_P_P = 1
Prop_H_H_Recep = 40
Prop_H_H_Triag = 40
Prop_H_H_Nu_Nu = 20
Prop_H_H_MD_Nu = 10
Prop_H_H_Labor = 30
Prop_H_H_Nur_B = 30

NB_SPLIT = 0

# Mask = ['F_BR','F_BR','F_BR','F_BR']



"""

    OFFICIAL INTERVENTION  TOTAL MODEL
    1 - Waiting area split into two rooms
    2 - Non-urgent attention into three rooms

"""

#------------------------------------------------------------------------------
#         GENERAL CONTRIBUTION INTERACTIONS
#                    PSEUDOMONAS

Prop_R_proce = 1 # Proportion, for all processes
Prop_Pseudom = 4.3 # Pham paper - cross-transmission
Prop_ICU = 55      # Example ICU tratment of patients
Pro_pat_ICU = 7    # Example ICU pat-pat
beta_Pseudom = Prop_Pseudom/(Prop_ICU*Pro_pat_ICU)/5
TP_Gener_Pse = 0.0001   # General calibration - IF NEEDED


# Reception
R_recep = random.randint(1,5)*Prop_R_proce # relative contrib of process
# R_recep = 0
Pat_pat_recep = 0    * beta_Pseudom * R_recep
Pat_hcw_recep = 0.8  * beta_Pseudom * R_recep
hcw_hcw_recep = 0    * beta_Pseudom * R_recep
pat_fom_recep = 0.05 * beta_Pseudom * R_recep
hcw_fom_recep = 0.15 * beta_Pseudom * R_recep

# Triage
R_triag = random.randint(1,5)*Prop_R_proce # relative contrib of process
# R_triag = 0
Pat_pat_triag = 0    * beta_Pseudom * R_triag
Pat_hcw_triag = 0.8  * beta_Pseudom * R_triag
hcw_hcw_triag = 0    * beta_Pseudom * R_triag
pat_fom_triag = 0.05 * beta_Pseudom * R_triag
hcw_fom_triag = 0.15 * beta_Pseudom * R_triag

# Waiting area
R_waitg = random.randint(5,10)*Prop_R_proce # relative contrib of process
# R_waitg = 0
Pat_pat_waitg = 0.3 * beta_Pseudom * R_waitg
Pat_hcw_waitg = 0   * beta_Pseudom * R_waitg
hcw_hcw_waitg = 0   * beta_Pseudom * R_waitg
# pat_fom_waitg = 0.7 * beta_Pseudom * R_waitg * 100
pat_fom_waitg = 0.7 * beta_Pseudom * R_waitg * 1
hcw_fom_waitg = 0   * beta_Pseudom * R_waitg

# Attention areas
R_atten = random.randint(20,60)*Prop_R_proce # relative contrib of process
# R_atten = 0
Pat_pat_atten = 0.07  * beta_Pseudom * R_atten 
Pat_hcw_atten = 0.425 * beta_Pseudom * R_atten 
hcw_hcw_atten = 0.15  * beta_Pseudom * R_atten 
pat_fom_atten = 0.28  * beta_Pseudom * R_atten * 1
hcw_fom_atten = 0.135 * beta_Pseudom * R_atten * 1

# Imaging 
R_imagi = random.randint(5,5)*Prop_R_proce # relative contrib of process
# R_imagi = 0
Pat_pat_imagi = 0       * beta_Pseudom * R_imagi
Pat_hcw_imagi = 0       * beta_Pseudom * R_imagi
hcw_hcw_imagi = 0       * beta_Pseudom * R_imagi
pat_fom_imagi = 0.00001 * beta_Pseudom * R_imagi
hcw_fom_imagi = 0       * beta_Pseudom * R_imagi

# Lab 
R_labor = random.randint(5,5)*Prop_R_proce # relative contrib of process
# R_labor = 0
Pat_pat_labor = 0   * beta_Pseudom * R_labor
Pat_hcw_labor = 0   * beta_Pseudom * R_labor
hcw_hcw_labor = 0   * beta_Pseudom * R_labor
pat_fom_labor = 0   * beta_Pseudom * R_labor
hcw_fom_labor = 0.5 * beta_Pseudom * R_labor

# Nurse base 
R_nurse = random.randint(5,10)*Prop_R_proce # relative contrib of process
# R_nurse = 0
Pat_pat_nurse = 0   * beta_Pseudom * R_nurse
Pat_hcw_nurse = 0   * beta_Pseudom * R_nurse
hcw_hcw_nurse = 0.4 * beta_Pseudom * R_nurse * 1
pat_fom_nurse = 0   * beta_Pseudom * R_nurse
# hcw_fom_nurse = 0.6 * beta_Pseudom * R_nurse * 100
hcw_fom_nurse = 0.6 * beta_Pseudom * R_nurse * 1

# --------------- INFECTION PERIODS -------------------------------------------
time_length_colonized = 3
time_length_asymptomatic = 5
time_length_infectious = 8

# --------------- FOMITE PARAMETERS -------------------------------------------

# definable variables
fomite_start_contam = 0.1 # probability that a fomite starts out contaminated
number_chairs_holding = 40 # number of chairs in default holding area (sans intervention)
number_chairs_holding_int = 20 # 1/2 of number_chairs_holding
prolonged_contact = 1 # increased transmission probability for prolonged contact (i.e. with waiting room chairs)
all_foms = range(0,11)

tp_person_Fomite = 1 * beta_Pseudom # transmission probability from person to fomite
# tp_Fomite_person = 0.1 # transmission probability from fomite to person
tp_Fomite_person_low_x100 = 4 # min transmission probability from fomite to person times 100
tp_Fomite_person_high_x100 = 10 # max transmission probability from fomite to person times 100
def tp_Fomite_person(tp_low_x100=tp_Fomite_person_low_x100, tp_high_x100=tp_Fomite_person_high_x100):
    tp_Fom_per = random.randint(tp_low_x100, tp_high_x100)
    tp_Fom_person = (tp_Fom_per/100) #* beta_Pseudom
    return(tp_Fom_person)
contact_occurs = 0.5 # probability that contact occurs between person and fomite (i.e. how often fomite is used) -- can differentiate by area/fomite

time_hand_clean = 10 # number of minutes that hands remain clean after washing
wash_hand_post_fom = 0.2 # probability that a HCW washes their hands after touching fomites (potentially infectious material / direct patient environment)
wash_hand_effectiveness = 0.2 # probability that washing hands will stop transmission from occurring
probability_clean_fomite = 0.1 # 0.5 # probability that a fomite is cleaned after use (takes into consideration probability of being soiled)
daily_cleaning_time = 0 # time of day (in minutes) when all fomites are cleaned
prob_fomite_uncontam_after_clean = 0.8 # probability that a fomite is no longer contaminated after cleaning

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#                            OFFICIAL   INTERVENTIONS
#                              NEW BASE CASE

#                               1 BASE CASE
#        

N_rooms_ = 6
N_beds_ = 6
# ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

ROMS_G = []
ROMS_G_NAM = []
for i in range(0, N_rooms_):
    ROMS_G.append(1)
    ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

BEDS_G = []
BEDS_G_NAM = []
for i in range(0, N_beds_):
    BEDS_G.append(1)
    BEDS_G_NAM.append('BEDS_{}'.format(i+1))


Area_1 = ROMS_G_NAM[0:3]
Area_2 = ROMS_G_NAM[3:6]

Area_1_U = BEDS_G_NAM[0:3]
Area_2_U = BEDS_G_NAM[3:6]

New_wait_URGT = 10
# WaitU_fact = 1000
New_wait_URGT_RED = 5

# -----------------  - Intervention indicators 

ATTEN_NU_INTRV = 0
Atten_intrv_fact = 0.5
ATTEN_NON_UR_ROOM_1 = 1
ATTEN_NON_UR_ROOM_2 = 1
ATTEN_NON_UR_ROOM_3 = 1


WAIT_NU_INTRV = 0
Wait_intrv_fact = 1

CURTAINS_INTRV = 0
CURTAINS = random.uniform(0.84,0.91)

VENTILA_INTRV = 0
if VENTILA_INTRV:
    Recep_venti = 0.80   # 20 % reduction
    Triag_venti = 0.75   # 25 % reduction
    WaitU_venti = 0.70   # 30 % reduction
    WaitN_venti = 0.80   # 20 % reduction
    Att_U_venti = 1
    Att_N_venti = 0.85   # 15 % reduction
    Imagi_venti = 0.90   # 10 % reduction
    Labor_venti = 1
    Nur_B_venti = 0.90   # 10 % reduction
else:
    Recep_venti = 1
    Triag_venti = 1
    WaitU_venti = 1
    WaitN_venti = 1
    Att_U_venti = 1
    Att_N_venti = 1
    Imagi_venti = 1
    Labor_venti = 1
    Nur_B_venti = 1

NB_INTER = 1
T_NB = 0.4 * NB_INTER

# HCW_BASES = 1
Att_interv = 1
# Att_NU_pro = 0.5     # start 0.5
Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs
PB_SYMPTOMS = 1-0.41 # Proportion of asymptomatic infections among infected HCWs

NB_SPLIT = 0
NB_ROOM = 0
HEAD_wait_NU = 1  # HEADS update
HEAD_wait_U = 1   # HEADS update
HEAD_Att_NU = 1  # HEADS update
HEAD_Att_U = 1    # HEADS update
HEAD_Imag = 1    # HEADS update
HEAD_Labor = 1     # HEADS update
# CURTAINS = random.uniform(0.84,0.91)
# VENTILAT = random.uniform(0.65,0.75)

# VENTILAT = 0.75
VENTILAT = 1
# CURTAINS = 1
# VENTILAT = 1
Recep_fact = 1 * Recep_venti
Triag_fact = 1 * Triag_venti
WaitU_fact = 1 * WaitU_venti
WaitN_fact = 1 * WaitN_venti
Att_U_fact = 1 * Att_U_venti
Att_N_fact = 1 * Att_N_venti
Imagi_fact = 1 * Imagi_venti
Labor_fact = 1 * Labor_venti
Nur_B_fact = 1 * Nur_B_venti

Mask = ['S_SP','S_BR','F_SP','F_BR']
SCREE_HCW = 0


#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                           INTERVENTION  
#                            2 CURTAINS (FP)

#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 1
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
#     Recep_venti = 0.80   # 20 % reduction
#     Triag_venti = 0.75   # 25 % reduction
#     WaitU_venti = 0.70   # 30 % reduction
#     WaitN_venti = 0.80   # 20 % reduction
#     Att_U_venti = 1
#     Att_N_venti = 0.85   # 15 % reduction
#     Imagi_venti = 0.90   # 10 % reduction
#     Labor_venti = 1
#     Nur_B_venti = 0.90   # 10 % reduction
# else:
#     Recep_venti = 1
#     Triag_venti = 1
#     WaitU_venti = 1
#     WaitN_venti = 1
#     Att_U_venti = 1
#     Att_N_venti = 1
#     Imagi_venti = 1
#     Labor_venti = 1
#     Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                             INTERVENTION  

#                               3 VENTILAT
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                                INTERVENTION  

#                            4 VENTILAT + CURTAINS
#        


# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 1
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                            OFFICIAL INTERVENTION  
#                    
#                             5  WAIT_NU_INTRV (HS)
#        


# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 1
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#                                 INTERVENTION  
#                    
#                             6 ATTEN_NU_INTRV (AS)
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                            OFFICIAL INTERVENTION  
#    
#                       7 ATTEN_NU_INTRV + WAIT_NU_INTRV (HS+AS)
#      
  
# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 1
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
#                                  INTERVENTION  
#                                  8 NB split (EBS)
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 1
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0


#------------------------------------------------------------------------------


#TODO NB_ROOM

#------------------------------------------------------------------------------
#                              INTERVENTION  

#                                9 NB Vol (EBE)
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
#                              INTERVENTION  

#                              10 AS + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 0
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
#                              INTERVENTION  

#                              11 NBV + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 0
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                              INTERVENTION  

#                              12 AS + NBV + Vent
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 1
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 0.9
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                              INTERVENTION  

#                              13 AS + NBV  (AS+EBE)
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 1
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti


# Pat_pat_atten = Pat_pat_atten * 0.9
# Pat_hcw_atten = Pat_hcw_atten * 0.9
# hcw_hcw_atten = hcw_hcw_atten * 0.9
# pat_fom_atten = pat_fom_atten * 0.9
# hcw_fom_atten = hcw_fom_atten * 0.9

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#                              INTERVENTION  

#                              14 AS(Vent) + NBV 
#        

# N_rooms_ = 6
# N_beds_ = 6
# # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
# # ROMS_G_NAM = ['ROOM_1', 'ROOM_2','ROOM_3']

# ROMS_G = []
# ROMS_G_NAM = []
# for i in range(0, N_rooms_):
#     ROMS_G.append(1)
#     ROMS_G_NAM.append('ROOM_{}'.format(i+1))
    

# # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]
# # BEDS_G_NAM = ['BEDS_1', 'BEDS_2','BEDS_3']

# BEDS_G = []
# BEDS_G_NAM = []
# for i in range(0, N_beds_):
#     BEDS_G.append(1)
#     BEDS_G_NAM.append('BEDS_{}'.format(i+1))


# Area_1 = ROMS_G_NAM[0:3]
# Area_2 = ROMS_G_NAM[3:6]

# Area_1_U = BEDS_G_NAM[0:3]
# Area_2_U = BEDS_G_NAM[3:6]

# New_wait_URGT = 10
# # WaitU_fact = 1000
# New_wait_URGT_RED = 5

# # -----------------  - Intervention indicators 

# ATTEN_NU_INTRV = 1
# # Atten_intrv_fact = 0.5
# ATTEN_NON_UR_ROOM_1 = 1
# ATTEN_NON_UR_ROOM_2 = 1
# ATTEN_NON_UR_ROOM_3 = 1


# WAIT_NU_INTRV = 0
# Wait_intrv_fact = 1

# CURTAINS_INTRV = 0
# CURTAINS = random.uniform(0.84,0.91)

# VENTILA_INTRV = 0
# if VENTILA_INTRV:
    
#     Tr_Pr = pd.read_excel (r'data_arriv\2_Ventil_TP_Update_HEADS_May_22.xlsx',
#                                                             sheet_name = None)
#     TP_pyth = 0.01
#     TP_pyth = TP_pyth * 0.02 # 0.062  Reduction General
    
#     for i in range(len(Tr_Pr['1_Reception'])):
#         Tr_Pr['1_Reception'].loc[i,'m'] = int(Tr_Pr['1_Reception'].loc[i,'m'])
#         Tr_Pr['2_Triage'].loc[i,'m']    = int(Tr_Pr['2_Triage'].loc[i,'m'])
#         Tr_Pr['3_Wait_NoN'].loc[i,'m']  = int(Tr_Pr['3_Wait_NoN'].loc[i,'m'])
#         Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'] = int(Tr_Pr['4_Wait_Urg_Flur'].loc[i,'m'])
#         Tr_Pr['5_Atte_NoN'].loc[i,'m']  = int(Tr_Pr['5_Atte_NoN'].loc[i,'m'])
#         Tr_Pr['6_Atte_Urg_1'].loc[i,'m']= int(Tr_Pr['6_Atte_Urg_1'].loc[i,'m'])
#         Tr_Pr['7_Imaging'].loc[i,'m']   = int(Tr_Pr['7_Imaging'].loc[i,'m'])
#         Tr_Pr['8_Laborat'].loc[i,'m']   = int(Tr_Pr['8_Laborat'].loc[i,'m'])
#         Tr_Pr['10_WAIT_INTRV'].loc[i,'m']   = int(Tr_Pr['10_WAIT_INTRV'].loc[i,'m'])
#         Tr_Pr['11_Att_NU_INTRV'].loc[i,'m']   = int(Tr_Pr['11_Att_NU_INTRV'].loc[i,'m'])
        

    
#     # Recep_venti = 0.80   # 20 % reduction
#     # Triag_venti = 0.75   # 25 % reduction
#     # WaitU_venti = 0.70   # 30 % reduction
#     # WaitN_venti = 0.80   # 20 % reduction
#     # Att_U_venti = 1
#     # Att_N_venti = 0.85   # 15 % reduction
#     # Imagi_venti = 0.90   # 10 % reduction
#     # Labor_venti = 1
#     # Nur_B_venti = 0.90   # 10 % reduction
# # else:
# Recep_venti = 1
# Triag_venti = 1
# WaitU_venti = 1
# WaitN_venti = 1
# Att_U_venti = 1
# Att_N_venti = 0.9
# Imagi_venti = 1
# Labor_venti = 1
# Nur_B_venti = 1

# NB_INTER = 1
# T_NB = 0.4 * NB_INTER

# # HCW_BASES = 1
# Att_interv = 1
# # Att_NU_pro = 0.5     # start 0.5
# Att_NU_pro = 1
# PB_SYMPTOMS = 0.41 # Proportion of asymptomatic infections among infected HCWs

# NB_SPLIT = 0
# NB_ROOM = 1
# HEAD_wait_NU = 1  # HEADS update
# HEAD_wait_U = 1   # HEADS update
# HEAD_Att_NU = 1  # HEADS update
# HEAD_Att_U = 1    # HEADS update
# HEAD_Imag = 1    # HEADS update
# HEAD_Labor = 1     # HEADS update
# # CURTAINS = random.uniform(0.84,0.91)
# # VENTILAT = random.uniform(0.65,0.75)

# # VENTILAT = 0.75
# VENTILAT = 1
# # CURTAINS = 1
# # VENTILAT = 1
# Recep_fact = 1 * Recep_venti
# Triag_fact = 1 * Triag_venti
# WaitU_fact = 1 * WaitU_venti
# WaitN_fact = 1 * WaitN_venti
# Att_U_fact = 1 * Att_U_venti
# Att_N_fact = 1 * Att_N_venti
# Imagi_fact = 1 * Imagi_venti
# Labor_fact = 1 * Labor_venti
# Nur_B_fact = 1 * Nur_B_venti

# Mask = ['S_SP','S_BR','F_SP','F_BR']
# SCREE_HCW = 0

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#         1                  FAR-AND NEAR-FIELD TPS 

#    Reception
TP_Farf_Recep = 0
TP_Near_Recep = 1
TP_Fom_Recep = 1

#    Triage (perform in reception)
TP_Farf_Triag = 0
TP_Near_Triag = 0
TP_Fom_Triag = 0

#    Waiting urgent area
TP_Farf_WaitU = 0
TP_Near_WaitU = 0
# Note: no urgent waiting for fomites

#    Holding area
TP_Farf_WaiNU = 0
if ((WAIT_NU_INTRV == 1) ):
    TP_Farf_WaiNU_INT = 0
TP_Near_WaiNU = 1
if ((WAIT_NU_INTRV == 1) ):
    TP_Near_WaiNU_INT = 1
TP_Fom_WaiNU = 1
if ((WAIT_NU_INTRV == 1)):
    TP_Fom_WaiNU_INT = 1

#    Attention Urgent Area
TP_Farf_At_Ur = 0   # subject to commented previous TP setting in original code
TP_Near_At_Ur = 1
TP_Fom_At_Ur = 1

#    Attention Non Urgent Area
# original setting TP
# TP_Farf_At_NU = Att_N_fact * HEAD_Att_NU *Att_interv * Att_NU_pro
TP_Farf_At_NU = 0   # subject to commented previous TP setting in original code
if ((ATTEN_NU_INTRV == 1) or (CURTAINS_INTRV == 1)):
    TP_Farf_At_NU_INT = 0
TP_Near_At_NU = 1   #  subject to commented TP Near-field
if ((ATTEN_NU_INTRV == 1) or (CURTAINS_INTRV == 1)):
    TP_Near_At_NU_INT = 1
# Note: assess (non-)urgent together so no non-intervention non-urgent param
if ((ATTEN_NU_INTRV == 1) or (CURTAINS_INTRV == 1)):
    TP_Fom_At_NU_INT = 1

#     Imaging
TP_Farf_Imagi = 0
TP_Near_Imagi = 1
# Note: no fomites considered in imaging

#     Laboratory
TP_Farf_Labor = 0
TP_Near_Labor = 1
# Note: no fomites considered in laboratory

#     HCW Base
TP_Farf_HCW_B = 0
if ((NB_SPLIT == 1) or (NB_ROOM == 1)):
    TP_Farf_HCW_B_INT = 0
TP_Near_HCW_B = 1
if ((NB_SPLIT == 1) or (NB_ROOM == 1)):
    TP_Near_HCW_B_INT = 1
TP_Fom_HCW_B = 1 # NOTE: fomites in ED Base run same for intervention & not









# shift_1 =  [1, 480]  #on minutes bases, min 1 to 480 minutes (60*8) 
# shift_2 =  [481, 960]
# shift_3 =  [961, 1440]

# shift_1 = [60*6, 60*(6+8)] # ->  6 h, 14 h 
# shift_2 = [(60*(6+8))+1, 60*(6+8+8)]
# shift_3 = [(60*(6+8+8))+1, (60*6)-1]

shift_1 = [1, 60*(8)] # ->  6 h, 14 h 
shift_2 = [(60*(8))+1, 60*(8+8)]
shift_3 = [(60*(8+8))+1, (60*(8*3))-1]

color_wait = ['YELLLOW','GREEN','BLUE']  



# time_arriv = []
# # for i in range(Num_Aget):
# for i in range(Aget_day.loc[0, "tot"]):
#     time_arriv.append(random.randint(Active_Period[0], Active_Period[1]))
# time_arriv.sort()


t_arriv = []
for i in range(hrs):
    pati = int(Df['D'+str(1)].loc[i, "DAY"])
    if pati > 0:
        for k in range(pati):
            t_ar = random.randint(h_ranges[i][0], h_ranges[i][1])   
            t_arriv.append(t_ar)
            t_arriv.sort()
            
color = ['RED','ORANGE','YELLLOW','GREEN','BLUE','WITHOUT']            
triag_pat = []
for i in range(hrs):
    for k in range(len(color)):
        if (Df['D'+str(1)].loc[i,color[k]]) > 0:
            for qq in range(Df['D'+str(1)].loc[i,color[k]]):
                if ('WITHOUT' == color[k]):
                    k1 = random.randint(2, 4)
                    triag_pat.append(color[k1])
                else:    
                    triag_pat.append(color[k])
            
            
    

            # triag_pat.sort()            
            

     # SET THE NUMBER OF USERS
Users = []
# for i in range(Num_Aget):
for i in range(Aget_day.loc[0, "tot"]):
    # User -> Agent_Number, Infection Status, Area, Area-Time, Area-time_count, arriv, 
    # interact_moment, side_time, side_label, area of getting infected?, day, 
    # symptom, indicate staff on shift
    # ESI Red - Blue
    # 15: ROOM to be in in case of attention non-urgent
    
    # 0 - Agent_Number[1:32]
    # 1 - Infection Status[0=Uninfected, 1=arrived infected, 2=nosocomial]
    # 2 - Area [current area of User]
    # 3 - Area-Time [integer stating total time spent in area]
    # 4 - Area-time_count [integer counting time spent in area]
    # 5 - arriv [integer stating arrival in ED]
    # 6 - interact_moment  [0]
    # 7 - side_time [0]
    # 8 - side_label (area???)
    # 9 - area of getting infected
    # 10 - day [0, 30]
    # ? - symptom??? [UNDEFINED]
    # 11 - indicate staff on shift
    # 12 - ESI [(RED?), ORANGE, YELLOW, GREEN, BLUE]
    # 13 - ???? [UNDEFINED]
    # 14 - ???? [UNDEFINED]
    # 15: ROOM to be in in case of attention (non-urgent=room, urgent=bed)
    #     [ROOM_1 : ROOM_6, BEDS_1 : BEDS_6, UNDEFINED]
    # 16: indicate fomite from which infection came
    # 17: actual room (not bed) to be used in case of attention base case 
    #     (used for fomite interaction)
    #     ["UR_Room_13", "UR_Room_46", "NU_Room_13", "NU_Room_46"]
    # 18: chair used in holding area
    Users.append([i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, UNDEF, UNDEF, 0, 
                  UNDEF, triag_pat[i], UNDEF, UNDEF, UNDEF, UNDEF, UNDEF, 0])

   
User_track_1 = []


"""--------------------------------------------------------------------------
                            FOMITES
   
"""


# --------------- FOMITES INIT ------------------------------------------------

     # SET THE NUMBER OF Fomites
Fomite = []
number_fomites = 11
# for i in range(Num_Aget):
for i in range(number_fomites):
    # 0 - number of fomite
    # 1 - type of fomite
    # 2 - Inf_status
    # 3 - duration (in minutes) that it stays contaminated
    # 4 - counter of status
    # 5 - location of fomite
    # 6 - room of fomite
    # 7 - time when infected
    # 8 - who contaminated fomite
    # 9 - 
    # 10 - TP lower range  ??? (depending on how many dif ones -- if similar, use if statement in function)
    # 11 - TP upper range  ???
    Fomite.append([i+1, UNDEF, UNDEF, 0, 0, UNDEF, UNDEF, 0, UNDEF]) # note: appears later too (search for "Fomite.append")
    
Type_Fomite = ["Counter", "PC", "Chair", "BPCuff", "Sink", "Light", "Door"]
Status_Fomite = ["Uncontaminated", "Contaminated"]
Duration_Fomite = 1440
Location_Fomite = [RECEP, WAI_N, AT_UR, At_NU, HCW_B]
# Location_Fomite = [At_NU, AT_UR]
Room_Fomite = ["UR_Room_13", "UR_Room_46", "NU_Room_13", "NU_Room_46"]
Room_Fomite_Intervention = ["ROOM_1", "ROOM_2", "ROOM_3",
                            "ROOM_4", "ROOM_5", "ROOM_6"]
                            # "BEDS_1", "BEDS_2", "BEDS_3",
                            # "BEDS_4", "BEDS_5", "BEDS_6",
# Room_Fomite_Intervention = ["UR_Room_1", "UR_Room_2", "UR_Room_3",
#                             "UR_Room_4", "UR_Room_5", "UR_Room_6",
#                             "NU_Room_1", "NU_Room_2", "NU_Room_3",
#                             "NU_Room_4", "NU_Room_5", "NU_Room_6"]

# set infection status of all fomites
for i in range(number_fomites):
    # Fomite[i][1] = Type_Fomite[2]
    # Fomite[i][3] = Duration_Fomite
    # Fomite[i][5] = Location_Fomite[0]
    Fomite[i][2] = Status_Fomite[0]
    if (random.random() < fomite_start_contam) == 1:
        Fomite[i][2] = Status_Fomite[1]
        Fomite[i][4] = 1
        Fomite[i][3] = Duration_Fomite
    # if Fomite[i][5] = At_NU or Fomite[i][5] = AT_UR:
        # Fomite[i][6] = Room_Fomite[0]
        # Fomite[i][7] = Bed_Fomite[0]

# fomites in reception area
for i in range(0, 2):
    Fomite[i][5] = Location_Fomite[0]
Fomite[0][1] = Type_Fomite[0]
Fomite[1][1] = Type_Fomite[1]

# fomites in holding area
# Fomite[2][5] = Location_Fomite[1]
# Fomite[2][1] = Type_Fomite[2]
Chairs = []
for i in range(number_chairs_holding):
    # 0 - number of fomite
    # 1 - type of fomite
    # 2 - Inf_status
    # 3 - duration (in minutes) that it stays contaminated
    # 4 - counter of status
    # 5 - location of fomite
    # 6 - room of fomite
    # 7 - time when infected
    # 8 - who contaminated fomite
    # 9 - occupied status
    Chairs.append([i+1, "Chair", UNDEF, 0, 0, Location_Fomite[1], "WAT_ROM", 0, UNDEF])
    Chairs[i][2] = Status_Fomite[0]
    if (random.random() < fomite_start_contam) == 1:
        Chairs[i][2] = Status_Fomite[1]
        Chairs[i][4] = 1
        Chairs[i][3] = Duration_Fomite
Fomite[2] = Chairs

# fomites in attention areas
for i in range(3, 7):
    Fomite[i][1] = Type_Fomite[3]
# non-urgent
for i in range(3, 5):
    Fomite[i][5] = Location_Fomite[2]
Fomite[3][6] = Room_Fomite[0]
Fomite[4][6] = Room_Fomite[1]
# urgent
for i in range(5, 7):
    Fomite[i][5] = Location_Fomite[3]
Fomite[5][6] = Room_Fomite[2]
Fomite[6][6] = Room_Fomite[3]

# fomites in ED base area
for i in range(7, 11):
    Fomite[i][5] = Location_Fomite[4]
Fomite[7][1] = Type_Fomite[1]
Fomite[8][1] = Type_Fomite[4]
Fomite[9][1] = Type_Fomite[5]
Fomite[10][1] = Type_Fomite[6]
fomite_EDBase_rep = (7,8)
fomite_EDBase_once = (9,10)
  
Fomite       

# --------------- INTERVENTIONS ----------------------------------------------
# Fomites for specific interventions
def intervention_add_fomite(fomite_type, fomite_location, fomite_room=UNDEF, num_new_fomites=0):
    Fomite.append([number_fomites+num_new_fomites+1, UNDEF, UNDEF, 0, 0, UNDEF, UNDEF, 0, UNDEF])
    # contamination status
    Fomite[number_fomites+num_new_fomites][2] = Status_Fomite[0]
    if (random.random() < fomite_start_contam) == 1:
        Fomite[number_fomites+num_new_fomites][2] = Status_Fomite[1]
        Fomite[number_fomites+num_new_fomites][4] = 1
        Fomite[number_fomites+num_new_fomites][3] = Duration_Fomite
    # fomite type and location
    Fomite[number_fomites+num_new_fomites][1] = fomite_type
    Fomite[number_fomites+num_new_fomites][5] = fomite_location
    Fomite[number_fomites+num_new_fomites][6] = fomite_room
    return

# change existing fomites for interventions (e.g. if room changes based on intervention)
def intervention_change_fomite(fomite_number, fomite_location, fomite_room):
    # fomite type and location
    Fomite[fomite_number-1][5] = fomite_location
    Fomite[fomite_number-1][6] = fomite_room

# Curtains or attention area separation
if CURTAINS_INTRV == 1 or ATTEN_NU_INTRV == 1:
    # intervention_change_fomite(4, AT_UR, Room_Fomite_Intervention[0])
    # intervention_add_fomite("BPCuff", AT_UR, Room_Fomite_Intervention[1], 4)
    # intervention_add_fomite("BPCuff", AT_UR, Room_Fomite_Intervention[2], 5)
    # intervention_change_fomite(5, AT_UR, Room_Fomite_Intervention[3])
    # intervention_add_fomite("BPCuff", AT_UR, Room_Fomite_Intervention[4], 6)
    # intervention_add_fomite("BPCuff", AT_UR, Room_Fomite_Intervention[5], 7)
    intervention_change_fomite(6, At_NU, Room_Fomite_Intervention[0])
    intervention_change_fomite(7, At_NU, Room_Fomite_Intervention[1])
    intervention_add_fomite("BPCuff", At_NU, Room_Fomite_Intervention[2])
    intervention_add_fomite("BPCuff", At_NU, Room_Fomite_Intervention[3], 1)
    intervention_add_fomite("BPCuff", At_NU, Room_Fomite_Intervention[4], 2)
    intervention_add_fomite("BPCuff", At_NU, Room_Fomite_Intervention[5], 3)
    all_foms = range(0,15)
    
# Waiting area separation
# # adjust probability of interaction (50%) or create 1 set of fomites per room?
# # if Users get individually assigned to 2 unique holding areas:
# # if using 1 chair as proxy
# if WAIT_NU_INTRV == 1:
#     intervention_change_fomite(3, WAI_N, "WAT_ROM_1")
#     if ATTEN_NU_INTRV == 0:
#         intervention_add_fomite("Chair", WAI_N, "WAT_ROM_2")
#     if ATTEN_NU_INTRV == 1:
#         intervention_add_fomite("Chair", WAI_N, "WAT_ROM_2", 8)
# # if have list of n vectors
if WAIT_NU_INTRV == 1:
    Chairs = []
    for i in range(number_chairs_holding):
        Chairs.append([i+1, "Chair", UNDEF, 0, 0, Location_Fomite[1], UNDEF, 0, UNDEF])
        Chairs[i][2] = Status_Fomite[0]
        if (random.random() < fomite_start_contam) == 1:
            Chairs[i][2] = Status_Fomite[1]
            Chairs[i][4] = 1
            Chairs[i][3] = Duration_Fomite
    for j in range(number_chairs_holding_int):
        Chairs[j][6] = "WAT_ROM_1"
    for j in range(number_chairs_holding_int):
        Chairs[j + number_chairs_holding_int][6] = "WAT_ROM_2"
    Fomite[2] = Chairs

# # ED base separation
# # adjust probability of interaction (50%) or create 1 set of fomites per room?
# # if HCWs get individually assigned to 2 unique ED bases:
if NB_SPLIT ==1:
    intervention_change_fomite(8, HCW_B, "ROOM_1")
    intervention_change_fomite(9, HCW_B, "ROOM_1")
    intervention_change_fomite(10, HCW_B, "ROOM_1")
    intervention_change_fomite(11, HCW_B, "ROOM_1")
    intervention_add_fomite("PC", HCW_B, "ROOM_2")
    intervention_add_fomite("Sink", HCW_B, "ROOM_2", 1)
    intervention_add_fomite("Light", HCW_B, "ROOM_2", 2)
    intervention_add_fomite("Door", HCW_B, "ROOM_2", 3)
    all_foms = range(0,15)
    fomite_EDBase_int_Rm1_rep = (7,8)
    fomite_EDBase_int_Rm1_once = (9,10)
    fomite_EDBase_int_Rm2_rep = (11,12)
    fomite_EDBase_int_Rm2_once = (13,14)

# ED base extension
# no change in fomites

# Ventillation
# no change in fomites


# Tracking transmission/contamination involving fomites
trans_Fom_User = []
trans_Fom_HCW = []
trans_User_Fom = []
trans_HCW_Fom = []



"""                            WORKERS (HCW)
                               
                 Number of HCW according to UMG data 
                               
"""
#                 SET THE NUMBER OF WORKERS PER AREA AND SHIFT (s1-s3)
recep_N_s1 = 3
recep_N_s2 = 2
recep_N_s3 = 1

triag_N_s1 = 2
triag_N_s2 = 2
triag_N_s3 = 1

triag_U_N_s1 = 2
triag_U_N_s2 = 1
triag_U_N_s3 = 1

nur_NU_N_s1 = 4
nur_NU_N_s2 = 4
nur_NU_N_s3 = 3

Dr_NU_s1 = 4
Dr_NU_s2 = 4
Dr_NU_s3 = 3
# nurs_U_N = 2
# # Dr_NU_N = 1
# Dr_Ur_N = 1

imagi_N = 2
labor_N = 1


# 0 - HCW Number[1:4?]
# 1 - Infection Status[0=Uninfected, 1=arrived infected, 2=nosocomial]
# 2 - area
# 3 - (0)
# 4 - (0)
# 5 - (UNDEF)
# 6 - (0)
# 7 - (UNDEF)
# 8 - (UNDEF)
# 9 - (UNDEF)
# 10 - (UNDEF)
# 11 - (0)
# 12 - (0)
# 13 - (0)
# 14 - (UNDEF)


"""                  Worker RECEPTION
"""

V_recep_1 = []
V_recep_2 = []
V_recep_3 = []
for i in range(recep_N_s1):
    V_recep_1.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
for i in range(recep_N_s2):
    V_recep_2.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
for i in range(recep_N_s3):
    V_recep_3.append([i, 0, RECEP, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])


"""                  Worker TRIAGE/REGIS
"""
V_triag_1 = []
V_triag_2 = []
V_triag_3 = []
for i in range(triag_N_s1):
    V_triag_1.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
for i in range(triag_N_s2):
    V_triag_2.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
for i in range(triag_N_s3):
    V_triag_3.append([i, 0, TRIAG, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    

"""                 Worker NO URGENT and URGENT (TOGETHER UMG FEEDBACK)
"""

# 15 - ?
# 16 - Indication of rooms for Non-Urgent area
# 17 - Indication of bed for Urgent area

# 18 - Indication of rooms 2 for Non-Urgent area
# 19 - Indication of bed 2 for Urgent area
V_nurse_No_Urg_1 = []
V_nurse_No_Urg_2 = []
V_nurse_No_Urg_3 = []
# for i in range(nur_NU_N_s1):
#     V_nurse_No_Urg_1.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
#                              0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                              , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                              , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
# for i in range(nur_NU_N_s2):
#     V_nurse_No_Urg_2.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
#                              0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                              , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                              , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
# for i in range(nur_NU_N_s3):
#     V_nurse_No_Urg_3.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
#                              0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                              , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                              , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
    
for i in range(nur_NU_N_s1):
    V_nurse_No_Urg_1.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                             UNDEF])
for i in range(nur_NU_N_s2):
    V_nurse_No_Urg_2.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                             UNDEF])
for i in range(nur_NU_N_s3):
    V_nurse_No_Urg_3.append([i, 0, 'Nur_NO_URG', 0, 0, UNDEF,
                             0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                             , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                             , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                             UNDEF])
       
# Manual placement of rooms and beds
V_nurse_No_Urg_1[0][16] = 'ROOM_1'
V_nurse_No_Urg_1[0][17] = 'N_BED_4'
V_nurse_No_Urg_1[0][18] = 'ROOM_6'
V_nurse_No_Urg_1[0][19] = 'N_BED_7'
V_nurse_No_Urg_1[0][20] = ['NU_Room_13', 'NA', 'NU_Room_46', 'UR_Room_46']
V_nurse_No_Urg_1[1][16] = 'ROOM_2'
V_nurse_No_Urg_1[1][17] = 'N_BED_3'
V_nurse_No_Urg_1[1][18] = 'ROOM_5'
V_nurse_No_Urg_1[1][19] = 'N_BED_7'
V_nurse_No_Urg_1[1][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'NA']
V_nurse_No_Urg_1[2][16] = 'ROOM_3'
V_nurse_No_Urg_1[2][17] = 'N_BED_2'
V_nurse_No_Urg_1[2][18] = 'ROOM_7'
V_nurse_No_Urg_1[2][19] = 'N_BED_5'
V_nurse_No_Urg_1[2][20] = ['NU_Room_13', 'UR_Room_13', 'NA', 'UR_Room_46']
V_nurse_No_Urg_1[3][16] = 'ROOM_4'
V_nurse_No_Urg_1[3][17] = 'N_BED_1'
V_nurse_No_Urg_1[3][18] = 'ROOM_7'
V_nurse_No_Urg_1[3][19] = 'N_BED_6'
V_nurse_No_Urg_1[3][20] = ['NA', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']

V_nurse_No_Urg_2[0][16] = 'ROOM_2'
V_nurse_No_Urg_2[0][17] = 'N_BED_3'
V_nurse_No_Urg_2[0][18] = 'ROOM_5'
V_nurse_No_Urg_2[0][19] = 'N_BED_7'
V_nurse_No_Urg_2[0][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'NA']
V_nurse_No_Urg_2[1][16] = 'ROOM_1'
V_nurse_No_Urg_2[1][17] = 'N_BED_4'
V_nurse_No_Urg_2[1][18] = 'ROOM_6'
V_nurse_No_Urg_2[1][19] = 'N_BED_7'
V_nurse_No_Urg_2[1][20] = ['NU_Room_13', 'NA', 'NU_Room_46', 'UR_Room_46']
V_nurse_No_Urg_2[2][16] = 'ROOM_4'
V_nurse_No_Urg_2[2][17] = 'N_BED_1'
V_nurse_No_Urg_2[2][18] = 'ROOM_7'
V_nurse_No_Urg_2[2][19] = 'N_BED_6'
V_nurse_No_Urg_2[2][20] = ['NA', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
V_nurse_No_Urg_2[3][16] = 'ROOM_3'
V_nurse_No_Urg_2[3][17] = 'N_BED_2'
V_nurse_No_Urg_2[3][18] = 'ROOM_7'
V_nurse_No_Urg_2[3][19] = 'N_BED_5'
V_nurse_No_Urg_2[3][20] = ['NU_Room_13', 'UR_Room_13', 'NA', 'UR_Room_46']

V_nurse_No_Urg_3[0][16] = 'ROOM_1'
V_nurse_No_Urg_3[0][17] = 'N_BED_3'
V_nurse_No_Urg_3[0][18] = 'ROOM_6'
V_nurse_No_Urg_3[0][19] = 'N_BED_4'
V_nurse_No_Urg_3[0][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
V_nurse_No_Urg_3[1][16] = 'ROOM_2'
V_nurse_No_Urg_3[1][17] = 'N_BED_2'
V_nurse_No_Urg_3[1][18] = 'ROOM_4'
V_nurse_No_Urg_3[1][19] = 'N_BED_6'
V_nurse_No_Urg_3[1][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
V_nurse_No_Urg_3[2][16] = 'ROOM_3'
V_nurse_No_Urg_3[2][17] = 'N_BED_1'
V_nurse_No_Urg_3[2][18] = 'ROOM_5'
V_nurse_No_Urg_3[2][19] = 'N_BED_5'
V_nurse_No_Urg_3[2][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']


# 15 - ?
# 16 - Indication of rooms for Non-Urgent area
# 17 - Indication of bed for Urgent area    

# 18 - Indication of rooms 2 for Non-Urgent area
# 19 - Indication of bed 2 for Urgent area
dr_No_Urg_V_1 = []
dr_No_Urg_V_2 = []
dr_No_Urg_V_3 = []
# for i in range(Dr_NU_s1):
#     dr_No_Urg_V_1.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
#                           UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                           , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                           , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
# for i in range(Dr_NU_s2):
#     dr_No_Urg_V_2.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
#                           UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                           , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                           , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])
# for i in range(Dr_NU_s3):
#     dr_No_Urg_V_3.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
#                           UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
#                           , 'N_ROM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
#                           , 'N_ROM_{}'.format(i+4), 'N_BED_{}'.format(i+4)])

for i in range(Dr_NU_s1):
    dr_No_Urg_V_1.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                          UNDEF])
for i in range(Dr_NU_s2):
    dr_No_Urg_V_2.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                          UNDEF])
for i in range(Dr_NU_s3):
    dr_No_Urg_V_3.append([i, 0, 'dr_NO_URG', 0, 0, UNDEF, 0,
                          UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF
                          , 'ROOM_{}'.format(i+1), 'N_BED_{}'.format(i+1)
                          , 'ROOM_{}'.format(i+4), 'N_BED_{}'.format(i+4),
                          UNDEF])

# Manual placement of rooms and beds
dr_No_Urg_V_1[0][16] = 'ROOM_1'
dr_No_Urg_V_1[0][17] = 'N_BED_4'
dr_No_Urg_V_1[0][18] = 'ROOM_6'
dr_No_Urg_V_1[0][19] = 'N_BED_7'
dr_No_Urg_V_1[0][20] = ['NU_Room_13', 'NA', 'NU_Room_46', 'UR_Room_46']
dr_No_Urg_V_1[1][16] = 'ROOM_2'
dr_No_Urg_V_1[1][17] = 'N_BED_3'
dr_No_Urg_V_1[1][18] = 'ROOM_5'
dr_No_Urg_V_1[1][19] = 'N_BED_7'
dr_No_Urg_V_1[1][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'NA']
dr_No_Urg_V_1[2][16] = 'ROOM_3'
dr_No_Urg_V_1[2][17] = 'N_BED_2'
dr_No_Urg_V_1[2][18] = 'ROOM_7'
dr_No_Urg_V_1[2][19] = 'N_BED_5'
dr_No_Urg_V_1[2][20] = ['NU_Room_13', 'UR_Room_13', 'NA', 'UR_Room_46']
dr_No_Urg_V_1[3][16] = 'ROOM_4'
dr_No_Urg_V_1[3][17] = 'N_BED_1'
dr_No_Urg_V_1[3][18] = 'ROOM_7'
dr_No_Urg_V_1[3][19] = 'N_BED_6'
dr_No_Urg_V_1[3][20] = ['NA', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']

dr_No_Urg_V_2[0][16] = 'ROOM_2'
dr_No_Urg_V_2[0][17] = 'N_BED_3'
dr_No_Urg_V_2[0][18] = 'ROOM_5'
dr_No_Urg_V_2[0][19] = 'N_BED_7'
dr_No_Urg_V_2[0][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'NA']
dr_No_Urg_V_2[1][16] = 'ROOM_1'
dr_No_Urg_V_2[1][17] = 'N_BED_4'
dr_No_Urg_V_2[1][18] = 'ROOM_6'
dr_No_Urg_V_2[1][19] = 'N_BED_7'
dr_No_Urg_V_2[1][20] = ['NU_Room_13', 'NA', 'NU_Room_46', 'UR_Room_46']
dr_No_Urg_V_2[2][16] = 'ROOM_4'
dr_No_Urg_V_2[2][17] = 'N_BED_1'
dr_No_Urg_V_2[2][18] = 'ROOM_7'
dr_No_Urg_V_2[2][19] = 'N_BED_6'
dr_No_Urg_V_2[2][20] = ['NA', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
dr_No_Urg_V_2[3][16] = 'ROOM_3'
dr_No_Urg_V_2[3][17] = 'N_BED_2'
dr_No_Urg_V_2[3][18] = 'ROOM_7'
dr_No_Urg_V_2[3][19] = 'N_BED_5'
dr_No_Urg_V_2[3][20] = ['NU_Room_13', 'UR_Room_13', 'NA', 'UR_Room_46']

dr_No_Urg_V_3[0][16] = 'ROOM_1'
dr_No_Urg_V_3[0][17] = 'N_BED_3'
dr_No_Urg_V_3[0][18] = 'ROOM_6'
dr_No_Urg_V_3[0][19] = 'N_BED_4'
dr_No_Urg_V_3[0][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
dr_No_Urg_V_3[1][16] = 'ROOM_2'
dr_No_Urg_V_3[1][17] = 'N_BED_2'
dr_No_Urg_V_3[1][18] = 'ROOM_4'
dr_No_Urg_V_3[1][19] = 'N_BED_6'
dr_No_Urg_V_3[1][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']
dr_No_Urg_V_3[2][16] = 'ROOM_3'
dr_No_Urg_V_3[2][17] = 'N_BED_1'
dr_No_Urg_V_3[2][18] = 'ROOM_5'
dr_No_Urg_V_3[2][19] = 'N_BED_5'
dr_No_Urg_V_3[2][20] = ['NU_Room_13', 'UR_Room_13', 'NU_Room_46', 'UR_Room_46']




"""                  Worker URGENT
"""
# V_nurse_Urg_1 = []
# V_nurse_Urg_2 = []
# V_nurse_Urg_3 = []
# for i in range(nurs_U_N):
#     V_nurse_Urg_1.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
#     V_nurse_Urg_2.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
#     V_nurse_Urg_3.append([i, 0, 'Nur_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
    
# V_dr_Urg_1 = []
# V_dr_Urg_2 = []
# V_dr_Urg_3 = []
# for i in range(Dr_Ur_N):
#     V_dr_Urg_1.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
#     V_dr_Urg_2.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])
#     V_dr_Urg_3.append([i, 0, 'dr_URG', 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF])



"""                  Worker IMAGING
"""
V_imagin_1 = []
V_imagin_2 = []
V_imagin_3 = []
for i in range(imagi_N):
    V_imagin_1.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    V_imagin_2.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    V_imagin_3.append([i, 0, IMAGI, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])


"""                  Worker LABORATORY
"""
V_labor_1 = []
V_labor_2 = []
V_labor_3 = []
for i in range(labor_N):
    V_labor_1.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    V_labor_2.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    V_labor_3.append([i, 0, LABOR, 0, 0, UNDEF, 0,UNDEF,UNDEF,UNDEF,UNDEF,0,0,0,UNDEF,UNDEF])
    

"""---------------------------------------------------------------------------
        Time of stay per area
        Time according to UMG data - Dr. Blaschke
        
""" 
RECEP_t_1   = [5, 10]          # 5 - 10min 
# TRIAG_U_t_1 = [5, 10]        # 5 - 10min 
t_triage_1  = [5, 10]          # 5 - 10min 
# t_wait_Nu_1 = [10, 60*4]     # 10 - 4h 
# t_wait_Ur_1 = [2, 10]        # 2 - 10 min   # ORANGE
t_Urgent_1  = [60*2, 60*4]     # 2h - 4h 
t_N_Urgen_1 = [60*1, 60*6]     # 4h - 6h 

t_wait_Nu_1 = [30, 60, 120]    # ESI 3: up to 30, ES 4: up to 60, ESI 5: up to 120
t_wait_Ur_1 = [1, 10]          # 2 - 10 min   # ESI ORANGE
"""---------------------------------------------------------------------------
"""    


"""---------------------  ROOMS in ATTENTION NON-URGENT AREA   ----------------
"""
# # ROOM availeable = 1
# # ROOM  occupied  = 0
# #  Init with all rooms availeable
# ATT_NU_ROOM_1 = 1
# ATT_NU_ROOM_2 = 1
# ATT_NU_ROOM_3 = 1



"""---------------------------------------------------------------------------
              
                  PATHOGEN TRANSMISSION PROBABILITY (RISK)
"""
#           Probability based on risk and pathogen transmission
# low = 0.20          # 20% probability
# medium = 0.45       # 45% probability
# high = 0.75         # 75% probability
# very_high = 0.9     # 90% probability

# # Risk per ED area
# PB_RECE = low
# P_TRI_R = medium
# P_TRI_U = high
# P_WAT_N = high   # Outpatients
# P_WAT_U = high   # Urgent patients
# P_N_URE = medium
# PB_URGE = medium
# PB_LABO = low
# PB_IMAG = low
# PB_ARE_test = medium

# # Risk on potential interventions
# ISOLA_R = very_high
# SHOCK_R = very_high
# INVASIV = very_high
# NEGATIV = medium

"""---------------------------------------------------------------------------
""" 

#                   Probabiliies for desitions and flow

Medic_test = 0.5                # confirmed UMG

# Own_Arrive = 0.6                # confirmed UMG
# Suspicion_of_infection = 0.2
# Isolation_needed = 0.2          # confirmed UMG (0.1 - 0.3)
# invasiv_prob = 0.15
# neg_press_prob = 0.15

# Isolation_room = 0            
# Emergen_doct = 1
# Shock_room = 0
# roll_up_wall = 0
# Invasiv_room = 0
# negt_pres_room = 0
# emerg_doctor = 0


"""------------------Seat Map Waiting Area  -----------------------------------
"""
Seat_map = np.zeros((4,10))
Seat_map = Seat_map.astype(int)

"""---------------------------------------------------------------------------
""" 

"""----------------------------------------------------------------------------
                         ARRIVAL TO EMERGENCY
"""

def arrival_method(tim):
    # Time_var = tim
    
    
    # for j in range(Num_Aget):
    for j in range(len(Users)):
        ESI = Users[j][12]
        if color[0] == ESI:         # RED               (NO WAITING)
            Users[j][2] = AT_UR     # ATTENTION URGENT 
            t_Urgent = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[j][3] = t_Urgent
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, t_Urgent)
            
        elif color[1] == ESI:       # ORANGE            (1- 10 MIN WAITING)
            Users[j][2] = WAI_U     # WAITING URGENT 
            t_wait_Ur = random.randint(t_wait_Ur_1[0], t_wait_Ur_1[1])
            Users[j][3] = t_wait_Ur
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, t_wait_Ur)
            
            
        else:                       # YELLOW - GREEN - BLUE 
            Users[j][2] = RECEP     # RECEPTION 
            RECEP_t = random.randint(RECEP_t_1[0], RECEP_t_1[1])
            Users[j][3] = RECEP_t
            Users[j][4] = 0
            # Users[j][6] = random.randint(1, RECEP_t)
        
        
    
    return

"""----------------------------------------------------------------------------
                     FLOW (of users) PER POSSIBLE AREAS OF DEPARTMENT
"""

def area_desit_tree(agent, i):   
#    day = da        
    Curr_Area = agent[2]
    
    if RECEP == Curr_Area:
        Next_Area = TRIAG
        Users[i][2] = Next_Area
        t_triage = random.randint(t_triage_1[0], t_triage_1[1])
        Users[i][3] = t_triage
        Users[i][4] = 0
        # Users[i][6] = random.randint(1, t_triage)
        
    if  TRIAG == Curr_Area:
        Next_Area = WAI_N
        Users[i][2] = Next_Area
        for k in range(len(color_wait)):
            if color_wait[k] == agent[12]:
                # tim = t_wait_Nu_1[k]
                t_wait_Nu = random.randint(2, t_wait_Nu_1[k])
        Users[i][3] = t_wait_Nu
        Users[i][4] = 0
        # Users[i][6] = random.randint(1, t_wait_Nu)    
    
    # if TRIAG_U == Curr_Area:
    #     Next_Area = WAI_U
    #     Users[i][2] = Next_Area
    #     t_wait_Ur = random.randint(t_wait_Ur_1[0], t_wait_Ur_1[1])
    #     Users[i][3] = t_wait_Ur
    #     Users[i][4] = 0
        # Users[i][6] = random.randint(1, t_wait_Ur)
        
    if WAI_U == Curr_Area:
        
        #   ----------   ORIGINAL INIT  -------------------
        # Next_Area = AT_UR  # U_URG
        # Users[i][2] = Next_Area
        # t_Urgent = random.randint(t_Urgent_1[0], t_Urgent_1[1])
        # Users[i][3] = t_Urgent
        # Users[i][4] = 0
        #   ----------   ORIGINAL CLOSE  -------------------
        
        
        #   ----------   DUE TO INTERVENTIONS INIT  -------------------
        #  --  Having three beds in the general urgent area
        if (BEDS_G[0] == 1):
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[0]
            ATT_NU_ROOM_1 = 0
            BEDS_G[0] = ATT_NU_ROOM_1
            # ATT_NU_ROOM_1 = 0
        elif (BEDS_G[1] == 1):
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[1]
            ATT_NU_ROOM_2= 0
            BEDS_G[1] = ATT_NU_ROOM_2
            # ATT_NU_ROOM_2 = 0
        elif BEDS_G[2] == 1:
            Next_Area = AT_UR  # N_URG
            Users[i][2] = Next_Area
            t_N_Urgen = random.randint(t_Urgent_1[0], t_Urgent_1[1])
            Users[i][3] = t_N_Urgen
            Users[i][4] = 0
            Users[i][15] = BEDS_G_NAM[2]
            ATT_NU_ROOM_3 = 0 
            BEDS_G[2] = ATT_NU_ROOM_3
            # ATT_NU_ROOM_3 = 0
        elif (BEDS_G[0] == 0 and BEDS_G[1] == 0 and BEDS_G[2] == 0):
            #  IF all beds occupied, send back to waiting area for N time
            TR_1 = 0
            TR_2 = 0
            TR_3 = 0
            for k in range(len(Users)):
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[0]) ):
                    TR_1 = Users[k][3] - Users[k][4]
                    
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[1] ) ):
                    TR_2 = Users[k][3] - Users[k][4]
                    
                if (( Users[k][2] == 'ATTEN_URGE' ) and
                    (Users[k][15] == BEDS_G_NAM[2] ) ):
                    TR_3 = Users[k][3] - Users[k][4]
                  
            T_new = min(TR_1,TR_2,TR_3)
            if T_new == 0:
                T_new = New_wait_URGT
            Next_Area = WAI_U
            Users[i][2] = Next_Area
            t_wait_Nu = random.randint(1, T_new)
            if color[0] == Users[i][12]:  # ESI in RED, wait up to 5 min
                T_new = New_wait_URGT_RED
                t_wait_Nu = random.randint(1, T_new)
            Users[i][3] = t_wait_Nu
            Users[i][4] = 0

            
        #   ----------   DUE TO INTERVENTIONS CLOSE  -------------------
        
        
    if WAI_N == Curr_Area:
        
        if WAIT_NU_INTRV:
            # print(ATTEN_NU_INTRV)
            # Check room availeability
            
            # ROMS_G_NAM
            # ROMS_G
            # for i in range(len(ROMS_G)):
            
            if (ROMS_G[0] == 1):
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[0]
                ATT_NU_ROOM_1 = 0
                ROMS_G[0] = ATT_NU_ROOM_1
                # ATT_NU_ROOM_1 = 0
            elif (ROMS_G[1] == 1):
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[1]
                ATT_NU_ROOM_2= 0
                ROMS_G[1] = ATT_NU_ROOM_2
                # ATT_NU_ROOM_2 = 0
            elif ROMS_G[2] == 1:
                Next_Area = At_NU  # N_URG
                Users[i][2] = Next_Area
                t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                Users[i][3] = t_N_Urgen
                Users[i][4] = 0
                Users[i][15] = ROMS_G_NAM[2]
                ATT_NU_ROOM_3 = 0 
                ROMS_G[2] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0
            elif (ROMS_G[0] == 0 and ROMS_G[1] == 0 and ROMS_G[2] == 0):
                #  IF all rooms occupied, send back to waiting area for N time
                TR_1 = 0
                TR_2 = 0
                TR_3 = 0
                for k in range(len(Users)):
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[0]) ):
                        TR_1 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[1] ) ):
                        TR_2 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[2] ) ):
                        TR_3 = Users[k][3] - Users[k][4]
                      
                T_new = min(TR_1,TR_2,TR_3)
                if T_new == 0:
                    T_new = 30
                Next_Area = WAI_N
                Users[i][2] = Next_Area
                t_wait_Nu = random.randint(1, T_new)
                Users[i][3] = t_wait_Nu
                Users[i][4] = 0
        else:
            # Next_Area = At_NU  # N_URG
            # Users[i][2] = Next_Area
            # t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
            # Users[i][3] = t_N_Urgen
            # Users[i][4] = 0      
            
            # N_rooms_ = 3
            # N_beds_ = 3
            #  ------------   HERE FOR THE AUTOMATIC ROOMS INIT  ---------
            # for q in range(0, N_rooms_):
            #     if (ROMS_G[q] == 1):
            #         Next_Area = At_NU  # N_URG
            #         Users[i][2] = Next_Area
            #         t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
            #         Users[i][3] = t_N_Urgen
            #         Users[i][4] = 0
            #         Users[i][15] = ROMS_G_NAM[0]
            #         ATT_NU_ROOM_1 = 0
            #         ROMS_G[q] = ATT_NU_ROOM_1
            #  ------------   HERE FOR THE AUTOMATIC ROOMS CLOSE  -------
            
            
            if (np.count_nonzero(ROMS_G) == 0):
                TR_1 = 0
                TR_2 = 0
                TR_3 = 0
                TR_4 = 0
                TR_5 = 0
                TR_6 = 0
                for k in range(len(Users)):
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[0]) ):
                        TR_1 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[1] ) ):
                        TR_2 = Users[k][3] - Users[k][4]
                        
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[2] ) ):
                        TR_3 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[3] ) ):
                        TR_4 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[4] ) ):
                        TR_5 = Users[k][3] - Users[k][4]
                    if (( Users[k][2] == 'ATTE_N_URG' ) and
                        (Users[k][15] == ROMS_G_NAM[5] ) ):
                        TR_6 = Users[k][3] - Users[k][4]
                        
                T_new = min(TR_1,TR_2,TR_3, TR_4,TR_5,TR_6)
                if T_new == 0:     #   Patient can be sent back to waiting area
                    T_new = 30     #   for the next availeable time room or up to 30 min
                Next_Area = WAI_N
                Users[i][2] = Next_Area
                t_wait_Nu = random.randint(1, T_new)
                Users[i][3] = t_wait_Nu
                Users[i][4] = 0
                
            else:
                # for k in range(0,len(ROMS_G)):
                #     if (ROMS_G[k] == 1):
                #         Next_Area = At_NU  # N_URG
                #         Users[i][2] = Next_Area
                #         t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                #         Users[i][3] = t_N_Urgen
                #         Users[i][4] = 0
                #         Users[i][15] = ROMS_G_NAM[k]
                #         ATT_NU_ROOM_1 = 0
                #         ROMS_G[k] = ATT_NU_ROOM_1
                
                if (ROMS_G[0] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[0]
                    ATT_NU_ROOM_1 = 0
                    ROMS_G[0] = ATT_NU_ROOM_1
                    
                elif (ROMS_G[1] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[1]
                    ATT_NU_ROOM_2= 0
                    ROMS_G[1] = ATT_NU_ROOM_2
                    # ATT_NU_ROOM_2 = 0
                elif ROMS_G[2] == 1:
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[2]
                    ATT_NU_ROOM_3 = 0 
                    ROMS_G[2] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0
                
                elif (ROMS_G[3] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[3]
                    ATT_NU_ROOM_1 = 0
                    ROMS_G[3] = ATT_NU_ROOM_1
                    
                elif (ROMS_G[4] == 1):
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[4]
                    ATT_NU_ROOM_2 = 0
                    ROMS_G[4] = ATT_NU_ROOM_2
                    # ATT_NU_ROOM_2 = 0
                elif ROMS_G[5] == 1:
                    Next_Area = At_NU  # N_URG
                    Users[i][2] = Next_Area
                    t_N_Urgen = random.randint(t_N_Urgen_1[0], t_N_Urgen_1[1])
                    Users[i][3] = t_N_Urgen
                    Users[i][4] = 0
                    Users[i][15] = ROMS_G_NAM[5]
                    ATT_NU_ROOM_3 = 0 
                    ROMS_G[5] = ATT_NU_ROOM_3
                # ATT_NU_ROOM_3 = 0
                
            # elif (ROMS_G[0] == 0 and ROMS_G[1] == 0 and ROMS_G[2] == 0):
            #     #  IF all rooms occupied, send back to waiting area for N time
            #     TR_1 = 0
            #     TR_2 = 0
            #     TR_3 = 0
            #     for k in range(len(Users)):
            #         if (( Users[k][2] == 'ATTE_N_URG' ) and
            #             (Users[k][15] == ROMS_G_NAM[0]) ):
            #             TR_1 = Users[k][3] - Users[k][4]
                        
            #         if (( Users[k][2] == 'ATTE_N_URG' ) and
            #             (Users[k][15] == ROMS_G_NAM[1] ) ):
            #             TR_2 = Users[k][3] - Users[k][4]
                        
            #         if (( Users[k][2] == 'ATTE_N_URG' ) and
            #             (Users[k][15] == ROMS_G_NAM[2] ) ):
            #             TR_3 = Users[k][3] - Users[k][4]
                      
            #     T_new = min(TR_1,TR_2,TR_3)
            #     if T_new == 0:     #   Patient can be sent back to waiting area
            #         T_new = 30     #   for the next availeable time room or up to 30 min
            #     Next_Area = WAI_N
            #     Users[i][2] = Next_Area
            #     t_wait_Nu = random.randint(1, T_new)
            #     Users[i][3] = t_wait_Nu
            #     Users[i][4] = 0
        
    
#------------------------------------------------------------------------------    
      # To unseat patient once in attention services
#        ind = [(index, row.index(Users[i][0])) for index, row in enumerate(Seat_map) if (Users[i][0]) in row]
        # ind = np.where(Seat_map == Users[i][0])
        # Seat_map[ind[0], ind[1]] = 0
#------------------------------------------------------------------------------    

    if (At_NU == Curr_Area or AT_UR == Curr_Area or IMAGI == Curr_Area or 
                                           LABOR == Curr_Area):
        
        # if ATTEN_NU_INTRV:
        #     # print(ATTEN_NU_INTRV)
        #     if ( Users[i][15] != UNDEF ):
        #         if ( Users[i][15] == ROMS_G_NAM[0] ):
        #             ATT_NU_ROOM_1 = 1
        #             ROMS_G[0] = ATT_NU_ROOM_1
        #         if ( Users[i][15] == ROMS_G_NAM[1] ):
        #             ATT_NU_ROOM_2 = 1
        #             ROMS_G[1] = ATT_NU_ROOM_2
        #         if ( Users[i][15] == ROMS_G_NAM[2] ):
        #             ATT_NU_ROOM_3 = 1
        #             ROMS_G[2] = ATT_NU_ROOM_3
            
        #     Next_Area = EXIT_
        #     Users[i][2] = Next_Area
        #     # t_N_Urgen = random.randint(40, 2*60)
        #     Users[i][3] = 0
        #     Users[i][4] = 0
        
        # else:
            
            
        # -------   ATTENTION NON-URGENT  INIT ------------------
        if ( Users[i][15] != UNDEF ):
            if ( Users[i][15] == ROMS_G_NAM[0] ):
                ATT_NU_ROOM_1 = 1
                ROMS_G[0] = ATT_NU_ROOM_1
            if ( Users[i][15] == ROMS_G_NAM[1] ):
                ATT_NU_ROOM_2 = 1
                ROMS_G[1] = ATT_NU_ROOM_2
            if ( Users[i][15] == ROMS_G_NAM[2] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[2] = ATT_NU_ROOM_3
            
            if ( Users[i][15] == ROMS_G_NAM[3] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[3] = ATT_NU_ROOM_3
            if ( Users[i][15] == ROMS_G_NAM[4] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[4] = ATT_NU_ROOM_3
            if ( Users[i][15] == ROMS_G_NAM[5] ):
                ATT_NU_ROOM_3 = 1
                ROMS_G[5] = ATT_NU_ROOM_3
            
        # -------   ATTENTION NON-URGENT  CLOSE ------------------
        
        # -------   ATTENTION   URGENT  INIT ------------------
        if ( Users[i][15] != UNDEF ):
            if ( Users[i][15] == BEDS_G_NAM[0] ):
                ATT_NU_ROOM_1 = 1
                BEDS_G[0] = ATT_NU_ROOM_1
            if ( Users[i][15] == BEDS_G_NAM[1] ):
                ATT_NU_ROOM_2 = 1
                BEDS_G[1] = ATT_NU_ROOM_2
            if ( Users[i][15] == BEDS_G_NAM[2] ):
                ATT_NU_ROOM_3 = 1
                BEDS_G[2] = ATT_NU_ROOM_3
            if ( Users[i][15] == BEDS_G_NAM[3] ):
                ATT_NU_ROOM_4 = 1
                BEDS_G[3] = ATT_NU_ROOM_4
            if ( Users[i][15] == BEDS_G_NAM[4] ):
                ATT_NU_ROOM_5 = 1
                BEDS_G[4] = ATT_NU_ROOM_5
            if ( Users[i][15] == BEDS_G_NAM[5] ):
                ATT_NU_ROOM_6 = 1
                BEDS_G[5] = ATT_NU_ROOM_6
        # -------   ATTENTION   URGENT  CLOSE ------------------
        
        Next_Area = EXIT_
        Users[i][2] = Next_Area
        # t_N_Urgen = random.randint(40, 2*60)
        Users[i][3] = 0
        Users[i][4] = 0
    
    return agent

"""----------------------------------------------------------------------------
                           ROUTINE SHIFT 1
"""             
def action_desit_tree(agent, i, da, currt_time):    
    Curr_Area = agent[2]
    day_current = da     
    # interact_event = agent[6]
    # current_time = agent[4]
        
    if RECEP == Curr_Area:
        # FAR - FIELD
        # Sucep patient
        #   1- Check for the number of other suscp or infect in the room, 
        #      PAT and HCWs
        #   2- if infected in the room - 
        #       -Check for the FF interaction time, the area time (agent[3])
        #       -Checks the TP for that area time, since previously known the
        #        time of other infectious ocupants
        #   3- if TP TRUE - starts infection status
        #       agent[9] = Curr_Area           (area)
        #       agent[10] = day_current + 1    (day of infection)
        #       agent[11] = PATIEN+'_RECEPTION', (if (N_of(P_inf) > 
        #                   N_of(H_inf)) (WHO?)
        #
        # Infected patient
        #   1- Checks the TP for the area time for the interaction with HCWs
        #   2- if TP TRUE - starts infection status for HCWs in the area
        #

        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and 
                        (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s1):
                    if V_recep_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_1[i])
                    elif V_recep_1[i][1] == 0:
                        H_sus.append(V_recep_1[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, infected]*TP_pyth
                    # TP = TP * Recep_fact
                    
                    TP = TP * TP_Farf_Recep
                    
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff1_RECEPTION'
            
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                # TP = TP * Recep_fact
                
                TP = TP * TP_Farf_Recep
                
                for i in range(len(V_recep_1)):
                    if V_recep_1[i][1] == 0 and V_recep_1[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_1[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_1[i][6] = day_current + 1 
                            V_recep_1[i][5] = PATIEN +'_RECEPTION'
                            
            
            #------------    NEAR FIELD  RECEP  INIT  ---------------------
            Sucep_Area = []
            
            if agent[1] == 1:
                #              Patient-HCW
                SUS = random.randint(0, (len(V_recep_1))-1 )
                
                # if len(V_nurse_No_Urg_1) == 1:
                #         SUS = 0
                # else:
                #     SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )

                if V_recep_1[SUS][1] == 0 and V_recep_1[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_Recep * Pat_hcw_recep
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_recep_1[SUS][3] = day_current + 1
                        V_recep_1[SUS][5] = PATIEN+'_RECEPTION'
                        V_recep_1[SUS][6] = day_current + 1 
                
            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_recep_1))-1 )

            # Infected Nurse
            if V_recep_1[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_Recep * Pat_hcw_recep
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff1_RECEPTION'
            # ----------    NEAR FIELD  RECEP  CLOSE     -----------------

            # run fomite function once when entering area
            HCW_pool = V_recep_1 #[V_recep_1[0], V_recep_1[1], V_recep_1[2]]
            fomite_function(HCW_pool, RECEP)

        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s2):
                    if V_recep_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_2[i])
                    elif V_recep_2[i][1] == 0:
                        H_sus.append(V_recep_2[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, infected]*TP_pyth
                    # TP = TP * Recep_fact
                    
                    TP = TP * TP_Farf_Recep
                    
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff2_RECEPTION" 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff2_RECEPTION'
                
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                # TP = TP * Recep_fact
                
                TP = TP * TP_Farf_Recep
                
                for i in range(len(V_recep_2)):
                    if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_2[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_2[i][6] = day_current + 1 
                            if agent[1] == 1:
                                V_recep_2[i][5] = PATIEN +'_RECEPTION'
                                
            #------------    NEAR FIELD  RECEP  INIT  ---------------------
#
            Sucep_Area = []
            
            if agent[1] == 1:
                #              Patient-HCW
                
                
                
                SUS = random.randint(0, (len(V_recep_2))-1 )
                
                # if len(V_nurse_No_Urg_1) == 1:
                #         SUS = 0
                # else:
                #     SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )

                if V_recep_2[SUS][1] == 0 and V_recep_2[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_Recep * Pat_hcw_recep
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_recep_2[SUS][3] = day_current + 1
                        V_recep_2[SUS][5] = PATIEN+'_RECEPTION'
                        V_recep_2[SUS][6] = day_current + 1 
                

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_recep_2))-1 )

            # Infected Nurse
            if V_recep_2[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_Recep * Pat_hcw_recep
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff2_RECEPTION'
            # ----------    NEAR FIELD  RECEP  CLOSE     -----------------
            
            # run fomite function once when entering area
            HCW_pool = V_recep_2 #[V_recep_2[0], V_recep_2[1]]
            fomite_function(HCW_pool, RECEP)
     
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
        
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            P_inf = []
            P_sus = []
            H_inf = []
            H_sus = []
            
            if (agent[1] == 0):
                for i in range(len(Users)):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='RECEPTION')):
                        if(Users[i][1] == 1):
                            cont_inf = cont_inf + 1
                            P_inf.append(Users[i])
                        if(Users[i][1] == 0):  
                            cont_tot = cont_tot + 1
                            P_sus.append(Users[i])
     
                for i in range(recep_N_s3):
                    if V_recep_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                        H_inf.append(V_recep_3[i])
                    elif V_recep_3[i][1] == 0:
                        H_sus.append(V_recep_3[i])
                        
                # infected = cont_inf + cont_inf_HCW
                infected = len(P_inf) + len(H_inf)
                
                if infected > 0:
                    times_P = []
                    times_H = []
                    time_pat = 0
                    time_hcw = 0
                    A1 = Tr_Pr['1_Reception'].loc[:,'m']
                    # diff = np.absolute(A1 - exp_time)
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    TP = Tr_Pr['1_Reception'].loc[index, infected]*TP_pyth
                    # TP = TP * Recep_fact
                    
                    TP = TP * TP_Farf_Recep
                    
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        if (len(P_inf) > len(H_inf)):
                            agent[11] = PATIEN +'_RECEPTION'
                        elif (len(H_inf) >= len(P_inf)):
                            agent[11] = 'Staff3_RECEPTION'
            
            if (agent[1] == 1):   
                
                A1 = Tr_Pr['1_Reception'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['1_Reception'].loc[index, 
                                                  1]*TP_pyth
                # TP = TP * Recep_fact
                
                TP = TP * TP_Farf_Recep
                
                for i in range(len(V_recep_3)):
                    if V_recep_3[i][1] == 0 and V_recep_3[i][6] == 0:
                        Trnasmiss = random.random() < TP   
                        if (Trnasmiss):
                            V_recep_3[i][3] = day_current + 1 
                            # V_recep_2[i][5] = PATIEN + '_RECEPTION'
                            V_recep_3[i][6] = day_current + 1 
                            V_recep_3[i][5] = PATIEN +'_RECEPTION'

            #------------    NEAR FIELD  RECEP  INIT  ---------------------
            Sucep_Area = []
            
            if agent[1] == 1:
                #              Patient-HCW
                SUS = random.randint(0, (len(V_recep_3))-1 )
                
                # if len(V_nurse_No_Urg_1) == 1:
                #         SUS = 0
                # else:
                #     SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )

                if V_recep_3[SUS][1] == 0 and V_recep_3[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_Recep * Pat_hcw_recep
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_recep_3[SUS][3] = day_current + 1
                        V_recep_3[SUS][5] = PATIEN+'_RECEPTION'
                        V_recep_3[SUS][6] = day_current + 1 
                

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_recep_3))-1 )

            # Infected Nurse
            if V_recep_3[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_Recep * Pat_hcw_recep
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff3_RECEPTION'
            # ----------    NEAR FIELD  RECEP  CLOSE     -----------------
                
            # run fomite function once when entering area
            HCW_pool = V_recep_3 #[V_recep_3[0]]
            fomite_function(HCW_pool, RECEP)
    
    if TRIAG == Curr_Area:
# FAR - FIELD
# Sucep patient
#   1- Check for the number of other suscp or infect in the room, PAT and HCWs
#   2- if infected in the room - 
#       -Check for the FF interaction time, the area time (agent[3])
#       -Checks the TP for that area time, since previously known the time of
#        other infectious ocupants
#   3- if TP TRUE - starts infection status
#       agent[9] = Curr_Area           (area)
#       agent[10] = day_current + 1    (day of infection)
#       agent[11] = PATIEN+'_RECEPTION', (if (N_of(P_inf) > N_of(H_inf)) (WHO?)
#
# Infected patient
#   1- Checks the TP for the area time for the interaction with HCWs
#   2- if TP TRUE - starts infection status for HCWs in the area
#

        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s1):
                if V_triag_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, infected]*TP_pyth
                # TP = TP * Triag_fact
                
                TP = TP * TP_Farf_Triag
                
                for i in range(triag_N_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_1[i][1] == 0 and V_triag_1[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_triag_1[i][3] = day_current + 1 
                            # V_triag_1[i][5] = PATIEN+'_TRIAGE'
                            V_triag_1[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_1[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_1[i][5] = 'Staff1_TRIAGE'
                            
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff1_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff1_TRIAGE'
            
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s2):
                if V_triag_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, infected]*TP_pyth
                # TP = TP * Triag_fact
                
                TP = TP * TP_Farf_Triag
                
                for i in range(triag_N_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_2[i][1] == 0 and V_triag_2[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_triag_2[i][3] = day_current + 1 
                            V_triag_2[i][5] = PATIEN +'_TRIAGE'
                            V_triag_2[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_2[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_2[i][5] = 'Staff2_TRIAGE'
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff2_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff2_TRIAGE'
            
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
            
            cont_tot = 0
            cont_inf = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
 
            for i in range(triag_N_s3):
                if V_triag_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = cont_inf + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['2_Triage'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                TP = Tr_Pr['2_Triage'].loc[index, 
                                           infected]*TP_pyth
                # TP = TP * Triag_fact
                
                TP = TP * TP_Farf_Triag
                
                for i in range(triag_N_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and (cont_inf != 0 or cont_inf_HCW != 0)):
                        if V_triag_3[i][1] == 0 and V_triag_3[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_triag_3[i][3] = day_current + 1 
                            V_triag_3[i][5] = PATIEN +'_TRIAGE'
                            V_triag_3[i][6] = day_current + 1 
                            if cont_inf > cont_inf_HCW:
                                V_triag_3[i][5] = PATIEN +'_TRIAGE'
                            elif cont_inf_HCW >= cont_inf:
                                V_triag_3[i][5] = 'Staff3_TRIAGE'
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='TRIAGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff3_TRIAGE"
                    if cont_inf > cont_inf_HCW:
                        agent[11] = PATIEN +'_RECEPTION'
                    elif cont_inf_HCW >= cont_inf:
                        agent[11] = 'Staff3_TRIAGE'         
            

    if WAI_U == Curr_Area:
        
# FAR - FIELD
# Sucep patient
#   1- Check for the number of other suscp or infect in the room, PAT 
#   2- if infected in the room - 
#       -Check for the FF interaction time, the area time (agent[3])
#       -Checks the TP for that area time, since previously known the time of
#        other infectious ocupants
#   3- if TP TRUE - starts infection status
#       agent[9] = Curr_Area           (area)
#       agent[10] = day_current + 1    (day of infection)
#       agent[11] = (WHO?)
#
# Infected patient
#   1- Checks the TP for the area time for the interaction with all other PAt 
#       in the area
#   2- if TP TRUE - starts infection status for PATs in the area
#
        cont_tot = 0
        cont_inf = 0

        for i in range(len(Users)):
            if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_URGENT'):
                cont_tot = cont_tot + 1
                if(Users[i][1] == 1):
                    cont_inf = cont_inf + 1
        infected = cont_inf 
        
        if infected > 0:
            A1 = Tr_Pr['4_Wait_Urg_Flur'].loc[:,'m']
            diff = np.absolute(A1 - agent[3])
            index = diff.argmin()
            TP = Tr_Pr['4_Wait_Urg_Flur'].loc[index, infected]*TP_pyth
            # Ext_waitU = 300
            # TP = TP * WaitU_fact*Ext_waitU*HEAD_wait_U
            
            TP = TP * TP_Farf_WaitU
            
            # TP = TP*100
    
            # for i in range(len(Users)):
            #     if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_URGENT'):
            Trnasmiss = random.random() < TP     
            if Trnasmiss and (agent[1] == 0):
                agent[1] = 2
                agent[9] = Curr_Area
                agent[10] = day_current + 1 
                agent[11] = "WAIT_URGENT"
            
            for i in range(len(Users)):
                if( (Users[i][5] < currt_time) and 
                   (Users[i][2] =='WAIT_URGENT') and
                    (Users[i] != agent) and
                    (Users[i][1] == 0) ):
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 1):
                        Users[i][1] = 2
                        Users[i][9] = Curr_Area
                        Users[i][10] = day_current + 1 
                        Users[i][11] = "WAIT_URGENT"

    
    if WAI_N == Curr_Area:
# FAR - FIELD
# Sucep patient
#   1- Check for the number of other suscp or infect in the room, PAT 
#   2- if infected in the room - 
#       -Check for the FF interaction time, the area time (agent[3])
#       -Checks the TP for that area time, since previously known the time of
#        other infectious ocupants
#   3- if TP TRUE - starts infection status
#       agent[9] = Curr_Area           (area)
#       agent[10] = day_current + 1    (day of infection)
#       agent[11] = (WHO?)
#
# Infected patient
#   1- Checks the TP for the area time for the interaction with all other PAt 
#       in the area
#   2- if TP TRUE - starts infection status for PATs in the area
#
# NEAR-FIELD
#   Infected PAT
#   1- Search for suscp PAT (random selected) - estimate interaction time for NF TP
#       - if TP TRUE, suscep starts infect status
#
# ----------------------- INTERVENTIONS ---------------------------------
# Intervention in waiting area - WAITING NON URGENT SPLIT
# Base case: patients come to the general waiting room area and interact there
# following the TP in 3_Wait_NoN
# 
# Intervent: patients are randomly accomodated in one of two rooms, they interact
# there with the TP 10_WAIT_INTRV, and two major levels are 
# applied - WAT_ROM_1 or WAT_ROM_2
# For the counting, both continue as WAIT_NO_URGENT

        if WAIT_NU_INTRV:
            # print(WAIT_NU_INTRV)
            
            #               SETTING FOR  WAT_ROM_1 
            #  --------  FAR FIELD  WAI_N ROOM 1  INIT  --------
            cont_tot = 0
            cont_inf = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='WAIT_NO_URGENT') and 
                    (Users[i][13] =='WAT_ROM_1') ):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            if infected > 0:
                # A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
                A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                # TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
                TP = Tr_Pr['10_WAIT_INTRV'].loc[index, infected]*TP_pyth * Wait_intrv_fact

                # TP = TP * WaitN_fact
                
                TP = TP * TP_Farf_WaiNU_INT
                

                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_NO_URGENT'):
                Trnasmiss = random.random() < TP     
                if (Trnasmiss and (agent[1] == 0) and  
                    (agent[13] =='WAT_ROM_1')):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = "WAIT_NO_URGENT"
                    # print(WAIT_NU_INTRV)
                
                # for i in range(len(Users)):
                #     if( (Users[i][5] < currt_time) and 
                #        (Users[i][2] =='WAIT_NO_URGENT') and
                #         (Users[i] != agent) and
                #         (Users[i][1] == 0) and
                #         (Users[i][13] == 'WAT_ROM_1')):
                #         Trnasmiss = random.random() < TP 
                #         if Trnasmiss and (agent[1] == 1):
                #             Users[i][1] = 2
                #             Users[i][9] = Curr_Area
                #             Users[i][10] = day_current + 1 
                #             Users[i][11] = "WAIT_NO_URGENT"
                            # print(WAIT_NU_INTRV)
            #  ----------  FAR FIELD  WAI_N ROOM 1  CLOSE  --------
            #------------    NEAR FIELD  WAI_N ROOM 1  INIT  -----------------
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0) and
                        (Users[i][13] == 'WAT_ROM_1')):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                    # TP = TP* WaitN_fact
                    TP = TP_Near_WaiNU_INT * Pat_pat_waitg
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(WAIT_NU_INTRV)
                        # print(Sucep_Area[SUS])
            
            #------------    NEAR FIELD  WAI_N ROOM 1  CLOSE ---------------------
            
            #               SETTING FOR  WAT_ROM_2 
            #  --------  FAR FIELD  WAI_N ROOM 2  INIT  --------
            cont_tot = 0
            cont_inf = 0
            for i in range(len(Users)):
                if ((Users[i][5] < currt_time) and 
                    (Users[i][2] =='WAIT_NO_URGENT') and 
                    (Users[i][13] =='WAT_ROM_2') ):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            if infected > 0:
                # A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
                A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                # TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
                TP = Tr_Pr['10_WAIT_INTRV'].loc[index, infected]*TP_pyth*Wait_intrv_fact
                # TP = TP * WaitN_fact
                
                TP = TP * TP_Farf_WaiNU_INT
                
                # TP = TP*300
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_NO_URGENT'):
                Trnasmiss = random.random() < TP     
                # if Trnasmiss and (agent[1] == 0):
                if (Trnasmiss and (agent[1] == 0) and  
                    (agent[13] =='WAT_ROM_2')):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = "WAIT_NO_URGENT"
                    # print(WAIT_NU_INTRV)
                
                # for i in range(len(Users)):
                #     if( (Users[i][5] < currt_time) and 
                #        (Users[i][2] =='WAIT_NO_URGENT') and
                #         (Users[i] != agent) and
                #         (Users[i][1] == 0) and
                #         (Users[i][13] == 'WAT_ROM_2')):
                #         Trnasmiss = random.random() < TP 
                #         if Trnasmiss and (agent[1] == 1):
                #             Users[i][1] = 2
                #             Users[i][9] = Curr_Area
                #             Users[i][10] = day_current + 1 
                #             Users[i][11] = "WAIT_NO_URGENT"
                            # print(WAIT_NU_INTRV)
            #  ----------  FAR FIELD  WAI_N ROOM 2  CLOSE  --------
            
            #------------    NEAR FIELD  WAI_N ROOM 2  INIT  -----------------
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0) and
                        (Users[i][13] == 'WAT_ROM_2')):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                    # TP = TP* WaitN_fact
                    TP = TP_Near_WaiNU_INT * Pat_pat_waitg
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(WAIT_NU_INTRV)
                        # print(Sucep_Area[SUS])
                        
            #------------    NEAR FIELD  WAI_N ROOM 2  CLOSE ------------------   
            
            #------------    FOMITES  WAI_N INTERVENTION ----------------------
            # run fomite function once when entering area
            # # in no defined separate rooms
            # HCW_pool = []
            # fomite_function(HCW_pool, Curr_Area, Fomite, 0.5)
            
            # if defined separate rooms
            fomite_function_WAI(WAI_N)            
            #------------    FOMITES  WAI_N INTERVENTION End ------------------
            
        else:
            cont_tot = 0
            cont_inf = 0
    
            for i in range(len(Users)):
                if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_NO_URGENT'):
                    cont_tot = cont_tot + 1
                    if(Users[i][1] == 1):
                        cont_inf = cont_inf + 1
            infected = cont_inf 
            
            # if infected > 0:
            #     A1 = Tr_Pr['3_Wait_NoN'].loc[:,'m']
            #     # A1 = Tr_Pr['10_WAIT_INTRV'].loc[:,'m']
                
            #     diff = np.absolute(A1 - agent[3])
            #     index = diff.argmin()
            #     TP = Tr_Pr['3_Wait_NoN'].loc[index, infected]*TP_pyth
            #     # TP = Tr_Pr['10_WAIT_INTRV'].loc[index, infected]*TP_pyth*Wait_intrv_fact
            #     # TP = TP*HEAD_wait_NU
            #     # TP = TP * WaitN_fact
            #     # TP = TP*300
            #     # for i in range(len(Users)):
            #     #     if (Users[i][5] < currt_time) and (Users[i][2] =='WAIT_NO_URGENT'):
                
            #     TP = TP * TP_Farf_WaiNU
                
            #     Trnasmiss = random.random() < TP     
            #     if Trnasmiss and (agent[1] == 0):
            #         agent[1] = 2
            #         agent[9] = Curr_Area
            #         agent[10] = day_current + 1 
            #         agent[11] = "WAIT_NO_URGENT"
                
            #     for i in range(len(Users)):
            #         if( (Users[i][5] < currt_time) and 
            #            (Users[i][2] =='WAIT_NO_URGENT') and
            #             (Users[i] != agent) and
            #             (Users[i][1] == 0) ):
            #             Trnasmiss = random.random() < TP 
            #             if Trnasmiss and (agent[1] == 1):
            #                 Users[i][1] = 2
            #                 Users[i][9] = Curr_Area
            #                 Users[i][10] = day_current + 1 
            #                 Users[i][11] = "WAIT_NO_URGENT"
            
            
            #------------    NEAR FIELD  WAI_N  INIT  ---------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='WAIT_NO_URGENT') and
                       (Users[i][1] == 0)):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                    # TP = TP * WaitN_fact
                    TP = TP_Near_WaiNU * Pat_pat_waitg
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = "WAIT_NO_URGENT"   
                        # print(Sucep_Area[SUS])
            
            #------------    NEAR FIELD  WAI_N  CLOSE ---------------------
            
            #------------    FOMITES WAI_N ------------------------------------
            # run fomite function once when entering area
            # HCW_pool = []
            # foms_WAI = range(0, number_chairs_holding)
            fomite_function_WAI(WAI_N) #, foms_WAI)
            # fomite_function(HCW_pool, Curr_Area)
            #------------    FOMITES WAI_N END --------------------------------
            

    if AT_UR == Curr_Area:
        # -------------------------- TRANSMIS PROBABILITY TOP -------------------------
        # FAR - FIELD
        # Here, we look for the total of infected in the room (PAT, NUR or DR), and based
        # on that total, we take the FF TP and apply for any suscpt (PAT, NUR or DR)
        #   1- Check if any infect in the room, PAT, NUR, DR, besides the entering one
        #   2- if infected in the room - FF interaction time, the area time (agent[3])
        #   3- FOR PAT
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   4- FOR NURSE
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   5- FOR DR
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   6- If necesary, sends to additional test - LAB or IMAG
        #       - calls function (time, agent, curr time)     
        #
        # NEAR-FIELD
        #   Infected PAT
        #   1- Search for suscp PAT (random selected) - estimate interaction time for NF TP
        #       - if TP TRUE, suscep starts infect status
        #   2- Search for NUR (rand select) - interact time NF proportion
        #       - if TP TRUE, suscep starts infect status for NUR
        #   3- Search for DR (rand select) - interact time NF proportion
        #       - if TP TRUE, suscep starts infect status for DR
        #
        #  Infected HCW
        #   1- search for a NUR and DR (rand)
        #   2- if NUR or DR infcted - interact time NF proportion (NUR or DR time)
        #   3- NF TP for proport of time - if TP TRUE
        #       - if TP TRUE, suscep starts infect status for PAT
        #  
        # -------------------------- TRANSMIS PROBABILITY BOTTOM-----------------------


        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ) ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ) ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2

            # cont_tot = 0
            # cont_inf = 0
            # infected = 0
            # # cont_tot_HCW = 0
            # cont_inf_HCW = 0
            # for i in range(len(Users)):
            #     # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE'):
            #     if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE')
            #             and (Users[i][15] != UNDEF ) ):
            #         cont_tot = cont_tot + 1
            #         if(Users[i][1] == 1):
            #             cont_inf = cont_inf + 1
 
            for i in range(nur_NU_N_s1):
                if V_nurse_No_Urg_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s1):
                if dr_No_Urg_V_1[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, 
                                               infected]*TP_pyth
                # TP = TP * Att_U_fact * HEAD_Att_U
                # TP = TP*Att_interv
                
                TP = TP * TP_Farf_At_Ur
                
                for i in range(nur_NU_N_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_nurse_No_Urg_1[i][3] = day_current + 1 
                            # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                            V_nurse_No_Urg_1[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_1[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_1[i][5] = 'Staff1_ATTEN_URGE'
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff1_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    if cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff1_ATTEN_URGE'
                            
                
                for i in range(Dr_NU_s1):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            dr_No_Urg_V_1[i][3] = day_current + 1 
                            # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_1[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_1[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_1[i][5] = 'Staff1_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)

            

            #------------    NEAR FIELD  ATTEN_URGE  INIT  ---------------------
          
            Sucep_Area = []
            # ------- Infected PAT, PAT - PAT Interact
            if agent[1] == 1:
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                
                # for i in range(len(Users)):
                #     if((Users[i][5] < currt_time) and 
                #        (Users[i][2] =='ATTEN_URGE') and
                #        (Users[i][1] == 0)):
                #         Sucep_Area.append(Users[i])
                # if len(Sucep_Area) != 0:
                #     if len(Sucep_Area) == 1:
                #         SUS = 0
                #     else:
                #         SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                   Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_pat_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_1) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )

                if V_nurse_No_Urg_1[SUS][1] == 0 and V_nurse_No_Urg_1[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_1[SUS][3] = day_current + 1
                        V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_1[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_1) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_1))-1 )

                if dr_No_Urg_V_1[SUS][1] == 0 and dr_No_Urg_V_1[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_1[SUS][3] = day_current + 1
                        dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_1[SUS][6] = day_current + 1             

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_1[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff1_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_1[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff1_ATTEN_URGE'     
               # -------------------------------------------------------------

            #------------    NEAR FIELD  ATTEN_URGE  CLOSE ---------------------    
        
    
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ) ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ) ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2
 
            for i in range(nur_NU_N_s2):
                if V_nurse_No_Urg_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s2):
                if dr_No_Urg_V_2[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, infected]*TP_pyth
                # TP = TP * Att_U_fact * HEAD_Att_U
                # TP = TP*Att_interv
                
                TP = TP * TP_Farf_At_Ur
                
                for i in range(nur_NU_N_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_nurse_No_Urg_2[i][3] = day_current + 1 
                            V_nurse_No_Urg_2[i][5] = PATIEN+'_ATTEN_URGE'
                            V_nurse_No_Urg_2[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_2[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_2[i][5] = 'Staff2_ATTEN_URGE'
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff2_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    if cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff2_ATTEN_URGE'
                            
                
                for i in range(Dr_NU_s2):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            dr_No_Urg_V_2[i][3] = day_current + 1 
                            dr_No_Urg_V_2[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_2[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_2[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_2[i][5] = 'Staff2_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)    

            #------------    NEAR FIELD  ATTEN_URGE  INIT  ---------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_pat_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_2) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_2))-1 )

                if V_nurse_No_Urg_2[SUS][1] == 0 and V_nurse_No_Urg_2[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_2[SUS][3] = day_current + 1
                        V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_2) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )

                if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_2[SUS][3] = day_current + 1
                        dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_2[SUS][6] = day_current + 1 

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_2[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff2_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_2[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff2_ATTEN_URGE'     
            # -------------------------------------------------------------  



            #------------    NEAR FIELD  ATTEN_URGE  CLOSE ---------------------
            
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
            
            cont_tot = 0
            cont_inf = 0
            cont_inf_2 = 0
            PAT_1 = 0
            PAT_2 = 0
            infected = 0
            # cont_tot_HCW = 0
            cont_inf_HCW = 0
            for i in range(len(Users)):
                # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE')
                    and (Users[i][15] != UNDEF ) ):
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_1') or 
                        (Users[i][15] == 'BEDS_2') or 
                        (Users[i][15] == 'BEDS_3') ) ):
                        cont_inf = cont_inf + 1
                    if ((Users[i][1] == 1) and 
                        ((Users[i][15] == 'BEDS_4') or 
                        (Users[i][15] == 'BEDS_5') or 
                        (Users[i][15] == 'BEDS_6') ) ):
                        cont_inf_2 = cont_inf_2 + 1

            PAT_1 = cont_inf
            PAT_2 = cont_inf_2
 
            for i in range(nur_NU_N_s3):
                if V_nurse_No_Urg_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
            for i in range(Dr_NU_s3):
                if dr_No_Urg_V_3[i][1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
    
            infected = (cont_inf + cont_inf_2) + cont_inf_HCW
            
            if infected > 0:
                A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
                diff = np.absolute(A1 - agent[3])
                index = diff.argmin()
                if infected > 5:
                    infected = 5
                TP = Tr_Pr['6_Atte_Urg_1'].loc[index, infected]*TP_pyth
                # TP = TP * Att_U_fact * HEAD_Att_U
                # TP = TP*Att_interv
                
                TP = TP * TP_Farf_At_Ur
                
                for i in range(nur_NU_N_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            V_nurse_No_Urg_3[i][3] = day_current + 1 
                            V_nurse_No_Urg_3[i][5] = PATIEN+'_ATTEN_URGE'
                            V_nurse_No_Urg_3[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                V_nurse_No_Urg_3[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                V_nurse_No_Urg_3[i][5] = 'Staff3_ATTEN_URGE'
                
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTEN_URGE'):
                Trnasmiss = random.random() < TP     
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    # agent[11] = "Staff3_ATTEN_URGE"
                    if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                        agent[11] = PATIEN +'_ATTEN_URGE'
                    elif cont_inf_HCW > (cont_inf + cont_inf_2):
                        agent[11] = 'Staff3_ATTEN_URGE'
                
                for i in range(Dr_NU_s3):
                    Trnasmiss = random.random() < TP
                    if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                        if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
    #                        V_recep[i][1] = 1        # Worker potential infection
                            dr_No_Urg_V_3[i][3] = day_current + 1 
                            dr_No_Urg_V_3[i][5] = PATIEN+'_ATTEN_URGE'
                            dr_No_Urg_V_3[i][6] = day_current + 1 
                            if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                dr_No_Urg_V_3[i][5] = PATIEN +'_ATTEN_URGE'
                            elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                dr_No_Urg_V_3[i][5] = 'Staff3_ATTEN_URGE'
                
                med_test = random.random() < Medic_test
                if med_test:
                    med_test_funct_shift_1(agent,i, da, currt_time)

            #------------    NEAR FIELD  ATTEN_URGE  INIT  ---------------------
            
            Sucep_Area = []
            if agent[1] == 1:
                Inf_room = Area_1_U + Area_2_U
                if agent[15] in (Area_1_U):
                    Inf_room = Area_1_U
                elif agent[15] in (Area_2_U):
                    Inf_room = Area_2_U
                
                for i in range(len(Users)):
                    if((Users[i][5] < currt_time) and 
                       (Users[i][2] =='ATTEN_URGE') and
                       (Users[i][1] == 0) and
                       (Users[i][15] in Inf_room )):
                        Sucep_Area.append(Users[i])
                if len(Sucep_Area) != 0:
                    if len(Sucep_Area) == 1:
                        SUS = 0
                    else:
                        SUS = random.randint(0, (len(Sucep_Area))-1 )
                    
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_pat_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        Sucep_Area[SUS][1] = 2
                        Sucep_Area[SUS][9] = Curr_Area
                        Sucep_Area[SUS][10] = day_current + 1 
                        Sucep_Area[SUS][11] = PATIEN +'_ATTEN_URGE' 
                        # print(Sucep_Area[SUS])

                #              Patient-HCW_Nurse
                if len(V_nurse_No_Urg_3) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 )

                if V_nurse_No_Urg_3[SUS][1] == 0 and V_nurse_No_Urg_3[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        V_nurse_No_Urg_3[SUS][3] = day_current + 1
                        V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTEN_URGE'
                        V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                
                #              Patient-HCW_MD
                if len(dr_No_Urg_V_3) == 1:
                        SUS = 0
                else:
                    SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )

                if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                    #                 Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_Ur * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss:
                        dr_No_Urg_V_3[SUS][3] = day_current + 1
                        dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTEN_URGE'
                        dr_No_Urg_V_3[SUS][6] = day_current + 1             

            #   ----------       HCW infected - patient   -----------------
            HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
            HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
            # Infected Nurse
            if V_nurse_No_Urg_3[HCW_N][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_N))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff3_ATTEN_URGE'
            # Infected Medical doc
            if dr_No_Urg_V_3[HCW_D][1] == 1:
                A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                Share_time = int(agent[4]*(Prop_P_H_M))
                diff = np.absolute(A1 - Share_time)
                index = diff.argmin()
                # TP = Tr_Pr_NEAR['Near'].loc[index, 
                #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
                TP = TP_Near_At_Ur * Pat_hcw_atten
                Trnasmiss = random.random() < TP 
                if Trnasmiss and (agent[1] == 0):
                    agent[1] = 2
                    agent[9] = Curr_Area
                    agent[10] = day_current + 1 
                    agent[11] = 'Staff3_ATTEN_URGE'     
            # ------------------------------------------------------------- 

            #------------    NEAR FIELD  ATTEN_URGE  CLOSE --------------------
                
    if At_NU == Curr_Area:  

        # -------------------------- TRANSMIS PROBABILITY TOP -------------------------
        # FAR - FIELD
        # Here, we look for the total of infected in the room (PAT, NUR or DR), and based
        # on that total, we take the FF TP and apply for any suscpt (PAT, NUR or DR)
        #   1- Check if any infect in the room, PAT, NUR, DR, besides the entering one
        #   2- if infected in the room - FF interaction time, the area time (agent[3])
        #   3- FOR PAT
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   4- FOR NURSE
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   5- FOR DR
        #       -TP for the area time, its applied with (who?) in area - HCW or PAT
        #   6- If necesary, sends to additional test - LAB or IMAG
        #       - calls function (time, agent, curr time)     
        #
        # NEAR-FIELD
        #   Infected PAT
        #   1- Search for suscp PAT (random selected) - estimate interaction time for NF TP
        #       - if TP TRUE, suscep starts infect status
        #   2- Search for NUR (rand select) - interact time NF proportion
        #       - if TP TRUE, suscep starts infect status for NUR
        #   3- Search for DR (rand select) - interact time NF proportion
        #       - if TP TRUE, suscep starts infect status for DR
        #
        #  Infected HCW
        #   1- search for a NUR and DR (rand)
        #   2- if NUR or DR infcted - interact time NF proportion (NUR or DR time)
        #   3- NF TP for proport of time - if TP TRUE
        #       - if TP TRUE, suscep starts infect status for PAT
        #  
        # -------------------------- TRANSMIS PROBABILITY BOTTOM-----------------------

        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:    

                
                # print(ATTEN_NU_INTRV)
                
                # if ATTEN_NON_UR_ROOM_1:
                    # print(ATTEN_NON_UR_ROOM_1)
                # cont_tot = 0
                # cont_inf = 0
                # infected = 0
                # # cont_tot_HCW = 0
                # cont_inf_HCW = 0
                # # for i in range(len(Users)):
                # #     # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                # #     if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                # #         and (Users[i][15] != UNDEF ) ):
                # #         cont_tot = cont_tot + 1
                # #         if(Users[i][1] == 1):
                # #             cont_inf = cont_inf + 1
     
                # for i in range(nur_NU_N_s1):
                #     if V_nurse_No_Urg_1[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
                # for i in range(Dr_NU_s1):
                #     if dr_No_Urg_V_1[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
        
                # # infected = cont_inf + cont_inf_HCW
                # infected =  cont_inf_HCW
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ) ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                           ( (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ) ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2

                for i in range(nur_NU_N_s1):
                    if V_nurse_No_Urg_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s1):
                    if dr_No_Urg_V_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                        
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth*CURTAINS
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth

                    # TP = TP * Att_N_fact
                    # TP = TP*Att_interv
                    # TP = TP*Att_NU_pro
                    
                    TP = TP * TP_Farf_At_NU_INT
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s1):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG'
                                    V_nurse_No_Urg_1[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     V_nurse_No_Urg_1[i][5] = PATIEN +'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG'
                                
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    # Trnasmiss = random.random() < TP     
                    # if Trnasmiss and (agent[1] == 0):
                    #     agent[1] = 2
                    #     agent[9] = Curr_Area
                    #     agent[10] = day_current + 1 
                    #     # agent[11] = "Staff1_ATTE_N_URG"
                    #     if cont_inf >= cont_inf_HCW:
                    #         agent[11] = PATIEN +'_ATTE_N_URG'
                    #     elif cont_inf_HCW > cont_inf:
                    #         agent[11] = 'Staff1_ATTE_N_URG'
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s1):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    dr_No_Urg_V_1[i][3] = day_current + 1 
                                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG'
                                    dr_No_Urg_V_1[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     dr_No_Urg_V_1[i][5] = PATIEN+'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
            
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                #              Patient-Patient
                Sucep_Area = []
                if agent[1] == 1:
                    # for i in range(len(Users)):
                    #     if((Users[i][5] < currt_time) and 
                    #        (Users[i][2] =='ATTE_N_URG') and
                    #        (Users[i][1] == 0)):
                    #         Sucep_Area.append(Users[i])
                    # if len(Sucep_Area) != 0:
                    #     if len(Sucep_Area) == 1:
                    #         SUS = 0
                    #     else:
                    #         SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                    #     A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    #     # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    #     Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    #     diff = np.absolute(A1 - Share_time)
                    #     index = diff.argmin()
                    #     TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                    #     Trnasmiss = random.random() < TP 
                    #     if Trnasmiss:
                    #         Sucep_Area[SUS][1] = 2
                    #         Sucep_Area[SUS][9] = Curr_Area
                    #         Sucep_Area[SUS][10] = day_current + 1 
                    #         Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                    #         # print(Sucep_Area[SUS])
                    
                    #              Patient-HCW_Nurse
                    
                    # if len(V_nurse_No_Urg_1) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
                        
                    # Curr_room = agent[15]
                    
                    # if Curr_room == 'ROOM_1':
                    #     SUS = 0
                    # elif Curr_room == 'ROOM_2':
                    #     SUS = 1
                    # elif Curr_room == 'ROOM_3':
                    #     SUS = 2
                    # # elif Curr_room == 'ROOM_4':
                    # else:
                    #     SUS = 3
                    
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s1):
                        if (Curr_room == V_nurse_No_Urg_1[i][16] or 
                            Curr_room == V_nurse_No_Urg_1[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                    
                    
                    #  Check in which room is the patient
                    #  Select the Nurse or MD attending that room
    
                    if V_nurse_No_Urg_1[SUS][1] == 0 and V_nurse_No_Urg_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_1[SUS][3] = day_current + 1
                            V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_1[SUS][6] = day_current + 1 
    
                    #              Patient-HCW_MD
                    # if len(dr_No_Urg_V_1) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(dr_No_Urg_V_1))-1 )
    
                    if dr_No_Urg_V_1[SUS][1] == 0 and dr_No_Urg_V_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_1[SUS][3] = day_current + 1
                            dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_1[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                #  Check in which room is the patient
                #  Select the Nurse or MD attending that room
                #  if the nurse or MD is infected, perform TP 
                
                Curr_room = agent[15]
                # if Curr_room == 'ROOM_1':
                #     SUS = 0
                # elif Curr_room == 'ROOM_2':
                #     SUS = 1
                # elif Curr_room == 'ROOM_3':
                #     SUS = 2
                # # elif Curr_room == 'ROOM_4':
                # else:
                #     SUS = 3
                    
                SUS = 0
                for i in range(nur_NU_N_s1):
                    if (Curr_room == V_nurse_No_Urg_1[i][16] or 
                        Curr_room == V_nurse_No_Urg_1[i][18]) :
                        SUS = i
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_1[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'     
                    # -------------------------------------------------------------    
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ) ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                           ( (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ) ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2

                for i in range(nur_NU_N_s1):
                    if V_nurse_No_Urg_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s1):
                    if dr_No_Urg_V_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    # TP = TP * Att_N_fact*HEAD_Att_NU
                    # TP = TP*Att_interv
                    # # TP = TP*0.5
                    # TP = TP*Att_NU_pro
                    
                    TP = TP * TP_Farf_At_NU
                    for i in range(nur_NU_N_s1):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_nurse_No_Urg_1[i][3] = day_current + 1 
                                V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_1[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_1[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG'
                                
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    Trnasmiss = random.random() < TP     
                    # if (Trnasmiss and (agent[1] == 0) and 
                    #     agent[15] == Users[i][15] ):
                    # HERE : set transmission pat-pat based on room
                    #         and HCW-pat rand
                    if (Trnasmiss and (agent[1] == 0) ):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff1_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        elif cont_inf_HCW > (cont_inf + cont_inf_2):
                            agent[11] = 'Staff1_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s1):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                dr_No_Urg_V_1[i][3] = day_current + 1 
                                dr_No_Urg_V_1[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_1[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_1[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
            
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                #              Patient-Patient
                Sucep_Area = []
                
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                    
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_pat_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                    
                    #              Patient-HCW_Nurse
                    
                    if len(V_nurse_No_Urg_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    
                    if V_nurse_No_Urg_1[SUS][1] == 0 and V_nurse_No_Urg_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_1[SUS][3] = day_current + 1
                            V_nurse_No_Urg_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_1[SUS][6] = day_current + 1 
    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_1))-1 )
    
                    if dr_No_Urg_V_1[SUS][1] == 0 and dr_No_Urg_V_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_1[SUS][3] = day_current + 1
                            dr_No_Urg_V_1[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_1[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_1))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_1[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_ATTE_N_URG'     
                   # -------------------------------------------------------------    
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
                

        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:
                # cont_tot = 0
                # cont_inf = 0
                # infected = 0
                # # cont_tot_HCW = 0
                # cont_inf_HCW = 0
                # # for i in range(len(Users)):
                # #     # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                # #     if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                # #             and (Users[i][15] != UNDEF ) ):
                # #         cont_tot = cont_tot + 1
                # #         if(Users[i][1] == 1):
                # #             cont_inf = cont_inf + 1
     
                # for i in range(nur_NU_N_s2):
                #     if V_nurse_No_Urg_2[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
                # for i in range(Dr_NU_s2):
                #     if dr_No_Urg_V_2[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
        
                # infected = cont_inf_HCW
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s2):
                    if V_nurse_No_Urg_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s2):
                    if dr_No_Urg_V_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    # TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth*CURTAINS
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    
                    
                    # TP = TP * Att_N_fact
                    # TP = TP*Att_interv
                    # TP = TP*Att_NU_pro
                    
                    TP = TP * TP_Farf_At_NU_INT
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s2):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG'
                                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     V_nurse_No_Urg_2[i][5] = PATIEN +'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    # Trnasmiss = random.random() < TP     
                    # if Trnasmiss and (agent[1] == 0):
                    #     agent[1] = 2
                    #     agent[9] = Curr_Area
                    #     agent[10] = day_current + 1 
                    #     # agent[11] = "Staff2_ATTE_N_URG"
                    #     if cont_inf >= cont_inf_HCW:
                    #         agent[11] = PATIEN +'_ATTE_N_URG'
                    #     if cont_inf_HCW >= cont_inf:
                    #         agent[11] = 'Staff2_ATTE_N_URG'
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s2):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    dr_No_Urg_V_2[i][3] = day_current + 1 
                                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                                    dr_No_Urg_V_2[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    # for i in range(len(Users)):
                    #     if((Users[i][5] < currt_time) and 
                    #        (Users[i][2] =='ATTE_N_URG') and
                    #        (Users[i][1] == 0)):
                    #         Sucep_Area.append(Users[i])
                    # if len(Sucep_Area) != 0:
                    #     if len(Sucep_Area) == 1:
                    #         SUS = 0
                    #     else:
                    #         SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                    #     A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    #     # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    #     Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    #     diff = np.absolute(A1 - Share_time)
                    #     index = diff.argmin()
                    #     TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    #     Trnasmiss = random.random() < TP 
                    #     if Trnasmiss:
                    #         Sucep_Area[SUS][1] = 2
                    #         Sucep_Area[SUS][9] = Curr_Area
                    #         Sucep_Area[SUS][10] = day_current + 1 
                    #         Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                    #         # print(Sucep_Area[SUS])
                
                    #              Patient-HCW_Nurse
                    
                    # HERE
                    # Curr_room = agent[15]
                    
                    # if Curr_room == 'ROOM_1':
                    #     SUS = 0
                    # elif Curr_room == 'ROOM_2':
                    #     SUS = 1
                    # elif Curr_room == 'ROOM_3':
                    #     SUS = 2
                    # # elif Curr_room == 'ROOM_4':
                    # else:
                    #     SUS = 3
                    
                    # if len(V_nurse_No_Urg_2) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
                        
                    
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s2):
                        if (Curr_room == V_nurse_No_Urg_2[i][16] or 
                            Curr_room == V_nurse_No_Urg_2[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                        
                    if V_nurse_No_Urg_2[SUS][1] == 0 and V_nurse_No_Urg_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_2[SUS][3] = day_current + 1
                            V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    # if len(dr_No_Urg_V_2) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )
    
                    if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_2[SUS][3] = day_current + 1
                            dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_2[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                
                Curr_room = agent[15]
                # SUS = ROMS_G_NAM.index(Curr_room)
                
                SUS = 0
                for i in range(nur_NU_N_s2):
                    if (Curr_room == V_nurse_No_Urg_2[i][16] or 
                        Curr_room == V_nurse_No_Urg_2[i][18]) :
                        SUS = i
                
                # if Curr_room == 'ROOM_1':
                #     SUS = 0
                # elif Curr_room == 'ROOM_2':
                #     SUS = 1
                # elif Curr_room == 'ROOM_3':
                #     SUS = 2
                # # elif Curr_room == 'ROOM_4':
                # else:
                #     SUS = 3
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_2[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'     
                # -------------------------------------------------------------            
    
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ) ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ) ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s2):
                    if V_nurse_No_Urg_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s2):
                    if dr_No_Urg_V_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    # TP = TP * Att_N_fact * HEAD_Att_NU *Att_interv * Att_NU_pro
                    # TP = TP*Att_interv
                    # # TP = TP*0.5
                    # TP = TP*Att_NU_pro
                    
                    
                    # TP = Farf_At_NU
                    # TP = Near_At_NU
                    
                    TP = TP * TP_Farf_At_NU
                    for i in range(nur_NU_N_s2):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_nurse_No_Urg_2[i][3] = day_current + 1 
                                V_nurse_No_Urg_2[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_2[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_2[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff2_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        if cont_inf_HCW >= (cont_inf + cont_inf_2):
                            agent[11] = 'Staff2_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s2):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                dr_No_Urg_V_2[i][3] = day_current + 1 
                                dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_2[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_2[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                        
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_pat_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                
                    #              Patient-HCW_Nurse
                    if len(V_nurse_No_Urg_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    
                    if V_nurse_No_Urg_2[SUS][1] == 0 and V_nurse_No_Urg_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_2[SUS][3] = day_current + 1
                            V_nurse_No_Urg_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_2[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_2))-1 )
    
                    if dr_No_Urg_V_2[SUS][1] == 0 and dr_No_Urg_V_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_2[SUS][3] = day_current + 1
                            dr_No_Urg_V_2[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_2[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_2))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_2[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_ATTE_N_URG'     
                # -------------------------------------------------------------            
    
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------

        
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]): 
            
            if ATTEN_NU_INTRV or CURTAINS_INTRV:
                # cont_tot = 0
                # cont_tot = 0
                # cont_inf = 0
                # # cont_tot_HCW = 0
                # cont_inf_HCW = 0
                # infected = 0
                # # for i in range(len(Users)):
                # #     # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                # #     if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                # #             and (Users[i][15] != UNDEF ) ):
                # #         cont_tot = cont_tot + 1
                # #         if(Users[i][1] == 1):
                # #             cont_inf = cont_inf + 1
     
                # for i in range(nur_NU_N_s3):
                #     if V_nurse_No_Urg_3[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
                # for i in range(Dr_NU_s3):
                #     if dr_No_Urg_V_3[i][1] == 1:
                #         cont_inf_HCW = cont_inf_HCW + 1
        
                # infected = cont_inf_HCW
                
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            (Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s3):
                    if V_nurse_No_Urg_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s3):
                    if dr_No_Urg_V_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    
                    # A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    
                    # A1 = Tr_Pr['11_Att_NU_INTRV'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                        
                    # TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth*CURTAINS
                    elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
                        TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, infected]*TP_pyth
                    

                    # TP = TP * Att_N_fact
                    # TP = TP*Att_interv
                    # TP = TP*Att_NU_pro
                    
                    TP = TP * TP_Farf_At_NU_INT
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(nur_NU_N_s3):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG'
                                    V_nurse_No_Urg_3[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     V_nurse_No_Urg_3[i][5] = PATIEN +'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    # Trnasmiss = random.random() < TP     
                    # if Trnasmiss and (agent[1] == 0):
                    #     agent[1] = 2
                    #     agent[9] = Curr_Area
                    #     agent[10] = day_current + 1 
                    #     # agent[11] = "Staff3_ATTE_N_URG"
                    #     if cont_inf >= cont_inf_HCW:
                    #         agent[11] = PATIEN +'_ATTE_N_URG'
                    #     if cont_inf_HCW > cont_inf:
                    #         agent[11] = 'Staff3_ATTE_N_URG'
                    
                    if CURTAINS_INTRV and 0 == ATTEN_NU_INTRV:
                        for i in range(Dr_NU_s3):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    dr_No_Urg_V_3[i][3] = day_current + 1 
                                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                                    dr_No_Urg_V_3[i][6] = day_current + 1 
                                # if cont_inf >= cont_inf_HCW:
                                #     dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                # elif cont_inf_HCW > cont_inf:
                                #     dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    # for i in range(len(Users)):
                    #     if((Users[i][5] < currt_time) and 
                    #        (Users[i][2] =='ATTE_N_URG') and
                    #        (Users[i][1] == 0)):
                    #         Sucep_Area.append(Users[i])
                    # if len(Sucep_Area) != 0:
                    #     if len(Sucep_Area) == 1:
                    #         SUS = 0
                    #     else:
                    #         SUS = random.randint(0, (len(Sucep_Area))-1 )
                        
                    #     A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    #     # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                    #     Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                    #     diff = np.absolute(A1 - Share_time)
                    #     index = diff.argmin()
                    #     TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    #     Trnasmiss = random.random() < TP 
                    #     if Trnasmiss:
                    #         Sucep_Area[SUS][1] = 2
                    #         Sucep_Area[SUS][9] = Curr_Area
                    #         Sucep_Area[SUS][10] = day_current + 1 
                    #         Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                    #         # print(Sucep_Area[SUS])
                   
                  #                Patient-HCW_Nurse
                    # if len(V_nurse_No_Urg_3) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 ) 
                    
                    Curr_room = agent[15]
                    SUS = 0
                    for i in range(nur_NU_N_s3):
                        if (Curr_room == V_nurse_No_Urg_3[i][16] or 
                            Curr_room == V_nurse_No_Urg_3[i][18]) :
                            SUS = i
                    
                    HCW_N = SUS
                    HCW_D = SUS
                    
                    
                    # Curr_room = agent[15]
                    
                    # if Curr_room == 'ROOM_1':
                    #     SUS = 0
                    # elif Curr_room == 'ROOM_2':
                    #     SUS = 1
                    # elif Curr_room == 'ROOM_3':
                    #     SUS = 2
                    # # elif Curr_room == 'ROOM_4':
                    # else:
                    #     SUS = 0
    
                    if V_nurse_No_Urg_3[SUS][1] == 0 and V_nurse_No_Urg_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_3[SUS][3] = day_current + 1
                            V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    # if len(dr_No_Urg_V_3) == 1:
                    #         SUS = 0
                    # else:
                    #     SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )
    
                    if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU_INT * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_3[SUS][3] = day_current + 1
                            dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_3[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                # HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
                # HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
                
                Curr_room = agent[15]
                # if Curr_room == 'ROOM_1':
                #     SUS = 0
                # elif Curr_room == 'ROOM_2':
                #     SUS = 1
                # elif Curr_room == 'ROOM_3':
                #     SUS = 2
                # # elif Curr_room == 'ROOM_4':
                # else:
                #     SUS = 0
                                
                SUS = 0
                for i in range(nur_NU_N_s3):
                    if (Curr_room == V_nurse_No_Urg_3[i][16] or 
                        Curr_room == V_nurse_No_Urg_3[i][18]) :
                        SUS = i
                    
                HCW_N = SUS
                HCW_D = SUS
                # Infected Nurse
                if V_nurse_No_Urg_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_3[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU_INT * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'     
                # ------------------------------------------------------------- 
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------
            
            else:
                cont_tot = 0
                cont_inf = 0
                cont_inf_2 = 0
                PAT_1 = 0
                PAT_2 = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                for i in range(len(Users)):
                    # if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    if ((Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG')
                        and (Users[i][15] != UNDEF ) ):
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_1') or 
                            (Users[i][15] == 'ROOM_2') or 
                            (Users[i][15] == 'ROOM_3') ) ):
                            cont_inf = cont_inf + 1
                        if ((Users[i][1] == 1) and 
                            ((Users[i][15] == 'ROOM_4') or 
                            (Users[i][15] == 'ROOM_5') or 
                            (Users[i][15] == 'ROOM_6') ) ):
                            cont_inf_2 = cont_inf_2 + 1

                PAT_1 = cont_inf
                PAT_2 = cont_inf_2
     
                for i in range(nur_NU_N_s3):
                    if V_nurse_No_Urg_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                for i in range(Dr_NU_s3):
                    if dr_No_Urg_V_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
        
                infected = (cont_inf + cont_inf_2) + cont_inf_HCW
                
                if infected > 0:
                    A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
                    diff = np.absolute(A1 - agent[3])
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['5_Atte_NoN'].loc[index, infected]*TP_pyth
                    # TP = TP * Att_N_fact * HEAD_Att_NU
                    # TP = TP*Att_interv
                    # # TP = TP*0.5
                    # TP = TP*Att_NU_pro
                    
                    TP = TP * TP_Farf_At_NU
                    for i in range(nur_NU_N_s3):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_nurse_No_Urg_3[i][3] = day_current + 1 
                                V_nurse_No_Urg_3[i][5] = PATIEN+'_ATTE_N_URG'
                                V_nurse_No_Urg_3[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    V_nurse_No_Urg_3[i][5] = PATIEN +'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        # agent[11] = "Staff3_ATTE_N_URG"
                        if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                            agent[11] = PATIEN +'_ATTE_N_URG'
                        if cont_inf_HCW > (cont_inf + cont_inf_2):
                            agent[11] = 'Staff3_ATTE_N_URG'
                    
                    for i in range(Dr_NU_s3):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and ((cont_inf + cont_inf_2) != 0 or cont_inf_HCW != 0)):
                            if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                dr_No_Urg_V_3[i][3] = day_current + 1 
                                dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                dr_No_Urg_V_3[i][6] = day_current + 1 
                                if (cont_inf + cont_inf_2) >= cont_inf_HCW:
                                    dr_No_Urg_V_3[i][5] = PATIEN+'_ATTE_N_URG'
                                elif cont_inf_HCW > (cont_inf + cont_inf_2):
                                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG'
                    
                    med_test = random.random() < Medic_test
                    if med_test:
                        med_test_funct_shift_1(agent,i, da, currt_time)
                #------------    NEAR FIELD  At_NU  INIT  ---------------------
                
                Sucep_Area = []
                if agent[1] == 1:
                    Inf_room = Area_1 + Area_2
                    if agent[15] in (Area_1):
                        Inf_room = Area_1
                    elif agent[15] in (Area_2):
                        Inf_room = Area_2
                        
                    for i in range(len(Users)):
                        if((Users[i][5] < currt_time) and 
                           (Users[i][2] =='ATTE_N_URG') and
                           (Users[i][1] == 0) and
                           (Users[i][15] in Inf_room )):
                            Sucep_Area.append(Users[i])
                    if len(Sucep_Area) != 0:
                        if len(Sucep_Area) == 1:
                            SUS = 0
                        else:
                            SUS = random.randint(0, (len(Sucep_Area))-1 )
                
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = abs(Sucep_Area[SUS][4]*Prop_P_P)
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_pat_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            Sucep_Area[SUS][1] = 2
                            Sucep_Area[SUS][9] = Curr_Area
                            Sucep_Area[SUS][10] = day_current + 1 
                            Sucep_Area[SUS][11] = PATIEN+'_ATTE_N_URG'   
                            # print(Sucep_Area[SUS])
                   
                    #              Patient-HCW_Nurse
                    if len(V_nurse_No_Urg_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    
                    if V_nurse_No_Urg_3[SUS][1] == 0 and V_nurse_No_Urg_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_nurse_No_Urg_3[SUS][3] = day_current + 1
                            V_nurse_No_Urg_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            V_nurse_No_Urg_3[SUS][6] = day_current + 1 
                    
                    #              Patient-HCW_MD
                    if len(dr_No_Urg_V_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(dr_No_Urg_V_3))-1 )
    
                    if dr_No_Urg_V_3[SUS][1] == 0 and dr_No_Urg_V_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(agent[4]*(Prop_P_H_M))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_At_NU * Pat_hcw_atten
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            dr_No_Urg_V_3[SUS][3] = day_current + 1
                            dr_No_Urg_V_3[SUS][5] = PATIEN+'_ATTE_N_URG'
                            dr_No_Urg_V_3[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
                HCW_D = random.randint(0, (len(dr_No_Urg_V_3))-1 )
                # Infected Nurse
                if V_nurse_No_Urg_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'
                # Infected Medical doc
                if dr_No_Urg_V_3[HCW_D][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_M))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_At_NU * Pat_hcw_atten
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_ATTE_N_URG'     
                # ------------------------------------------------------------- 
                
                #------------    NEAR FIELD  At_NU  CLOSE ---------------------

    return agent

     
"""----------------------------------------------------------------------------
                   ROUTINE MEDICAL TEST SHIFT 1
"""

def med_test_funct_shift_1(agent, i, day, currt_time):
    
    day_current = day
    Immagin = random.random() < 0.5
    t_med_test = random.randint(1, 60)
    agent[8] = agent[2]
    # Users[i][3] = t_med_test
    # agent[7] = agent[6] + t_med_test
    
    if Immagin:
        
        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                # Add counter to cont_inf_HCW (+1) if agent[1] == 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                    
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]

                    # TP = TP * Imagi_fact * HEAD_Imag
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Imagi
                    
                    for i in range(imagi_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_1[i][1] == 0 and V_imagin_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_1[i][3] = day_current + 1 
                                # V_imagin_1[i][5] = PATIEN +'_IMAGING'
                                V_imagin_1[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_1[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_1[i][5] = 'Staff1_IMAGING'
                                
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_IMAGING'
                               
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_1))-1 )
    
                    if V_imagin_1[SUS][1] == 0 and V_imagin_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Imagi * Pat_hcw_imagi
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_1[SUS][3] = day_current + 1
                            V_imagin_1[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_1[SUS][6] = day_current + 1 
                
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_1))-1 )
                # Infected Nurse
                if V_imagin_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Imagi * Pat_hcw_imagi
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_IMAGING'
                # ------------------------------------------------------------- 
                
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1

                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]

                    # TP = TP * Imagi_fact * HEAD_Imag
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Imagi
                    
                    for i in range(imagi_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_2[i][1] == 0 and V_imagin_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_2[i][3] = day_current + 1 
                                V_imagin_2[i][5] = PATIEN+'_IMAGING'
                                V_imagin_2[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_2[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_2[i][5] = 'Staff2_IMAGING'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2_IMAGING"
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_2))-1 )
    
                    if V_imagin_2[SUS][1] == 0 and V_imagin_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Imagi * Pat_hcw_imagi
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_2[SUS][3] = day_current + 1
                            V_imagin_2[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_2[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_2))-1 )
                # Infected Nurse
                if V_imagin_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Imagi * Pat_hcw_imagi
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_IMAGING'
                # ------------------------------------------------------------- 
    
        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(imagi_N):
                    if V_imagin_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1

                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                    
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['7_Imaging'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['7_Imaging'].loc[index, infected]

                    # TP = TP * Imagi_fact * HEAD_Imag
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Imagi
                    
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_imagin_3[i][1] == 0 and V_imagin_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_imagin_3[i][3] = day_current + 1 
                                V_imagin_3[i][5] = PATIEN+'_IMAGING'
                                V_imagin_3[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_imagin_3[i][5] = PATIEN +'_IMAGING'
                                elif cont_inf_HCW != 0:
                                    V_imagin_3[i][5] = 'Staff3_IMAGING'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='IMAGING'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3_IMAGING"
                
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_imagin_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_imagin_3))-1 )
    
                    if V_imagin_3[SUS][1] == 0 and V_imagin_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Imagi * Pat_hcw_imagi
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_imagin_3[SUS][3] = day_current + 1
                            V_imagin_3[SUS][5] = PATIEN +'_IMAGING'
                            V_imagin_3[SUS][6] = day_current + 1 
    
                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_imagin_3))-1 )
                # Infected Nurse
                if V_imagin_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Imagi * Pat_hcw_imagi
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_IMAGING'
                # ------------------------------------------------------------- 

    
    else:
        if (currt_time >= shift_1[0]) and (currt_time <= shift_1[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_1[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]

                    # TP = TP * Labor_fact * HEAD_Labor
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Labor
                    
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_1[i][1] == 0 and V_labor_1[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_1[i][3] = day_current + 1 
                                V_labor_1[i][5] = PATIEN+'_LABORATORY'
                                V_labor_1[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_1[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_1[i][5] = 'Staff1_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff1_LABORATORY"
    
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_1) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_1))-1 )
    
                    if V_labor_1[SUS][1] == 0 and V_labor_1[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Labor * Pat_hcw_labor
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_1[SUS][3] = day_current + 1
                            V_labor_1[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_1[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_1))-1 )
                # Infected Nurse
                if V_labor_1[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Labor * Pat_hcw_labor
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff1_LABORATORY'
                # ------------------------------------------------------------- 
    
        if (currt_time >= shift_2[0]) and (currt_time <= shift_2[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_2[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1
                
                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]

                    # TP = TP * Labor_fact * HEAD_Labor
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Labor
                    
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_2[i][1] == 0 and V_labor_2[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_2[i][3] = day_current + 1 
                                V_labor_2[i][5] = PATIEN+'_LABORATORY'
                                V_labor_2[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_2[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_2[i][5] = 'Staff2_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff2_LABORATORY"

                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_2) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_2))-1 )
    
                    if V_labor_2[SUS][1] == 0 and V_labor_2[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Labor * Pat_hcw_labor
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_2[SUS][3] = day_current + 1
                            V_labor_2[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_2[SUS][6] = day_current + 1     

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_2))-1 )
                # Infected Nurse
                if V_labor_2[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Labor * Pat_hcw_labor
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff2_LABORATORY'
                # ------------------------------------------------------------- 

        if (currt_time >= shift_3[0]) and (currt_time <= shift_3[1]):
                cont_tot = 0
                cont_inf = 0
                infected = 0
                # cont_tot_HCW = 0
                cont_inf_HCW = 0
                # for i in range(len(Users)):
                #     if (Users[i][5] < currt_time) and (Users[i][2] =='ATTE_N_URG'):
                #         cont_tot = cont_tot + 1
                #         if(Users[i][1] == 1):
                #             cont_inf = cont_inf + 1
     
                for i in range(labor_N):
                    if V_labor_3[i][1] == 1:
                        cont_inf_HCW = cont_inf_HCW + 1

                if agent[1] == 1:
                    cont_inf_HCW = cont_inf_HCW + 1
                
                infected = cont_inf_HCW         # count those infected HCW
                
                if infected > 0:
                    A1 = Tr_Pr['8_Laborat'].loc[:,'m']
                    diff = np.absolute(A1 - t_med_test)
                    index = diff.argmin()
                    if infected > 5:
                        infected = 5
                    TP = Tr_Pr['8_Laborat'].loc[index, infected]

                    # TP = TP * Labor_fact * HEAD_Labor
                    # TP = TP*TP_pyth
                    
                    TP = TP * TP_Farf_Labor
                    
                    for i in range(labor_N):
                        Trnasmiss = random.random() < TP
                        if (Trnasmiss and (cont_inf_HCW != 0)):
                            if V_labor_3[i][1] == 0 and V_labor_3[i][6] == 0:
        #                        V_recep[i][1] = 1        # Worker potential infection
                                V_labor_3[i][3] = day_current + 1 
                                V_labor_3[i][5] = PATIEN+'_LABORATORY'
                                V_labor_3[i][6] = day_current + 1 
                                if agent[1] == 1:
                                    V_labor_3[i][5] = PATIEN +'_LABORATORY'
                                elif cont_inf_HCW != 0:
                                    V_labor_3[i][5] = 'Staff3_LABORATORY'
                    
                    # for i in range(len(Users)):
                    #     if (Users[i][5] < currt_time) and (Users[i][2] =='LABORATORY'):
                    Trnasmiss = random.random() < TP     
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = "Staff3_LABORATORY"
                        
                #              Patient-HCW
                if agent[1] == 1:
                    if len(V_labor_3) == 1:
                            SUS = 0
                    else:
                        SUS = random.randint(0, (len(V_labor_3))-1 )
    
                    if V_labor_3[SUS][1] == 0 and V_labor_3[SUS][6] == 0:
                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                        Share_time = int(t_med_test*(Prop_P_H_N))
                        diff = np.absolute(A1 - Share_time)
                        index = diff.argmin()
                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                        TP = TP_Near_Labor * Pat_hcw_labor
                        Trnasmiss = random.random() < TP 
                        if Trnasmiss:
                            V_labor_3[SUS][3] = day_current + 1
                            V_labor_3[SUS][5] = PATIEN +'_LABORATORY'
                            V_labor_3[SUS][6] = day_current + 1 

                #   ----------       HCW infected - patient   -----------------
                HCW_N = random.randint(0, (len(V_labor_3))-1 )
                # Infected Nurse
                if V_labor_3[HCW_N][1] == 1:
                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                    Share_time = int(agent[4]*(Prop_P_H_N))
                    diff = np.absolute(A1 - Share_time)
                    index = diff.argmin()
                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[0]]*TP_pyth_Near
                    TP = TP_Near_Labor * Pat_hcw_labor
                    Trnasmiss = random.random() < TP 
                    if Trnasmiss and (agent[1] == 0):
                        agent[1] = 2
                        # agent[9] = Curr_Area
                        agent[10] = day_current + 1 
                        agent[11] = 'Staff3_LABORATORY'
                # ------------------------------------------------------------- 
        

    return


"""----------------------------------------------------------------------------
                          ROUTINE HCW SETTING 1
"""
def workers_settings(worker1, worker2, worker3):
        
        Users_workers_shift_1 = worker1
        Users_workers_shift_2 = worker2
        Users_workers_shift_3 = worker3
        
        
        for i in range(recep_N_s1):
            Users_workers_shift_1.append(V_recep_1[i])
        for i in range(recep_N_s2):
            Users_workers_shift_2.append(V_recep_2[i])
        for i in range(recep_N_s3):
            Users_workers_shift_3.append(V_recep_3[i])
    
        for i in range(triag_N_s1):
            Users_workers_shift_1.append(V_triag_1[i])
        for i in range(triag_N_s2):
            Users_workers_shift_2.append(V_triag_2[i])
        for i in range(triag_N_s3):
            Users_workers_shift_3.append(V_triag_3[i])
        
        for i in range(nur_NU_N_s1):
            Users_workers_shift_1.append(V_nurse_No_Urg_1[i])
        for i in range(nur_NU_N_s2):
            Users_workers_shift_2.append(V_nurse_No_Urg_2[i])
        for i in range(nur_NU_N_s3):
            Users_workers_shift_3.append(V_nurse_No_Urg_3[i])
        
        for i in range(Dr_NU_s1):
            Users_workers_shift_1.append(dr_No_Urg_V_1[i])
        for i in range(Dr_NU_s2):
            Users_workers_shift_2.append(dr_No_Urg_V_2[i])
        for i in range(Dr_NU_s3):    
            Users_workers_shift_3.append(dr_No_Urg_V_3[i])
        

        for i in range(imagi_N):
            Users_workers_shift_1.append(V_imagin_1[i])
            Users_workers_shift_2.append(V_imagin_2[i])
            Users_workers_shift_3.append(V_imagin_3[i])
        
        for i in range(labor_N):
            Users_workers_shift_1.append(V_labor_1[i])
            Users_workers_shift_2.append(V_labor_2[i])
            Users_workers_shift_3.append(V_labor_3[i])
    
    
        return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3
 
"""----------------------------------------------------------------------------
                          ROUTINE HCW INFECTION STATUS
"""    
def workers_settings_status(worker1, worker2, worker3, days):
    day_current = days
    Users_workers_shift_1 = worker1
    Users_workers_shift_2 = worker2
    Users_workers_shift_3 = worker3
    
    # ------------------   shift 1    -----------------------------------------
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] == 0):
            Users_workers_shift_1[i][4] = Users_workers_shift_1[i][3] + time_length_colonized #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_1[i][9] = 'Colonized'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_1[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_1[i][11] = Users_workers_shift_1[i][3] + time_length_asymptomatic #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_1[i][11] != 0)and (Users_workers_shift_1[i][10] == UNDEF): 
         #   Users_workers_shift_1[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] != 0) and (Users_workers_shift_1[i][4] != 0):
            Users_workers_shift_1[i][3] = day_current + 1 #reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_1)):
        if ((Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and 
                                     (Users_workers_shift_1[i][5] != UNDEF )):
            Users_workers_shift_1[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][4]) and (Users_workers_shift_1[i][1] == 1) :
            Users_workers_shift_1[i][12] = Users_workers_shift_1[i][3] + time_length_infectious #infectious , can spread infections after 5 days
            Users_workers_shift_1[i][9] = 'infectious'
            
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][12]) and (Users_workers_shift_1[i][9] == 'infectious') :
            #Users_workers_shift_1[i][13] = Users_workers_shift_1[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_1[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_1)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_1[i][3] == Users_workers_shift_1[i][11]) and  (Users_workers_shift_1[i][10] =='No symptom') and (Users_workers_shift_1[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_1[i][7] = SYMP_NO
            else:
                Users_workers_shift_1[i][7] = SYMP_YES            
    
                
    for i in range(len(Users_workers_shift_1)):
        if (Users_workers_shift_1[i][7] == SYMP_YES) and (Users_workers_shift_1[i][9] == 'infectious') :
            if Users_workers_shift_1[i][8] == REPLACE:
                Users_workers_shift_1[i][13] = Users_workers_shift_1[i][13] + 1
            Users_workers_shift_1[i][8] = REPLACE
            Users_workers_shift_1[i][1] = 0
            Users_workers_shift_1[i][4] = 0
            Users_workers_shift_1[i][5] = UNDEF
            Users_workers_shift_1[i][6] = 0
            Users_workers_shift_1[i][7] = UNDEF
            Users_workers_shift_1[i][9] = UNDEF
            Users_workers_shift_1[i][10] = UNDEF
            Users_workers_shift_1[i][11] = 0
            Users_workers_shift_1[i][12] = 0
            #Users_workers_shift_1[i][13] = 0
            Users_workers_shift_1[i][14] = UNDEF
            
        if (Users_workers_shift_1[i][10] == 'No symptom')and (Users_workers_shift_1[i][14] == 'immune') : 
            Users_workers_shift_1[i][1] = 0 
            Users_workers_shift_1[i][9] = UNDEF
            
           
    # ------------------   shift 2    -----------------------------------------
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] == 0):
            Users_workers_shift_2[i][4] = Users_workers_shift_2[i][3] + time_length_colonized #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_2[i][9] = 'Colonized'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_2[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_2[i][11] = Users_workers_shift_2[i][3] + time_length_asymptomatic #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_2[i][11] != 0)and (Users_workers_shift_2[i][10] == UNDEF): 
         #   Users_workers_shift_2[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] != 0) and (Users_workers_shift_2[i][4] != 0):
            Users_workers_shift_2[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
     
    for i in range(len(Users_workers_shift_2)):
        if ((Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and 
                                     (Users_workers_shift_2[i][5] != UNDEF )):
            Users_workers_shift_2[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][4]) and (Users_workers_shift_2[i][1] == 1) :
            Users_workers_shift_2[i][12] = Users_workers_shift_2[i][3] + time_length_infectious #infectious , can spread infections after 5 days
            Users_workers_shift_2[i][9] = 'infectious'
            
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][12])and (Users_workers_shift_2[i][9] == 'infectious') :
            #Users_workers_shift_2[i][13] = Users_workers_shift_2[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_2[i][14] = 'immune'
            

    for i in range(len(Users_workers_shift_2)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_2[i][3] == Users_workers_shift_2[i][11]) and  (Users_workers_shift_2[i][10] =='No symptom') and (Users_workers_shift_2[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_2[i][7] = SYMP_NO
            else:
                Users_workers_shift_2[i][7] = SYMP_YES         
    

                
    for i in range(len(Users_workers_shift_2)):
        if (Users_workers_shift_2[i][7] == SYMP_YES) and (Users_workers_shift_2[i][9] == 'infectious') :
            if Users_workers_shift_2[i][8] == REPLACE:
                Users_workers_shift_2[i][13] = Users_workers_shift_2[i][13] + 1
            Users_workers_shift_2[i][8] = REPLACE
            Users_workers_shift_2[i][1] = 0
            Users_workers_shift_2[i][4] = 0
            Users_workers_shift_2[i][5] = UNDEF
            Users_workers_shift_2[i][6] = 0
            Users_workers_shift_2[i][7] = UNDEF
            Users_workers_shift_2[i][9] = UNDEF
            Users_workers_shift_2[i][10] = UNDEF
            Users_workers_shift_2[i][11] = 0
            Users_workers_shift_2[i][12] = 0
            # Users_workers_shift_2[i][13] = 0
            Users_workers_shift_2[i][14] = UNDEF
            
            
        if (Users_workers_shift_2[i][10] == 'No symptom')and (Users_workers_shift_2[i][14] == 'immune') : 
            Users_workers_shift_2[i][1] = 0 
            Users_workers_shift_2[i][9] = UNDEF
            
        
    # ------------------   shift 3    -----------------------------------------
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] == 0):
            Users_workers_shift_3[i][4] = Users_workers_shift_3[i][3] + time_length_colonized #not infectious after three days of being exposed to an infected agent
            Users_workers_shift_3[i][9] = 'Colonized'#not infectious after three days of exposed to an infected agent
            Users_workers_shift_3[i][10] = 'No symptom'#not showing symptom  after three days of exposed to an infected agent
            Users_workers_shift_3[i][11] = Users_workers_shift_3[i][3] + time_length_asymptomatic #no of days of not showing symptoms after getting exposed to an infected person
        
        #if (Users_workers_shift_3[i][11] != 0)and (Users_workers_shift_3[i][10] == UNDEF): 
         #   Users_workers_shift_3[i][12] = 'No symptom'
            
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] != 0) and (Users_workers_shift_3[i][4] != 0):
            Users_workers_shift_3[i][3] = day_current + 1#reupdate index 3 to continue counter for the number of days
    
    for i in range(len(Users_workers_shift_3)):
        if ((Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and 
                                     (Users_workers_shift_3[i][5] != UNDEF )):
            Users_workers_shift_3[i][1] = 1    
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][4]) and (Users_workers_shift_3[i][1] == 1) :
            Users_workers_shift_3[i][12] = Users_workers_shift_3[i][3] + time_length_infectious #infectious , can spread infections after 5 days
            Users_workers_shift_3[i][9] = 'infectious'
            
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][12])and (Users_workers_shift_3[i][9] == 'infectious') :
            #Users_workers_shift_3[i][13] = Users_workers_shift_3[i][3] + 3 # #immune after days of being infectious 
            Users_workers_shift_3[i][14] = 'immune'
                      
        
    for i in range(len(Users_workers_shift_3)): #-> showing symptoms after 5 days of getting infected
        if (Users_workers_shift_3[i][3] == Users_workers_shift_3[i][11]) and  (Users_workers_shift_3[i][10] =='No symptom') and (Users_workers_shift_3[i][9] == 'infectious'):
            
            check = random.random() < PB_SYMPTOMS #more probable to be symptomatic
            if check: 
                Users_workers_shift_3[i][7] = SYMP_NO
            else:
                Users_workers_shift_3[i][7] = SYMP_YES           
    
    
    for i in range(len(Users_workers_shift_3)):
        if (Users_workers_shift_3[i][7] == SYMP_YES) and (Users_workers_shift_3[i][9] == 'infectious') :
            if Users_workers_shift_3[i][8] == REPLACE:
                Users_workers_shift_3[i][13] = Users_workers_shift_3[i][13] + 1
            Users_workers_shift_3[i][8] = REPLACE
            Users_workers_shift_3[i][1] = 0
            Users_workers_shift_3[i][4] = 0
            Users_workers_shift_3[i][5] = UNDEF
            Users_workers_shift_3[i][6] = 0
            Users_workers_shift_3[i][7] = UNDEF
            Users_workers_shift_3[i][9] = UNDEF
            Users_workers_shift_3[i][10] = UNDEF
            Users_workers_shift_3[i][11] = 0
            Users_workers_shift_3[i][12] = 0
            #Users_workers_shift_3[i][13] = 0
            Users_workers_shift_3[i][14] = UNDEF
            
                                                
        if (Users_workers_shift_3[i][10] == 'No symptom')and (Users_workers_shift_3[i][14] == 'immune') : 
            Users_workers_shift_3[i][1] = 0 
            Users_workers_shift_3[i][9] = UNDEF
    
    return Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3



def meet_HCW_1():
#---------------------------- TRANS PROB  INIT -------------------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM -------------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s1):
        if V_recep_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Recep_fact
        
        TP = TP * TP_Farf_Recep
        
        for i in range(recep_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_1[i][1] == 0 and V_recep_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_1[i][6] = day_current + 1 
                    V_recep_1[i][5] = 'Staff1_RECEPTION' 
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_1))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_1[Sus_HCW][1] == 0 and V_recep_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, 
        #                     Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Recep * hcw_hcw_recep
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_1[Sus_HCW][3] = day_current + 1
            V_recep_1[Sus_HCW][5] = 'Staff1_RECEPTION' 
            V_recep_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   

    
    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s1):
        if V_triag_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Triag_fact
        
        TP = TP * TP_Farf_Triag
        
        for i in range(triag_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_1[i][1] == 0 and V_triag_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_1[i][6] = day_current + 1 
                    V_triag_1[i][5] = 'Staff1_TRIAGE'
    
        # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_1[Sus_HCW][1] == 0 and V_triag_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Triag * hcw_hcw_triag
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_1[Sus_HCW][3] = day_current + 1
            V_triag_1[Sus_HCW][5] = 'Staff1_TRIAGE' 
            V_triag_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s1):
        if V_nurse_No_Urg_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_1[i])
    for i in range(Dr_NU_s1):
        if dr_No_Urg_V_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_1[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Att_U_fact * HEAD_Att_U
        
        TP = TP * TP_Farf_At_Ur
        
        for i in range(nur_NU_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_1[i][6] = day_current + 1 
                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTEN_URGE' 
        for i in range(Dr_NU_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_1[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_1[i][6] = day_current + 1 
                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_1))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, 
        #                         Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if ((random.random() < TP) and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, 
        #                         Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_1[Sus_M][6] == 0) ):
            dr_No_Urg_V_1[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_1[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_1[Sus_M][5] = 'Staff1_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s1):
        if V_nurse_No_Urg_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_1[i])
    for i in range(Dr_NU_s1):
        if dr_No_Urg_V_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_1[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
            TP = TP * TP_Farf_At_NU_INT
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU_INT
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU

        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_1[i][1] == 0 and V_nurse_No_Urg_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_1[i][6] = day_current + 1 
                    V_nurse_No_Urg_1[i][5] = 'Staff1_ATTE_N_URG' 
        for i in range(Dr_NU_s1):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_1[i][1] == 0 and dr_No_Urg_V_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_1[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_1[i][6] = day_current + 1 
                    dr_No_Urg_V_1[i][5] = 'Staff1_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_1))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_1))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index,
        #                             Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if ((random.random() < TP) and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, 
        #                             Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_1[Sus_N][1] == 0) and
            (V_nurse_No_Urg_1[Sus_N][6] == 0) ):
            V_nurse_No_Urg_1[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_1[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_1[Sus_N][5] = 'Staff1_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_1[Sus_M][6] == 0) ):
            dr_No_Urg_V_1[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_1[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_1[Sus_M][5] = 'Staff1_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]

        # TP = TP * Imagi_fact * HEAD_Imag
        # TP = TP*TP_pyth
        
        TP = TP * TP_Farf_Imagi
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_1[i][1] == 0 and V_imagin_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_1[i][6] = day_current + 1 
                    V_imagin_1[i][5] = 'Staff1_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_1[Sus_HCW][1] == 0 and V_imagin_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Imagi * hcw_hcw_imagi
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_1[Sus_HCW][3] = day_current + 1
            V_imagin_1[Sus_HCW][5] = 'Staff1_IMAGING' 
            V_imagin_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_1[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_1[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]

        # TP = TP*TP_pyth
        # TP = TP * Labor_fact * HEAD_Labor
        
        TP = TP * TP_Farf_Labor
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_1[i][1] == 0 and V_labor_1[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_1[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_1[i][6] = day_current + 1 
                    V_labor_1[i][5] = 'Staff1_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_1))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_1[Sus_HCW][1] == 0 and V_labor_1[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Labor * hcw_hcw_labor
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_1[Sus_HCW][3] = day_current + 1
            V_labor_1[Sus_HCW][5] = 'Staff1_LABORATORY' 
            V_labor_1[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 

    return



def meet_HCW_2():
    
#---------------------------- TRANS PROB  INIT -------------------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM -------------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s2):
        if V_recep_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Recep_fact
        
        TP = TP * TP_Farf_Recep
        
        for i in range(recep_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_2[i][1] == 0 and V_recep_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_2[i][6] = day_current + 1 
                    V_recep_2[i][5] = 'Staff2_RECEPTION' 

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_2))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_2[Sus_HCW][1] == 0 and V_recep_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Recep * hcw_hcw_recep
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_2[Sus_HCW][3] = day_current + 1
            V_recep_2[Sus_HCW][5] = 'Staff2_RECEPTION' 
            V_recep_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------   
    
    
    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s2):
        if V_triag_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Triag_fact
        for i in range(triag_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_2[i][1] == 0 and V_triag_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_2[i][6] = day_current + 1 
                    V_triag_2[i][5] = 'Staff2_TRIAGE'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_2[Sus_HCW][1] == 0 and V_triag_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Triag * hcw_hcw_triag
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_2[Sus_HCW][3] = day_current + 1
            V_triag_2[Sus_HCW][5] = 'Staff2_TRIAGE' 
            V_triag_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s2):
        if V_nurse_No_Urg_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_2[i])
    for i in range(Dr_NU_s2):
        if dr_No_Urg_V_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_2[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Att_U_fact * HEAD_Att_U
        
        TP = TP * TP_Farf_At_Ur
        
        for i in range(nur_NU_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTEN_URGE' 
        for i in range(Dr_NU_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_2[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_2[i][6] = day_current + 1 
                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_2))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_1[Sus_M][1] == 0) and
            (dr_No_Urg_V_2[Sus_M][6] == 0) ):
            dr_No_Urg_V_2[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_2[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_2[Sus_M][5] = 'Staff2_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s2):
        if V_nurse_No_Urg_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_2[i])
    for i in range(Dr_NU_s2):
        if dr_No_Urg_V_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_2[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
            TP = TP * TP_Farf_At_NU_INT
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU_INT
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU
        
        # TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_2[i][1] == 0 and V_nurse_No_Urg_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_2[i][6] = day_current + 1 
                    V_nurse_No_Urg_2[i][5] = 'Staff2_ATTE_N_URG' 
        for i in range(Dr_NU_s2):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_2[i][1] == 0 and dr_No_Urg_V_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_2[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_2[i][6] = day_current + 1 
                    dr_No_Urg_V_2[i][5] = 'Staff2_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_2))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_2))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_2[Sus_N][1] == 0) and
            (V_nurse_No_Urg_2[Sus_N][6] == 0) ):
            V_nurse_No_Urg_2[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_2[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_2[Sus_N][5] = 'Staff2_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_2[Sus_M][1] == 0) and
            (dr_No_Urg_V_2[Sus_M][6] == 0) ):
            dr_No_Urg_V_2[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_2[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_2[Sus_M][5] = 'Staff2_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]

        # TP = TP * Imagi_fact * HEAD_Imag
        # TP = TP*TP_pyth
        
        TP = TP * TP_Farf_Imagi
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_2[i][1] == 0 and V_imagin_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_2[i][6] = day_current + 1 
                    V_imagin_2[i][5] = 'Staff2_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_2[Sus_HCW][1] == 0 and V_imagin_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Imagi * hcw_hcw_imagi
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_2[Sus_HCW][3] = day_current + 1
            V_imagin_2[Sus_HCW][5] = 'Staff2_IMAGING' 
            V_imagin_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_2[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_2[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]

        # TP = TP*TP_pyth
        # TP = TP * Labor_fact * HEAD_Labor
        
        TP = TP * TP_Farf_Labor
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_2[i][1] == 0 and V_labor_2[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_2[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_2[i][6] = day_current + 1 
                    V_labor_2[i][5] = 'Staff2_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_2))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_2[Sus_HCW][1] == 0 and V_labor_2[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Labor * hcw_hcw_labor
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_2[Sus_HCW][3] = day_current + 1
            V_labor_2[Sus_HCW][5] = 'Staff2_LABORATORY' 
            V_labor_2[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 

    return



def meet_HCW_3():

#---------------------------- TRANS PROB  INIT -------------------------------------
# FAR -FIELD
# 1- Count the total of infected HCWs of the area
# 2- Check FF TP for time_area_HCW and appy for each HCW of the area  
#
# NEAR FIELD
# 1- Random select a HCW from area, account for the total of inf from FAR-FIELD
# 2- if suscept, apply NF TP for Prop_H_H_Recep
#
#---------------------------- TRANS PROB BOTOM -------------------------------------

    
    #  -------  RECEPTION --------------------
    cont_inf_HCW = 0
    infe_WCH = 0
    for i in range(recep_N_s3):
        if V_recep_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH = V_recep_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Recep_fact
        
        TP = TP * TP_Farf_Recep
        
        for i in range(recep_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_recep_3[i][1] == 0 and V_recep_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_recep_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_recep_3[i][6] = day_current + 1 
                    V_recep_3[i][5] = 'Staff3_RECEPTION' 
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_recep_3))-1 )
    if ( (infe_WCH != 0) and  
            (V_recep_3[Sus_HCW][1] == 0 and V_recep_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Recep)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Recep * hcw_hcw_recep
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_recep_3[Sus_HCW][3] = day_current + 1
            V_recep_3[Sus_HCW][5] = 'Staff3_RECEPTION' 
            V_recep_3[Sus_HCW][6] = day_current + 1  
     # -----------------  Near Field H-H  close  ------------------------
    

    #  -------  TRIAGE --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(triag_N_s3):
        if V_triag_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_triag_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['1_Reception'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['1_Reception'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Triag_fact
        
        TP = TP * TP_Farf_Triag
        
        for i in range(triag_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_triag_3[i][1] == 0 and V_triag_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_triag_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_triag_3[i][6] = day_current + 1 
                    V_triag_3[i][5] = 'Staff3_TRIAGE'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_triag_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_triag_3[Sus_HCW][1] == 0 and V_triag_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Triag)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_Triag * hcw_hcw_triag
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_triag_3[Sus_HCW][3] = day_current + 1
            V_triag_3[Sus_HCW][5] = 'Staff3_TRIAGE' 
            V_triag_3[Sus_HCW][6] = day_current + 1 
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  ATTEN_URGE --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s3):
        if V_nurse_No_Urg_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_3[i])
    for i in range(Dr_NU_s3):
        if dr_No_Urg_V_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_3[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['6_Atte_Urg_1'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        TP = Tr_Pr['6_Atte_Urg_1'].loc[index, cont_inf_HCW]*TP_pyth
        # TP = TP * Att_U_fact * HEAD_Att_U
        
        TP = TP * TP_Farf_At_Ur
        
        for i in range(nur_NU_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_3[i][6] = day_current + 1 
                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTEN_URGE' 
        for i in range(Dr_NU_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_3[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_3[i][6] = day_current + 1 
                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTEN_URGE'    
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_3))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTEN_URGE' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_At_Ur * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTEN_URGE' 
        if ((random.random() < TP) and (dr_No_Urg_V_3[Sus_M][1] == 0) and
            (dr_No_Urg_V_3[Sus_M][6] == 0) ):
            dr_No_Urg_V_3[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_3[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_3[Sus_M][5] = 'Staff3_ATTEN_URGE' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  ATTE_N_URG --------------------
    cont_inf_HCW = 0
    inf_N = []
    inf_M = []
    for i in range(nur_NU_N_s3):
        if V_nurse_No_Urg_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_N.append(V_nurse_No_Urg_3[i])
    for i in range(Dr_NU_s3):
        if dr_No_Urg_V_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            inf_M.append(dr_No_Urg_V_3[i])
    
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['5_Atte_NoN'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW_Att)
        index = diff.argmin()
        
        if CURTAINS_INTRV:
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth*CURTAINS
            TP = TP * TP_Farf_At_NU_INT
        # else: 
        #     TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        elif ATTEN_NU_INTRV and 0 == CURTAINS_INTRV:
            TP = Tr_Pr['11_Att_NU_INTRV'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU_INT
        else: 
            TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
            TP = TP * TP_Farf_At_NU
        
        # TP = Tr_Pr['5_Atte_NoN'].loc[index, cont_inf_HCW]*TP_pyth
        TP = TP * Att_N_fact * HEAD_Att_NU
        # TP = TP*ATT_NU_H_H
        for i in range(nur_NU_N_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_nurse_No_Urg_3[i][1] == 0 and V_nurse_No_Urg_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_nurse_No_Urg_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_nurse_No_Urg_3[i][6] = day_current + 1 
                    V_nurse_No_Urg_3[i][5] = 'Staff3_ATTE_N_URG' 
        for i in range(Dr_NU_s3):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if dr_No_Urg_V_3[i][1] == 0 and dr_No_Urg_V_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    dr_No_Urg_V_3[i][3] = day_current + 1 
                    # dr_No_Urg_V_1[i][5] = PATIEN+'_ATTEN_URGE'
                    dr_No_Urg_V_3[i][6] = day_current + 1 
                    dr_No_Urg_V_3[i][5] = 'Staff3_ATTE_N_URG' 
    
    # -----------------  Near Field HCW - HCW   ------------------------
    # if ((len(inf_N) == 0) or (len(inf_M) == 0)):
    #     Inf_HCW_N = 0
    #     Inf_HCW_M = 0
    # else:
    #     Inf_HCW_N = random.randint(0, (len(inf_N))-1 )
    #     Inf_HCW_M = random.randint(0, (len(inf_M))-1 )
    Sus_N = random.randint(0, (len(V_nurse_No_Urg_3))-1 )
    Sus_M = random.randint(0, (len(dr_No_Urg_V_3))-1 ) 
    
    #       Nurse - Nurse
    if ((len(inf_N) > 0 ) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Nu_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTE_N_URG' 

    #       MD  - Nurse
    if ( (len(inf_M) > 0)):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_MD_Nu)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        TP = TP_Near_At_NU * hcw_hcw_atten
        Trnasmiss = random.random() < TP
        if (Trnasmiss and (V_nurse_No_Urg_3[Sus_N][1] == 0) and
            (V_nurse_No_Urg_3[Sus_N][6] == 0) ):
            V_nurse_No_Urg_3[Sus_N][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            V_nurse_No_Urg_3[Sus_N][6] = day_current + 1 
            V_nurse_No_Urg_3[Sus_N][5] = 'Staff3_ATTE_N_URG' 
        if ((random.random() < TP) and (dr_No_Urg_V_3[Sus_M][1] == 0) and
            (dr_No_Urg_V_3[Sus_M][6] == 0) ):
            dr_No_Urg_V_3[Sus_M][3] = day_current + 1 
            # V_recep_1[i][5] = PATIEN+'_RECEPTION'
            dr_No_Urg_V_3[Sus_M][6] = day_current + 1 
            dr_No_Urg_V_3[Sus_M][5] = 'Staff3_ATTE_N_URG' 
    
    # -----------------  Near Field close   ------------------------
    
    
    #  -------  IMAGING --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(imagi_N):
        if V_imagin_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_imagin_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['7_Imaging'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['7_Imaging'].loc[index, cont_inf_HCW]

        # TP = TP * Imagi_fact * HEAD_Imag
        # TP = TP*TP_pyth
        
        TP = TP * TP_Farf_Imagi
        
        for i in range(imagi_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_imagin_3[i][1] == 0 and V_imagin_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_imagin_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_imagin_3[i][6] = day_current + 1 
                    V_imagin_3[i][5] = 'Staff3_IMAGING'
    
    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_imagin_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_imagin_3[Sus_HCW][1] == 0 and V_imagin_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Imagi * hcw_hcw_imagi
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_imagin_3[Sus_HCW][3] = day_current + 1
            V_imagin_3[Sus_HCW][5] = 'Staff3_IMAGING' 
            V_imagin_3[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 
    
    #  -------  LABORATORY --------------------
    cont_inf_HCW = 0
    infe_WCH_T = 0
    for i in range(labor_N):
        if V_labor_3[i][1] == 1:
            cont_inf_HCW = cont_inf_HCW + 1
            infe_WCH_T = V_labor_3[i]
    if cont_inf_HCW > 0:
        if cont_inf_HCW > 5:
            cont_inf_HCW = 5
        A1 = Tr_Pr['8_Laborat'].loc[:,'m']
        diff = np.absolute(A1 - time_area_HCW)
        index = diff.argmin()
        TP = Tr_Pr['8_Laborat'].loc[index, cont_inf_HCW]

        # TP = TP*TP_pyth
        # TP = TP * Labor_fact * HEAD_Labor
        
        TP = TP * TP_Farf_Triag
        
        for i in range(labor_N):
            Trnasmiss = random.random() < TP
            if Trnasmiss:
                if V_labor_3[i][1] == 0 and V_labor_3[i][6] == 0:
#                        V_recep[i][1] = 1        # Worker potential infection
                    V_labor_3[i][3] = day_current + 1 
                    # V_recep_1[i][5] = PATIEN+'_RECEPTION'
                    V_labor_3[i][6] = day_current + 1 
                    V_labor_3[i][5] = 'Staff3_LABORATORY'

    # -----------------  Near Field H-H   ------------------------
    Sus_HCW = random.randint(0, (len(V_labor_3))-1 )
    if ( (infe_WCH_T != 0) and  
            (V_labor_3[Sus_HCW][1] == 0 and V_labor_3[Sus_HCW][6] == 0) ):
        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
        # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
        # Share_time = int(agent[4]*(Prop_P_H_M))
        diff = np.absolute(A1 - Prop_H_H_Labor)
        index = diff.argmin()
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
        TP = TP_Near_Labor * hcw_hcw_labor
        Trnasmiss = random.random() < TP 
        if Trnasmiss:
            V_labor_3[Sus_HCW][3] = day_current + 1
            V_labor_3[Sus_HCW][5] = 'Staff3_LABORATORY' 
            V_labor_3[Sus_HCW][6] = day_current + 1 
            
     # -----------------  Near Field H-H  close  ------------------------ 


    return


"""----------------------------------------------------------------------------
                          Routine for Fomites
""" 
def fomite_function(HCW_pool, Curr_Area, which_foms=all_foms, TP_multiplier=1):
    # Define User rooms
    # for I in User, if [15] == "ROOM_1": [17] = "NU_Room_13"
    if Curr_Area == AT_UR or Curr_Area == At_NU:
        for i in range(len(Users)):
            if CURTAINS_INTRV == 0 and ATTEN_NU_INTRV == 0:
                if Users[i][15] == "ROOM_1" or Users[i][15] == "ROOM_2" or Users[i][15] == "ROOM_3":
                    Users[i][17] = "NU_Room_13"
                elif Users[i][15] == "ROOM_4" or Users[i][15] == "ROOM_5" or Users[i][15] == "ROOM_6":
                    Users[i][17] = "NU_Room_46"
                elif Users[i][15] == "BEDS_1" or Users[i][15] == "BEDS_2" or Users[i][15] == "BEDS_3":
                    Users[i][17] = "UR_Room_13"
                elif Users[i][15] == "BEDS_4" or Users[i][15] == "BEDS_5" or Users[i][15] == "BEDS_6":
                    Users[i][17] = "UR_Room_46"
                elif Users[i][15] == UNDEF and Users[i][2] == AT_UR:
                    if random.random() < 0.5:
                        Users[i][17] = "UR_Room_13"
                    else: 
                        Users[i][17] = "UR_Room_46"


    # Define fomites
    if Curr_Area != WAI_N:
        # for i in range(len(Fomite))
        for f in which_foms:
            if Fomite[f][5] == Curr_Area:
        
                #  -- ----            User and fomite interaction -------------------
                for i in range(len(Users)):
                    # Identify users in area
                    if Users[i][2] == Curr_Area and Users[i][5] <= Time_var:
                        
                        # Reception: patient only interacts with counter (only nonurgent)
                        if (RECEP == Curr_Area and (Users[i][12] == "YELLOW" or Users[i][12] == "GREEN" or Users[i][12] == "BLUE")):
                            if Fomite[f][1] == "Counter":
                                # if fomite is contaminated, might infect patient
                                if Users[i][1] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]: 
                                    # tp_Fomite_person = random.random() < 0.5
                                    if (random.random() < tp_Fomite_person() * pat_fom_recep * TP_Fom_Recep) == 1:
                                        Users[i][1] = 3
                                        Users[i][9] = Curr_Area
                                        Users[i][10] = day_current + 1  # date of infection (since starts at 0)
                                        Users[i][16] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5]
                                        trans_Fom_User.append([Fomite[f][1], 'Patient', Curr_Area])
                                        # print(str(Time_var) + ": patient " + str(i) + " infected by " + Fomite[f][1] + " in " + Curr_Area)
                                # if patient is infectious, might contaminate fomite
                                elif Users[i][1] == 1 and Fomite[f][2] == "Uncontaminated":
                                    # tp_person_Fomite = random.random() < 0.5
                                    if (random.random() < tp_person_Fomite * pat_fom_recep * TP_Fom_Recep) == 1:
                                        Fomite[f][2] = "Contaminated"
                                        Fomite[f][3] = Duration_Fomite
                                        Fomite[f][4] = 1
                                        Fomite[f][8] = 'patient_' + str(i)
                                        Fomite[f][7] = Time_var
                                        trans_User_Fom.append([Fomite[f][1], 'Patient', Curr_Area])
                                        # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by patient " + str(i) + " in " + Curr_Area)
                        
                        # Attention areas: contact with BP cuff, 1 per room
                        if AT_UR == Curr_Area or (At_NU == Curr_Area and CURTAINS_INTRV == 0 and ATTEN_NU_INTRV == 0):
                            for room in Room_Fomite:
                                if Users[i][17] == room and Fomite[f][6] == room:
                                    # contact_occurs = random.random() < 0.5
                                    if (random.random() < contact_occurs) == 1:
                                        # if fomite is contaminated, might infect patient
                                        if Users[i][1] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]: 
                                            # tp_Fomite_person = random.random() < 0.5
                                            if (random.random() < tp_Fomite_person() * pat_fom_atten * TP_Fom_At_Ur) == 1:
                                                Users[i][1] = 3
                                                Users[i][9] = Curr_Area
                                                Users[i][10] = day_current + 1  # date of infection (since starts at 0)
                                                Users[i][16] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5] + '_' + room
                                                trans_Fom_User.append([Fomite[f][1], 'Patient', Curr_Area])
                                                # print(str(Time_var) + ": patient " + str(i) + " infected by " + Fomite[f][1] + " in " + Curr_Area)
                                        # if patient is infectious, might contaminate fomite
                                        elif Users[i][1] == 1 and Fomite[f][2] == "Uncontaminated":
                                            # tp_person_Fomite = random.random() < 0.5
                                            if (random.random() < tp_person_Fomite * pat_fom_atten * TP_Fom_At_Ur) == 1:
                                                Fomite[f][2] = "Contaminated"
                                                Fomite[f][3] = Duration_Fomite
                                                Fomite[f][4] = 1
                                                Fomite[f][8] = 'patient_' + str(i)
                                                Fomite[f][7] = Time_var
                                                trans_User_Fom.append([Fomite[f][1], 'Patient', Curr_Area])
                                                # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by patient " + str(i) + " in " + Curr_Area)
                        if At_NU == Curr_Area and (CURTAINS_INTRV == 1 or ATTEN_NU_INTRV == 1):
                            for room in Room_Fomite_Intervention:
                                if Users[i][15] == room and Fomite[f][6] == room:
                                    # contact_occurs = random.random() < 0.5
                                    if (random.random() < contact_occurs) == 1:
                                        # if fomite is contaminated, might infect patient
                                        if Users[i][1] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]: 
                                            # tp_Fomite_person = random.random() < 0.5
                                            if (random.random() < tp_Fomite_person() * pat_fom_atten * TP_Fom_At_NU_INT) == 1:
                                                Users[i][1] = 3
                                                Users[i][9] = Curr_Area
                                                Users[i][10] = day_current + 1  # date of infection (since starts at 0)
                                                Users[i][16] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5] + '_' + room 
                                                trans_Fom_User.append([Fomite[f][1], 'Patient', Curr_Area])
                                                # print(str(Time_var) + ": patient " + str(i) + " infected by " + Fomite[f][1] + " in " + Curr_Area)
                                        # if patient is infectious, might contaminate fomite
                                        elif Users[i][1] == 1 and Fomite[f][2] == "Uncontaminated":
                                            # tp_person_Fomite = random.random() < 0.5
                                            if (random.random() < tp_person_Fomite * pat_fom_atten * TP_Fom_At_NU_INT) == 1:
                                                Fomite[f][2] = "Contaminated"
                                                Fomite[f][3] = Duration_Fomite
                                                Fomite[f][4] = 1
                                                Fomite[f][8] = 'patient_' + str(i)
                                                Fomite[f][7] = Time_var
                                                trans_User_Fom.append([Fomite[f][1], 'Patient', Curr_Area])
                                                # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by patient " + str(i) + " in " + Curr_Area)
                        
                        # fomite cleaning after use/in case of visible soiling
                        # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                        if Fomite[f][2] == "Contaminated":
                            if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                                Fomite[f][2] = "Uncontaminated"
                                Fomite[f][3] = 0
                                Fomite[f][4] = 0
                                # print("Fomite cleaned after use")
                        
                #  -- ----            HCW and fomite interaction -------------------
                for j in range(len(HCW_pool)):
                    # determine hand washing
                    # if HCW_pool[j][20] > (Time_var + time_hand_clean):
                                        
                        # Reception: HCWs interact with counter and PC
                        if RECEP == Curr_Area:
                            # if fomite is contaminated, might infect HCW
                            if (HCW_pool[j][1] == 0 and HCW_pool[j][3] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]):
                                # tp_Fomite_person = random.random() < 0.5
                                if (random.random() < tp_Fomite_person() * hcw_fom_recep * TP_Fom_Recep) == 1:
                                    # HCW_pool[j][1] = 3
                                    # # NOTE: for below, check that positions in HCW_pool[i] are correct (use debug???)
                                    HCW_pool[j][5] = Curr_Area
                                    HCW_pool[j][3] = day_current + 1  # what does this line do?
                                    HCW_pool[j][6] = day_current + 1  # what does this line do?
                                    HCW_pool[j][15] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5]
                                    trans_Fom_HCW.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                    # print(str(Time_var) + ": " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " infected by " + Fomite[f][1] + str(f) + " in " + Curr_Area)
                            # if HCW is infectious, might contaminate fomite
                            elif (HCW_pool[j][1] == 1 and Fomite[f][2] == "Uncontaminated"):
                                # tp_person_Fomite = random.random() < 0.5
                                if (random.random() < tp_person_Fomite * hcw_fom_recep * TP_Fom_Recep) == 1:
                                    Fomite[f][2] = "Contaminated"
                                    Fomite[f][3] = Duration_Fomite
                                    Fomite[f][4] = 1
                                    Fomite[f][8] = HCW_pool[j][2] + '_num_' + str(HCW_pool[j][0])
                                    Fomite[f][7] = Time_var
                                    trans_HCW_Fom.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                    # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " in " + Curr_Area)
                        
                            # fomite cleaning after use/in case of visible soiling
                            # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                            if Fomite[f][2] == "Contaminated":
                                if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                                    Fomite[f][2] = "Uncontaminated"
                                    Fomite[f][3] = 0
                                    Fomite[f][4] = 0
                                    # print("Fomite cleaned after use") 
                        
                        # Attention areas: contact with BP cuff, 1 per room
                        if (AT_UR == Curr_Area or (At_NU == Curr_Area and CURTAINS_INTRV == 0 and ATTEN_NU_INTRV == 0)):  # ToDo: do I need to figure out which room HCW is in at that time and restrict to that room?
                            for room in Room_Fomite:
                                if ((HCW_pool[j][20][0] == room 
                                     or HCW_pool[j][20][1] == room 
                                     or HCW_pool[j][20][2] == room 
                                     or HCW_pool[j][20][3] == room) 
                                    and Fomite[f][6] == room):
                                    # contact_occurs = random.random() < 0.5
                                    if (random.random() < contact_occurs) == 1:
                                        # if fomite is contaminated, might infect HCW
                                        if (HCW_pool[j][1] == 0 and HCW_pool[j][3] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]):
                                            # tp_Fomite_person = random.random() < 0.5
                                            if (random.random() < tp_Fomite_person() * hcw_fom_atten * TP_Fom_At_Ur) == 1:
                                                # HCW_pool[j][1] = 3
                                                # # NOTE: for below, check that positions in HCW_pool[i] are correct (use debug???)
                                                HCW_pool[j][5] = Curr_Area
                                                HCW_pool[j][3] = day_current + 1  # what does this line do?
                                                HCW_pool[j][6] = day_current + 1  # what does this line do?
                                                HCW_pool[j][15] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5]
                                                trans_Fom_HCW.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                                # print(str(Time_var) + ": " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " infected by " + Fomite[f][1] + str(f) + " in " + Curr_Area)
                                        # if HCW is infectious, might contaminate fomite
                                        elif (HCW_pool[j][1] == 1 and Fomite[f][2] == "Uncontaminated"):
                                            # tp_person_Fomite = random.random() < 0.5
                                            if (random.random() < tp_person_Fomite * hcw_fom_atten * TP_Fom_At_Ur) == 1:
                                                Fomite[f][2] = "Contaminated"
                                                Fomite[f][3] = Duration_Fomite
                                                Fomite[f][4] = 1
                                                Fomite[f][8] = HCW_pool[j][2] + '_num_' + str(HCW_pool[j][0])
                                                Fomite[f][7] = Time_var
                                                trans_HCW_Fom.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                                # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " in " + Curr_Area)
                        
                            # fomite cleaning after use/in case of visible soiling
                            # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                            if Fomite[f][2] == "Contaminated":
                                if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                                    Fomite[f][2] = "Uncontaminated"
                                    Fomite[f][3] = 0
                                    Fomite[f][4] = 0
                                    # print("Fomite cleaned after use")             
                        
                        if (At_NU == Curr_Area and (CURTAINS_INTRV == 1 or ATTEN_NU_INTRV == 1)):
                            for room in Room_Fomite_Intervention:
                                if (Fomite[f][6] == room and (HCW_pool[j][16] == room or 
                                                       HCW_pool[j][18] == room)):
                                    # if fomite is contaminated, might infect HCW
                                    if (HCW_pool[j][1] == 0 and HCW_pool[j][3] == 0 and Fomite[f][2] == "Contaminated" and Fomite[f][3]>=Fomite[f][4]):
                                        # tp_Fomite_person = random.random() < 0.5
                                        if (random.random() < tp_Fomite_person() * hcw_fom_atten * TP_Fom_At_NU_INT) == 1:
                                            # HCW_pool[j][1] = 3
                                            # # NOTE: for below, check that positions in HCW_pool[i] are correct (use debug???)
                                            HCW_pool[j][5] = Curr_Area
                                            HCW_pool[j][3] = day_current + 1  # what does this line do?
                                            HCW_pool[j][6] = day_current + 1  # what does this line do?
                                            HCW_pool[j][15] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5]
                                            trans_Fom_HCW.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                            # print(str(Time_var) + ": " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " infected by " + Fomite[f][1] + str(f) + " in " + Curr_Area)
                                    # if HCW is infectious, might contaminate fomite
                                    elif (HCW_pool[j][1] == 1 and Fomite[f][2] == "Uncontaminated"):
                                        # tp_person_Fomite = random.random() < 0.5
                                        if (random.random() < tp_person_Fomite * hcw_fom_atten * TP_Fom_At_NU_INT) == 1:
                                            Fomite[f][2] = "Contaminated"
                                            Fomite[f][3] = Duration_Fomite
                                            Fomite[f][4] = 1
                                            Fomite[f][8] = HCW_pool[j][2] + '_num_' + str(HCW_pool[j][0])
                                            Fomite[f][7] = Time_var
                                            trans_HCW_Fom.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                            # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " in " + Curr_Area)
                        
                            # fomite cleaning after use/in case of visible soiling
                            # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                            if Fomite[f][2] == "Contaminated":
                                if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                                    Fomite[f][2] = "Uncontaminated"
                                    Fomite[f][3] = 0
                                    Fomite[f][4] = 0
                                    # print("Fomite cleaned after use")         
                        
                        # ED Base
                        if HCW_B == Curr_Area:
                            # some chance of touching fomites
                            # contact_occurs = random.random() < 0.5
                            if (random.random() < (contact_occurs * TP_multiplier)) == 1:
                                # if fomite is contaminated, might infect HCW
                                if (HCW_pool[j][1] == 0 and HCW_pool[j][3] == 0 and 
                                    Fomite[f][2] == "Contaminated" and 
                                    Fomite[f][3]>=Fomite[f][4]):
                                    # tp_Fomite_person = random.random() < 0.5
                                    if (random.random() < tp_Fomite_person() * hcw_fom_nurse * TP_Fom_HCW_B) == 1:
                                        # HCW_pool[j][1] = 3
                                        # # NOTE: for below, check that positions in HCW_pool[i] are correct (use debug???)
                                        HCW_pool[j][5] = Curr_Area
                                        HCW_pool[j][3] = day_current + 1  # what does this line do?
                                        HCW_pool[j][6] = day_current + 1  # what does this line do?
                                        HCW_pool[j][15] = 'Fomite_' + Fomite[f][1] + '_' + Fomite[f][5]
                                        trans_Fom_HCW.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                        # print(str(Time_var) + ": " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " infected by " + Fomite[f][1] + str(f) + " in " + Curr_Area)
                                # if HCW is infectious, might contaminate fomite
                                elif (HCW_pool[j][1] == 1 and Fomite[f][2] == "Uncontaminated"):
                                    # tp_person_Fomite = random.random() < 0.5
                                    if (random.random() < tp_person_Fomite * hcw_fom_nurse * TP_Fom_HCW_B) == 1:
                                        Fomite[f][2] = "Contaminated"
                                        Fomite[f][3] = Duration_Fomite
                                        Fomite[f][4] = 1
                                        Fomite[f][8] = HCW_pool[j][2] + '_num_' + str(HCW_pool[j][0])
                                        Fomite[f][7] = Time_var
                                        trans_HCW_Fom.append([Fomite[f][1], HCW_pool[j][2], Curr_Area])
                                        # print(str(Time_var) + ": " + Fomite[f][1] + str(f) + " contaminated by " + HCW_pool[j][2] + str(HCW_pool[j][0]) + " in " + Curr_Area)
                            
                            # fomite cleaning after use/in case of visible soiling
                            # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                            if Fomite[f][2] == "Contaminated":
                                if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                                    Fomite[f][2] = "Uncontaminated"
                                    Fomite[f][3] = 0
                                    Fomite[f][4] = 0
                                    # print("Fomite cleaned after use")            
                            
                        # if (random.random() < wash_hand_post_fom * wash_hand_effectiveness):
                            # HCW_pool[j][20] = Time_var
                                    
                # # fomite cleaning after use/in case of visible soiling
                # # assume cleaning occurs some % of the time (could also make this differ by area/fomite)
                # if Fomite[f][2] == "Contaminated":
                #     if (random.random() < (probability_clean_fomite*prob_fomite_uncontam_after_clean)) == 1:
                #         Fomite[f][2] = "Uncontaminated"
                #         Fomite[f][3] = 0
                #         Fomite[f][4] = 0
                #         # print("Fomite cleaned after use")
    
    #  -- ----            Fomite toy task close -------------------
    
    return #print("Fomite routine complete")

# def fomite_function_WAI(Curr_Area, which_foms=all_foms, TP_multiplier=1):
def fomite_function_WAI(Curr_Area, TP_multiplier=1):                     
    # Holding area: patient interacts with chair
    if WAI_N == Curr_Area:
        if WAIT_NU_INTRV == 0:
            number_chairs = number_chairs_holding
            holding_area_room = ["WAT_ROM"]
            TP_Fom_Waitg = TP_Fom_WaiNU
        if WAIT_NU_INTRV == 1:
            number_chairs = number_chairs_holding_int
            holding_area_room = ["WAT_ROM_1", "WAT_ROM_2"]
            TP_Fom_Waitg = TP_Fom_WaiNU_INT
        
        for room in holding_area_room:
            # choosing a chair
            c_options = list(range(1, number_chairs + 1))
            
            # first remove chairs occupied by people already in holding area
            
            # for i in range(len(Users)):
            #     if ((Users[i][2] == Curr_Area or Users[i][2] == At_NU) and 
            #         (Users[i][5] <= Time_var) and (Users[i][13] == room)):
                    
            #         if Users[i][18] != 0:
            #             c_options.remove(Users[i][18])
                        
            # next occupy chairs for new users and run interaction between users and chairs
            for i in range(len(Users)):
                if Users[i][2] == Curr_Area and Users[i][5] <= Time_var and Users[i][13] == room:
                    if Users[i][18] == 0:
                        Users[i][18] = random.choice(c_options)
                        c_options.remove(Users[i][18])
                    c = Users[i][18] - 1
                    if room == "WAT_ROM_2":
                        c = Users[i][18] - 1 + number_chairs_holding_int
                    # check that chair is in same room as patient
                    # if Fomite[2][c][6] != Users[i][13]:
                        # print("Error! Fomite not in room")
                    if Users[i][1] == 0 and Fomite[2][c][2] == "Contaminated" and Fomite[2][c][3]>=Fomite[2][c][4]:
                        # interact with chair
                        if (random.random() < tp_Fomite_person() * pat_fom_waitg * prolonged_contact * TP_Fom_Waitg) == 1:
                            Users[i][1] = 3
                            Users[i][9] = Curr_Area
                            Users[i][10] = day_current + 1  # date of infection (since starts at 0)
                            Users[i][16] = 'Fomite_' + Fomite[2][c][1] + '_' + Fomite[2][c][5]
                            trans_Fom_User.append([Fomite[2][c][1], 'Patient', Curr_Area])
                            # print(str(Time_var) + ": patient " + str(i) + " infected by Chair " + str(Fomite[2][c][0]) + " in " + Curr_Area)
                    # if patient is infectious, might contaminate fomite
                    elif Users[i][1] == 1 and Fomite[2][c][2] == "Uncontaminated":
                        # interact with chair
                        if (random.random() < tp_person_Fomite * pat_fom_waitg * prolonged_contact * TP_Fom_Waitg) == 1:
                            Fomite[2][c][2] = "Contaminated"
                            Fomite[2][c][3] = Duration_Fomite
                            Fomite[2][c][4] = 1
                            Fomite[2][c][8] = 'patient_' + str(i)
                            Fomite[2][c][7] = Time_var
                            trans_User_Fom.append([Fomite[2][c][1], 'Patient', Curr_Area])
                            # print(str(Time_var) + ": Chair " + str(c+1) + " contaminated by patient " + str(i) + " in " + Curr_Area)
                        
    
    #  -- ----            Fomite toy task close -------------------
    
    return #print("Fomite routine complete")

# # Function for fomite cleaning (alternative to have a chance of cleaning after every interaction)
# def fomite_cleaning(Curr_Area, prob_cleaning, Fomite_subset=Fomite):
#     # global Time_var
#     for Fom in Fomite_subset:
#         if Fom[5] == Curr_Area:
#             if Fom[2] == "Contaminated":
#                 if (random.random() < prob_cleaning) == 1:
#                     Fom[2] = "Uncontaminated"
#                     Fom[3] = 0
#                     Fom[4] = 0
                    
#     return


"""----------------------------------------------------------------------------
                          Main function
""" 
def main_funct():
    global Time_var, ROMS_G, BEDS_G
    N_new_day_from_w = []
    N_new_day_work = []
    N_new_day = []
    N_waiting_H = []
    
    Result_worker = []
    
    N_new_day_from_shift_1 = []
    N_new_day_from_shift_2 = []
    N_new_day_from_shift_3 = []
    
    HCW_inf_1 = []
    HCW_inf_2 = []
    HCW_inf_3 = []
    
    port_RECEP_from_shift_1  =[]
    port_TRIAG_from_shift_1 =[]
    port_TRIAG_U_from_shift_1  =[]
    port_N_URG_from_shift_1 =[]
    port_N_N_URG_from_shift_1  =[]
    port_DR_URGE_from_shift_1  =[]
    port_DR_N_URG_from_shift_1 =[]
    port_IMAGI_from_shift_1 =[]
    port_LABOR_from_shift_1 =[]
    port_ARE_test_from_shift_1 =[]
    
    port_RECEP_from_shift_2  =[]
    port_TRIAG_from_shift_2 =[]
    port_TRIAG_U_from_shift_2  =[]
    port_N_URG_from_shift_2 =[]
    port_N_N_URG_from_shift_2  =[]
    port_DR_URGE_from_shift_2  =[]
    port_DR_N_URG_from_shift_2 =[]
    port_IMAGI_from_shift_2 =[]
    port_LABOR_from_shift_2 =[]
    port_ARE_test_from_shift_2 =[]
    
    port_RECEP_from_shift_3  =[]
    port_TRIAG_from_shift_3 =[]
    port_TRIAG_U_from_shift_3  =[]
    port_N_URG_from_shift_3 =[]
    port_N_N_URG_from_shift_3  =[]
    port_DR_URGE_from_shift_3  =[]
    port_DR_N_URG_from_shift_3 =[]
    port_IMAGI_from_shift_3 =[]
    port_LABOR_from_shift_3 =[]
    port_ARE_test_from_shift_3 =[]
    
    
    
    RECEP_from_shift_1 = []
    TRIAG_from_shift_1 = []
    TRIAG_U_from_shift_1 = []
    N_URG_from_shift_1 = []
    N_N_URG_from_shift_1 = []
    IMAGI_from_shift_1 = []
    LABOR_from_shift_1 = []
    DR_URGE_from_shift_1 = []
    DR_N_URG_from_shift_1 = []
    ARE_test_from_shift_1 = []
                           
    RECEP_from_shift_2 = []
    TRIAG_from_shift_2 = []
    TRIAG_U_from_shift_2 = []
    N_URG_from_shift_2 = []
    N_N_URG_from_shift_2 = []
    IMAGI_from_shift_2 = []
    LABOR_from_shift_2 = []
    DR_URGE_from_shift_2 = []
    DR_N_URG_from_shift_2 = []
    ARE_test_from_shift_2 = []
    
    RECEP_from_shift_3 = []
    TRIAG_from_shift_3 = []
    TRIAG_U_from_shift_3 = []
    N_URG_from_shift_3 = []
    N_N_URG_from_shift_3 = []
    IMAGI_from_shift_3 = []
    LABOR_from_shift_3 = []
    DR_URGE_from_shift_3 = []
    DR_N_URG_from_shift_3 = []
    ARE_test_from_shift_3 = []
    
    Recep_port = []
    Triag_port = []
    WaitU_port = []
    WaitN_port = []
    AtteU_port = []
    AtteN_port = []
    Imagi_port = []
    Labot_port = []
    
    Recep_port_HCW = []
    Triag_port_HCW = []
    AtteU_port_HCW = []
    AtteN_port_HCW = []
    Imagi_port_HCW = []
    Labot_port_HCW = []
    Base1_port_HCW = []
    Base2_port_HCW = []
    Base3_port_HCW = []
    
    Pat_new_Fom = []
    HCW_new_Fom = []
    Fomite_new = []
    
    Recep_propo = 0
    Triag_propo = 0
    WaitU_propo = 0
    WaitN_propo = 0
    AtteU_propo = 0
    AtteN_propo = 0
    Imagi_propo = 0
    Labot_propo = 0
    
    Recep_prop_H = 0
    Triag_prop_H = 0
    AtteU_prop_H = 0
    AtteN_prop_H = 0
    Imagi_prop_H = 0
    Labot_prop_H = 0
    Base1_prop_H = 0
    Base2_prop_H = 0
    Base3_prop_H = 0
    
     
    Result_user = []
    result_monthly = []

    # nday  = 10
    # nday  = 10
    nday = 30
    for day in range(nday):
        day_current = day
        arrival_method(Time_var)
        
        day_inf = day_cases[day_current]
        if day_inf > 0:
            infec = np.random.randint(1,len(Users), size=(day_inf))

            for i in range(len(infec)):
                Users[infec[i]][1] = 1
                Users[infec[i]][9] = INFEC
        
        if WAIT_NU_INTRV == 0:
            for i in range(len(Users)):
                if Users[i][2] == 'RECEPTION':
                    Users[i][13] = 'WAT_ROM'
        if WAIT_NU_INTRV:
            for i in range(len(Users)):
                if Users[i][2] == 'RECEPTION':
                    ROOM_W = np.random.randint(1,3) # patient to room 1 or 2 in WNU
                    if 1 == ROOM_W:
                        Users[i][13] = 'WAT_ROM_1'
                    else:
                        Users[i][13] = 'WAT_ROM_2'
            
        while Time_var < Time_scale:
            # if (Time_var >= shift_1[0]) and (Time_var <= shift_1[1]):
                # arrival_method(Time_var)
            for k in range(len(Users)):
                if Users[k][5] == Time_var:  # time to enter next area
                    Users[k][4] = 1  # reset to set time in area
                    
                if (Users[k][5] < Time_var) and (Users[k][4] < Users[k][3]):  # double check conditions are met
                    Curr_time = Users[k][4]
                    Users[k][4] = Curr_time + 1
                    
                if (Users[k][4] == Users[k][3]) and (Users[k][5] < Time_var) and (Users[k][2] != EXIT_):  
                    # area time counter = area time
                    action_desit_tree(Users[k], k, day, Time_var)         
                    area_desit_tree(Users[k],k)
            
            for Fom in Fomite:
                if Fom[2] == "Contaminated" and Fom[3] > Fom[4]:  # note didn't ahve second condition
                    Fom[4] += 1  # count minutes
                
                # set fomite to uncontaminated if duration of contamination has been exceeded
                if Fom[2] == "Contaminated" and Fom[3] <= Fom[4]:
                    Fom[2] = "Uncontaminated"
                    Fom[3] = 0
                    Fom[4] = 0
                    # print("Fomite duration exceeded")
                    
                # daily fomite cleaning
                if Fom[2] == "Contaminated":
                    if Time_var == daily_cleaning_time:
                        if (random.random() < prob_fomite_uncontam_after_clean) == 1:
                            Fom[2] = "Uncontaminated"
                            Fom[3] = 0
                            Fom[4] = 0
                            # print("Fomite cleaned")
            
            # ---------- fomites ------
            
            # Run fomite_function every 5 minutes in attention areas
            if Time_var % 5 == 0 and Time_var != 0:  # if Time_var is a multiple of 5
                # fomite_function(HCW_pool, Curr_Area)  # original location
                if Time_var <= shift_2[1] and Time_var >= shift_2[0]:  # just > or >= ?
                    # shift_num = "2"
                    HCW_pool = V_nurse_No_Urg_2 + dr_No_Urg_V_2
                if Time_var <= shift_3[1] and Time_var >= shift_3[0]:
                    # shift_num = "3"
                    HCW_pool = V_nurse_No_Urg_3 + dr_No_Urg_V_3
                if Time_var <= shift_1[1] and Time_var >= shift_1[0]:
                    # shift_num = "1"
                    HCW_pool = V_nurse_No_Urg_1 + dr_No_Urg_V_1
                fomite_function(HCW_pool, AT_UR)
                fomite_function(HCW_pool, At_NU)
                
                # List_Areas = (RECEP, TRIAG, WAI_U, WAI_N, AT_UR, At_NU, IMAGI, LABOR, HCW_B)
                # for Curr_Area in List_Areas:
                #     # if Curr_Area == RECEP:
                #     #     if shift_num == "2":
                #     #         HCW_pool = V_recep_2 #[V_recep_2[0], V_recep_2[1]]
                #     #     elif shift_num == "3":
                #     #         HCW_pool = V_recep_3 #[V_recep_3[0]]
                #     #     elif shift_num == "1":
                #     #         HCW_pool = V_recep_1 #[V_recep_1[0], V_recep_1[1], V_recep_1[2]]
                #     # elif Curr_Area == TRIAG: # what about TRIAG_U?
                #     #     if shift_num == "2":
                #     #         HCW_pool = V_triag_2 #[V_triag_2[0], V_triag_2[1]]
                #     #     elif shift_num == "3":
                #     #         HCW_pool = V_triag_3 #[V_triag_3[0]]
                #     #     elif shift_num == "1":
                #     #         HCW_pool = V_triag_1 #[V_triag_1[0], V_triag_1[1]]
                #     # elif Curr_Area == WAI_U or Curr_Area == WAI_N:
                #     #     HCW_pool = []
                #     elif Curr_Area == AT_UR or Curr_Area == At_NU:
                #         if shift_num == "2":
                #             HCW_pool = V_nurse_No_Urg_2 + dr_No_Urg_V_2
                #             # HCW_pool = [V_nurse_No_Urg_2[0], V_nurse_No_Urg_2[1], V_nurse_No_Urg_2[2], V_nurse_No_Urg_2[3], 
                #             #             dr_No_Urg_V_2[0], dr_No_Urg_V_2[1], dr_No_Urg_V_2[2], dr_No_Urg_V_2[3]]
                #         elif shift_num == "3":
                #             HCW_pool = V_nurse_No_Urg_3 + dr_No_Urg_V_3
                #             # HCW_pool = [V_nurse_No_Urg_3[0], V_nurse_No_Urg_3[1], V_nurse_No_Urg_3[2],
                #             #             dr_No_Urg_V_3[0], dr_No_Urg_V_3[1], dr_No_Urg_V_3[2]]
                #         elif shift_num == "1":
                #             HCW_pool = V_nurse_No_Urg_1 + dr_No_Urg_V_1
                #             # HCW_pool = [V_nurse_No_Urg_1[0], V_nurse_No_Urg_1[1], V_nurse_No_Urg_1[2], V_nurse_No_Urg_1[3],
                #             #             dr_No_Urg_V_1[0], dr_No_Urg_V_1[1], dr_No_Urg_V_1[2], dr_No_Urg_V_1[3]]
                #         # run every 5 minutes
                #         fomite_function(HCW_pool, AT_UR)
                #         fomite_function(HCW_pool, At_NU)
                #     # elif Curr_Area == IMAGI:
                #     #     if shift_num == "2":
                #     #         HCW_pool = V_imagin_2 #[V_imagin_2[0], V_imagin_2[1]]
                #     #     elif shift_num == "3":
                #     #         HCW_pool = V_imagin_3 #[V_imagin_3[0], V_imagin_3[1]]
                #     #     elif shift_num == "1":
                #     #         HCW_pool = V_imagin_1 #[V_imagin_1[0], V_imagin_1[1]]
                #     # elif Curr_Area == LABOR:
                #     #     if shift_num == "2":
                #     #         HCW_pool = V_labor_2 #[V_labor_2[0]]
                #     #     elif shift_num == "3":
                #     #         HCW_pool = V_labor_3 #[V_labor_3[0]]
                #     #     elif shift_num == "1":
                #     #         HCW_pool = V_labor_1 #[V_labor_1[0]]
                #     elif HCW_B == Curr_Area:
                #         if shift_num == "2":
                #             HCW_pool = V_recep_2 + V_triag_2 + V_nurse_No_Urg_2 + dr_No_Urg_V_2 + V_imagin_2 + V_labor_2
                #         elif shift_num == "3":
                #             HCW_pool = V_recep_3 + V_triag_3 + V_nurse_No_Urg_3 + dr_No_Urg_V_3 + V_imagin_3 + V_labor_3
                #         elif shift_num == "1":
                #             HCW_pool = V_recep_1 + V_triag_1 + V_nurse_No_Urg_1 + dr_No_Urg_V_1 + V_imagin_1 + V_labor_1
                #         # run every 5 minutes
                #         if NB_ROOM == 0:
                #             fomite_function(HCW_pool, HCW_B, (7,8))
                #         elif NB_ROOM == 1:
                #             fomite_function(HCW_pool, HCW_B, (7,8), 0.5)
                    
            # Cleaning routine (decide how/when we want to handle cleaning)
            # # Check if fomites need to be cleaned every 5 minutes (1 minute after fomite interactions above)
            # if Time_var % 5 == 1:
            #     fomite_cleaning(AT_UR, 0.5)
            #     fomite_cleaning(At_NU, 0.5)
            #     fomite_cleaning(HCW_B, 0.5, [Fomite[7], Fomite[8]])
            # ---------- END FOMITES ----------
            
            # ---------- HWC MEETING PER AREA IN NORMAL WORK END SHIFTS ------
            
            # if shift_1[0] == Time_var:
            #     meet_HCW_1()
            
            # if shift_2[0] == Time_var:
            #     meet_HCW_2()
                
            # if shift_3[0] == Time_var:
            #     meet_HCW_3()
    
            
            #SCREE_HCW 
            # if (shift_2[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_2 = staff_shift[1]
                
            #     for i in range(len(Users_workers_shift_2)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_2[i][1] != 0 
            #             and (PCR_test)):
            #             Users_workers_shift_2[i][8] = REPLACE
            #             Users_workers_shift_2[i][1] = 0
            #             Users_workers_shift_2[i][4] = 0
            #             Users_workers_shift_2[i][5] = UNDEF
            #             Users_workers_shift_2[i][6] = 0
            #             Users_workers_shift_2[i][7] = UNDEF
            #             Users_workers_shift_2[i][9] = UNDEF
            #             Users_workers_shift_2[i][10] = UNDEF
            #             Users_workers_shift_2[i][11] = 0
            #             Users_workers_shift_2[i][12] = 0
            #             #Users_workers_shift_1[i][13] = 0
            #             Users_workers_shift_2[i][14] = UNDEF
            
            if shift_2[0] == Time_var:
                meet_HCW_2()
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 1 and 2  -------   
            if Time_var == shift_2[0]:
                N_HCW_inf_tot = 0
                N_HCW_inf_1 = 0
                N_HCW_inf_2 = 0
                Users_workers_shift_1 = []
                Users_workers_shift_2= []
                Users_workers_shift_3= []
                # Create worker_shifts 
                staff_shift  = workers_settings(Users_workers_shift_1, 
                                                Users_workers_shift_2, 
                                                Users_workers_shift_3)
                Users_workers_shift_1 = staff_shift[0]
                Users_workers_shift_2 = staff_shift[1]
                # Users_workers_shift_3 = staff_shift[2]
                
                # ------- Interv SPLIT Burse base
                # 1- Size of both HCWs groups of the shift
                # 2. From size, rand select half of each group to meet the other
                #    rand half or the other group
                # 3. For each half, apply room characterit.
                
                # NB_SPLIT = 1
                if NB_SPLIT:
                    ROOM_1 = 1
                    ROOM_2 = 1            
                    
                    G_1 = random.sample(range(0, len(Users_workers_shift_1)), 
                                        (int((len(Users_workers_shift_1))/2)) )
                    G_2 = random.sample(range(0, len(Users_workers_shift_2)), 
                                        (int((len(Users_workers_shift_2))/2)) )
                    
                    G_H_1 = []
                    G_H_1_2 = []
                    G_H_2 = []
                    G_H_2_2 = []
                    for i in range(len(G_1)):
                        G_H_1.append((Users_workers_shift_1[G_1[i]]))
                    for i in range(len(Users_workers_shift_1)):
                        if (not(Users_workers_shift_1[i] in G_H_1)):
                            G_H_1_2.append(Users_workers_shift_1[i])
                    
                    for i in range(len(G_2)):
                        G_H_2.append((Users_workers_shift_2[G_2[i]]))
                    for i in range(len(Users_workers_shift_2)):
                        if (not(Users_workers_shift_2[i] in G_H_2)):
                            G_H_2_2.append(Users_workers_shift_2[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_1)):
                            if G_H_1[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_1[i])
                        for i in range(len(G_H_2)):
                            if G_H_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        # print(N_HCW_inf_tot)
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            TP = TP * TP_Farf_HCW_B_INT
           
                            for i in range(len(G_H_1)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_1[i][1] == 0 and 
                                        G_H_1[i][6] == 0):
                                        i_n = Users_workers_shift_1.index(G_H_1[i])
                                        Users_workers_shift_1[i_n][3] = day_current + 1 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE'
                          
                            for i in range(len(G_H_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2[i][1] == 0 and 
                                        G_H_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2)-1)
                                if (G_H_2[Sus_2][1] == 0 and 
                                                    G_H_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_1)-1)
                                if (G_H_1[Sus_1][1] == 0 and 
                                                    G_H_1[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1[Sus_1])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1
                                        
                        # fomites
                        HCW_pool = G_H_1 + G_H_2
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_1_2)):
                            if G_H_1_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_1_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        # print(N_HCW_inf_tot)
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                                TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                             N_HCW_inf_tot]*TP_pyth
                                # TP = TP * Nur_B_fact
                                # TP = TP * T_NB
                                TP = TP * TP_Farf_HCW_B
               
                                for i in range(len(G_H_1_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_1_2[i][1] == 0 and 
                                            G_H_1_2[i][6] == 0):
                                            i_n = Users_workers_shift_1.index(G_H_1_2[i])
                                            Users_workers_shift_1[i_n][3] = day_current + 1 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE'
                              
                                for i in range(len(G_H_2_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_2_2[i][1] == 0 and 
                                            G_H_2_2[i][6] == 0):
                                            i_n = Users_workers_shift_2.index(G_H_2_2[i])
                                            Users_workers_shift_2[i_n][3] = day_current + 1 
                                            Users_workers_shift_2[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                if (G_H_2_2[Sus_2][1] == 0 and 
                                                    G_H_2_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_1_2)-1)
                                if (G_H_1_2[Sus_1][1] == 0 and 
                                                    G_H_1_2[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1_2[Sus_1])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1
                                        
                        # fomites
                        HCW_pool = G_H_1_2 + G_H_2_2
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                                     
                    #    ----------  Close Near Field  ----------------------------  
                    
                    # # ------- fomites
                    # # if fomites treated as 50% probability of non-ED base intervention -- can do it differently, but relies on being able t:
                    # HCW_pool = [V_recep_1[0], V_recep_1[1], V_recep_1[2],
                    #             V_triag_1[0], V_triag_1[1],
                    #             V_nurse_No_Urg_1[0], V_nurse_No_Urg_1[1], V_nurse_No_Urg_1[2], V_nurse_No_Urg_1[3],
                    #             dr_No_Urg_V_1[0], dr_No_Urg_V_1[1], dr_No_Urg_V_1[2], dr_No_Urg_V_1[3],
                    #             V_imagin_1[0], V_imagin_1[1],
                    #             V_labor_1[0],
                    #             V_recep_2[0], V_recep_2[1],
                    #             V_triag_2[0], V_triag_2[1],
                    #             V_nurse_No_Urg_2[0], V_nurse_No_Urg_2[1], V_nurse_No_Urg_2[2], V_nurse_No_Urg_2[3],
                    #             dr_No_Urg_V_2[0], dr_No_Urg_V_2[1], dr_No_Urg_V_2[2], dr_No_Urg_V_2[3],
                    #             V_imagin_2[0], V_imagin_2[1],
                    #             V_labor_2[0]]
                    # fomite_function(HCW_pool, HCW_B, [Fomite[9], Fomite[10]], 0.5)
                    # ------- Close intervention
                
                else:
                
                    Inf_H_1 = []
                    Inf_H_2 = []
                    for i in range(len(Users_workers_shift_1)):
                        if Users_workers_shift_1[i][1] == 1:
                            N_HCW_inf_1 = N_HCW_inf_1 + 1
                            Inf_H_1.append(Users_workers_shift_1[i])
                    for i in range(len(Users_workers_shift_2)):
                        if Users_workers_shift_2[i][1] == 1:
                            N_HCW_inf_2 = N_HCW_inf_2 + 1
                            Inf_H_2.append(Users_workers_shift_2[i])
                    N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                         
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                        
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            # TP = TP * Labor_fact
                            # # TP = TP*TP_pyth*TP_major
                            # TP = TP*TP_pyth*1
                            # TP_major = 1
                            TP = TP * TP_Farf_HCW_B_INT
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            
                            TP = TP * TP_Farf_HCW_B
                            
                        for i in range(len(Users_workers_shift_1)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if (Users_workers_shift_1[i][1] == 0 and 
                                    Users_workers_shift_1[i][6] == 0):
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_1[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_1[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff2_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_2)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if (Users_workers_shift_2[i][1] == 0 and 
                                    Users_workers_shift_2[i][6] == 0):
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_2[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_2[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff2_HCW_BASE'
                
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_1) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_2)-1)
                        if (Users_workers_shift_2[Sus_2][1] == 0 and 
                                            Users_workers_shift_2[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, 
                            #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_2[Sus_2][3] = day_current + 1
                                Users_workers_shift_2[Sus_2][5] = 'Staff1_HCW_BASE' 
                                Users_workers_shift_2[Sus_2][6] = day_current + 1 
                    if len(Inf_H_2) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_1)-1)
                        if (Users_workers_shift_1[Sus_1][1] == 0 and 
                                            Users_workers_shift_1[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, 
                            #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_1[Sus_1][3] = day_current + 1
                                Users_workers_shift_1[Sus_1][5] = 'Staff2_HCW_BASE' 
                                Users_workers_shift_1[Sus_1][6] = day_current + 1
                    #    ----------  Close Near Field  ----------------------------
                
                    # ------- Fomites
                    # HCW_pool = [V_recep_1[0], V_recep_1[1], V_recep_1[2],
                    #             V_triag_1[0], V_triag_1[1],
                    #             V_nurse_No_Urg_1[0], V_nurse_No_Urg_1[1], V_nurse_No_Urg_1[2], V_nurse_No_Urg_1[3],
                    #             dr_No_Urg_V_1[0], dr_No_Urg_V_1[1], dr_No_Urg_V_1[2], dr_No_Urg_V_1[3],
                    #             V_imagin_1[0], V_imagin_1[1],
                    #             V_labor_1[0],
                    #             V_recep_2[0], V_recep_2[1],
                    #             V_triag_2[0], V_triag_2[1],
                    #             V_nurse_No_Urg_2[0], V_nurse_No_Urg_2[1], V_nurse_No_Urg_2[2], V_nurse_No_Urg_2[3],
                    #             dr_No_Urg_V_2[0], dr_No_Urg_V_2[1], dr_No_Urg_V_2[2], dr_No_Urg_V_2[3],
                    #             V_imagin_2[0], V_imagin_2[1],
                    #             V_labor_2[0]]
                    HCW_pool = Users_workers_shift_1 + Users_workers_shift_2
                    # run light and door once on entry
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_once)
                    # run PC and sink 3-5 times for repeated contact
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    
            # Cleaning routine (decide how/when we want to handle cleaning)
            # if Time_var == (shift_2[0] + 1):
            #     fomite_cleaning(HCW_B, 0.5, [Fomite[9], Fomite[10]])
            # ------- End fomites
                
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 2 and 3  -------
            # if (shift_3[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_3 = staff_shift[2]
                
            #     for i in range(len(Users_workers_shift_3)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_3[i][1] != 0 
            #             and (PCR_test)):
            #             # and Users_workers_shift_2[i][9] == 'infectious'):
            #             Users_workers_shift_3[i][8] = REPLACE
            #             Users_workers_shift_3[i][1] = 0
            #             Users_workers_shift_3[i][4] = 0
            #             Users_workers_shift_3[i][5] = UNDEF
            #             Users_workers_shift_3[i][6] = 0
            #             Users_workers_shift_3[i][7] = UNDEF
            #             Users_workers_shift_3[i][9] = UNDEF
            #             Users_workers_shift_3[i][10] = UNDEF
            #             Users_workers_shift_3[i][11] = 0
            #             Users_workers_shift_3[i][12] = 0
            #             Users_workers_shift_3[i][14] = UNDEF
            
            if shift_3[0] == Time_var:
                meet_HCW_3()
            
            if Time_var == shift_3[0]:
                N_HCW_inf_tot = 0
                N_HCW_inf_2 = 0
                N_HCW_inf_3 = 0
                Users_workers_shift_1 = []
                Users_workers_shift_2= []
                Users_workers_shift_3= []
                # Create worker_shifts 
                staff_shift  = workers_settings(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3)
                Users_workers_shift_1 = staff_shift[0]
                Users_workers_shift_2 = staff_shift[1]
                Users_workers_shift_3 = staff_shift[2]
                
                # ------- Interv SPLIT Burse base
                # 1- Size of both HCWs groups of the shift
                # 2. From size, rand select half of each group to meet the other
                #    rand half or the other group
                # 3. For each half, apply room characterit.
                
                if NB_SPLIT:
                    ROOM_1 = 1
                    ROOM_2 = 1
                    
                    G_3 = random.sample(range(0, len(Users_workers_shift_3)), 
                                        (int((len(Users_workers_shift_3))/2)) )
                    G_2 = random.sample(range(0, len(Users_workers_shift_2)), 
                                        (int((len(Users_workers_shift_2))/2)) )
                    
                    G_H_3 = []
                    G_H_3_2 = []
                    G_H_2 = []
                    G_H_2_2 = []
                    for i in range(len(G_3)):
                        G_H_3.append((Users_workers_shift_3[G_3[i]]))
                    for i in range(len(Users_workers_shift_3)):
                        if (not(Users_workers_shift_3[i] in G_H_3)):
                            G_H_3_2.append(Users_workers_shift_3[i])
                    
                    for i in range(len(G_2)):
                        G_H_2.append((Users_workers_shift_2[G_2[i]]))
                    for i in range(len(Users_workers_shift_2)):
                        if (not(Users_workers_shift_2[i] in G_H_2)):
                            G_H_2_2.append(Users_workers_shift_2[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3)):
                            if G_H_3[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3[i])
                        for i in range(len(G_H_2)):
                            if G_H_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            TP = TP * TP_Farf_HCW_B_INT
           
                            for i in range(len(G_H_3)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3[i][1] == 0 and 
                                        G_H_3[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                          
                            for i in range(len(G_H_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2[i][1] == 0 and 
                                        G_H_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff3_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2)-1)
                                if (G_H_2[Sus_2][1] == 0 and 
                                                    G_H_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff3_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3)-1)
                                if (G_H_3[Sus_1][1] == 0 and 
                                                    G_H_3[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                                        
                        # fomites
                        HCW_pool = G_H_2 + G_H_3
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3_2)):
                            if G_H_3_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                         N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            TP = TP * TP_Farf_HCW_B_INT
           
                            for i in range(len(G_H_3_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3_2[i][1] == 0 and 
                                        G_H_3_2[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3_2[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE'
                          
                            for i in range(len(G_H_2_2)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_2_2[i][1] == 0 and 
                                        G_H_2_2[i][6] == 0):
                                        i_n = Users_workers_shift_2.index(G_H_2_2[i])
                                        Users_workers_shift_2[i_n][3] = day_current + 1 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_2[i_n][5] = 'Staff2_HCW_BASE'
                                        
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                if (G_H_2_2[Sus_2][1] == 0 and 
                                                    G_H_2_2[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_2.index(G_H_2_2[Sus_2])
                                        Users_workers_shift_2[i_n][3] = day_current + 1
                                        Users_workers_shift_2[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_2[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3_2)-1)
                                if (G_H_3_2[Sus_1][1] == 0 and 
                                                    G_H_3_2[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3_2[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff2_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                                        
                        # fomites
                        HCW_pool = G_H_3_2 + G_H_2_2
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                                        
                    #    ----------  Close Near Field  ----------------------------  
                    
                    # # ------- fomites
                    # # if fomites treated as 50% probability of non-ED base intervention:
                    # HCW_pool = [V_recep_3[0], 
                    #             V_triag_3[0], 
                    #             V_nurse_No_Urg_3[0], V_nurse_No_Urg_3[1], V_nurse_No_Urg_3[2],
                    #             dr_No_Urg_V_3[0], dr_No_Urg_V_3[1], dr_No_Urg_V_3[2], 
                    #             V_imagin_3[0], V_imagin_3[1], 
                    #             V_labor_3[0],
                    #             V_recep_2[0], V_recep_2[1],
                    #             V_triag_2[0], V_triag_2[1],
                    #             V_nurse_No_Urg_2[0], V_nurse_No_Urg_2[1], V_nurse_No_Urg_2[2], V_nurse_No_Urg_2[3],
                    #             dr_No_Urg_V_2[0], dr_No_Urg_V_2[1], dr_No_Urg_V_2[2], dr_No_Urg_V_2[3],
                    #             V_imagin_2[0], V_imagin_2[1],
                    #             V_labor_2[0]]
                    # fomite_function(HCW_pool, HCW_B, [Fomite[9], Fomite[10]], 0.5)
                    # ------- Close intervention                
                
                else:
                    N_HCW_inf_tot = 0
                    N_HCW_inf_2 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    Inf_H_2 = []
                    Inf_H_3 = []
                    for i in range(len(Users_workers_shift_2)):
                        if Users_workers_shift_2[i][1] == 1:
                            N_HCW_inf_2 = N_HCW_inf_2 + 1
                            Inf_H_2.append(Users_workers_shift_2[i])
                    for i in range(len(Users_workers_shift_3)):
                        if Users_workers_shift_3[i][1] == 1:
                            N_HCW_inf_3 = N_HCW_inf_3 + 1
                            Inf_H_3.append(Users_workers_shift_3[i])
                    N_HCW_inf_tot = N_HCW_inf_2 + N_HCW_inf_3
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                            
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                                
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            # TP = TP * Labor_fact
                            # # TP = TP*TP_pyth*TP_major
                            # TP = TP*TP_pyth*1
                            # TP_major = 1
                            
                            # TP = TP * TP_Near_HCW_B_INT
                            #TODO test change from near field to far
                            TP = TP * TP_Farf_HCW_B_INT
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            
                            TP = TP * TP_Farf_HCW_B
                            
                        for i in range(len(Users_workers_shift_2)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_2[i][1] == 0 and Users_workers_shift_2[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_2[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_2[i][6] = day_current + 1 
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff2_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_2[i][5] = 'Staff3_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_3)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_3[i][1] == 0 and Users_workers_shift_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_3[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_3[i][6] = day_current + 1 
                                    if N_HCW_inf_2 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff2_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff3_HCW_BASE'
    
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_2) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_2)-1)
                        if (Users_workers_shift_2[Sus_2][1] == 0 and 
                                            Users_workers_shift_2[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_2[Sus_2][3] = day_current + 1
                                Users_workers_shift_2[Sus_2][5] = 'Staff3_HCW_BASE' 
                                Users_workers_shift_2[Sus_2][6] = day_current + 1 
                    if len(Inf_H_3) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_3)-1)
                        if (Users_workers_shift_3[Sus_1][1] == 0 and 
                                            Users_workers_shift_3[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_3[Sus_1][3] = day_current + 1
                                Users_workers_shift_3[Sus_1][5] = 'Staff2_HCW_BASE' 
                                Users_workers_shift_3[Sus_1][6] = day_current + 1
                    #  ------------  Close Near Field  ----------------------------
                
                    # ------- Fomites
                    # HCW_pool = [V_recep_3[0], 
                    #             V_triag_3[0], 
                    #             V_nurse_No_Urg_3[0], V_nurse_No_Urg_3[1], V_nurse_No_Urg_3[2],
                    #             dr_No_Urg_V_3[0], dr_No_Urg_V_3[1], dr_No_Urg_V_3[2], 
                    #             V_imagin_3[0], V_imagin_3[1], 
                    #             V_labor_3[0],
                    #             V_recep_2[0], V_recep_2[1],
                    #             V_triag_2[0], V_triag_2[1],
                    #             V_nurse_No_Urg_2[0], V_nurse_No_Urg_2[1], V_nurse_No_Urg_2[2], V_nurse_No_Urg_2[3],
                    #             dr_No_Urg_V_2[0], dr_No_Urg_V_2[1], dr_No_Urg_V_2[2], dr_No_Urg_V_2[3],
                    #             V_imagin_2[0], V_imagin_2[1],
                    #             V_labor_2[0]]
                    HCW_pool = Users_workers_shift_3 + Users_workers_shift_2
                    # run light and door once on entry
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_once)
                    # run PC and sink 3-5 times for repeated contact
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                
            # Cleaning routine (decide how/when we want to handle cleaning)
            # if Time_var == (shift_3[0] + 1):
            #     fomite_cleaning(HCW_B, 0.5, [Fomite[9], Fomite[10]])
            # ------- End fomites
                
            # --------- HCW REPORTING (Pflegestützpunkt) SHIFT 3 and 1  -------
            
            # if (shift_1[0] == Time_var and SCREE_HCW and day_current > 9):
            #     Users_workers_shift_1 = []
            #     Users_workers_shift_2 = []
            #     Users_workers_shift_3 = []
            #     # Create worker_shifts 
            #     staff_shift  = workers_settings(Users_workers_shift_1, 
            #                                     Users_workers_shift_2, 
            #                                     Users_workers_shift_3)
            #     Users_workers_shift_1 = staff_shift[0]
                
            #     for i in range(len(Users_workers_shift_1)):
            #         PCR_test = random.random() < PCR_Eff
            #         if (Users_workers_shift_1[i][1] != 0 
            #             and (PCR_test)):
            #             # and Users_workers_shift_2[i][9] == 'infectious'):
            #             Users_workers_shift_1[i][8] = REPLACE
            #             Users_workers_shift_1[i][1] = 0
            #             Users_workers_shift_1[i][4] = 0
            #             Users_workers_shift_1[i][5] = UNDEF
            #             Users_workers_shift_1[i][6] = 0
            #             Users_workers_shift_1[i][7] = UNDEF
            #             Users_workers_shift_1[i][9] = UNDEF
            #             Users_workers_shift_1[i][10] = UNDEF
            #             Users_workers_shift_1[i][11] = 0
            #             Users_workers_shift_1[i][12] = 0
            #             Users_workers_shift_1[i][14] = UNDEF
            
            
            if shift_1[0] == Time_var:
                meet_HCW_1()
            
            if Time_var == shift_1[0]:
             
                if NB_SPLIT: 
                    N_HCW_inf_tot = 0
                    N_HCW_inf_1 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, 
                                 Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    ROOM_1 = 1
                    ROOM_2 = 1
                    
                    G_3 = random.sample(range(0, len(Users_workers_shift_3)), 
                                        (int((len(Users_workers_shift_3))/2)) )
                    G_1 = random.sample(range(0, len(Users_workers_shift_1)), 
                                        (int((len(Users_workers_shift_1))/2)) )
                    
                    G_H_3 = []
                    G_H_3_2 = []
                    G_H_1 = []
                    G_H_1_2 = []
                    for i in range(len(G_3)):
                        G_H_3.append((Users_workers_shift_3[G_3[i]]))
                    for i in range(len(Users_workers_shift_3)):
                        if (not(Users_workers_shift_3[i] in G_H_3)):
                            G_H_3_2.append(Users_workers_shift_3[i])
                    
                    for i in range(len(G_1)):
                        G_H_1.append((Users_workers_shift_1[G_1[i]]))
                    for i in range(len(Users_workers_shift_1)):
                        if (not(Users_workers_shift_1[i] in G_H_1)):
                            G_H_1_2.append(Users_workers_shift_1[i])
                    
                    # ---- ROOM 1
                    if ROOM_1:
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3)):
                            if G_H_3[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3[i])
                        for i in range(len(G_H_1)):
                            if G_H_1[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_1[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                            
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            TP = TP * TP_Farf_HCW_B_INT
           
                            for i in range(len(G_H_3)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_3[i][1] == 0 and 
                                        G_H_3[i][6] == 0):
                                        i_n = Users_workers_shift_3.index(G_H_3[i])
                                        Users_workers_shift_3[i_n][3] = day_current + 1 
                                        Users_workers_shift_3[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                          
                            for i in range(len(G_H_1)):
                                Trnasmiss = random.random() < TP
                                if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                    if (G_H_1[i][1] == 0 and 
                                        G_H_1[i][6] == 0):
                                        i_n = Users_workers_shift_1.index(G_H_1[i])
                                        Users_workers_shift_1[i_n][3] = day_current + 1 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                                        if N_HCW_inf_1 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                        if N_HCW_inf_2 != 0:
                                            Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE'
                            
                            # ------------- Nurse Base - Near field
                            if N_HCW_inf_1 > 0:
                                Sus_2 = random.randint(0, len(G_H_1)-1)
                                if (G_H_1[Sus_2][1] == 0 and 
                                                    G_H_1[Sus_2][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_1.index(G_H_1[Sus_2])
                                        Users_workers_shift_1[i_n][3] = day_current + 1
                                        Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE' 
                                        Users_workers_shift_1[i_n][6] = day_current + 1 
                            
                            if N_HCW_inf_2 > 0:
                                Sus_1 = random.randint(0, len(G_H_3)-1)
                                if (G_H_3[Sus_1][1] == 0 and 
                                                    G_H_3[Sus_1][6] == 0):
                                    A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                    diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                    index = diff.argmin()
                                    # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                    #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                    # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                    TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                    Trnasmiss = random.random() < TP
                                    if Trnasmiss:
                                        i_n = Users_workers_shift_3.index(G_H_3[Sus_1])
                                        Users_workers_shift_3[i_n][3] = day_current + 1
                                        Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE' 
                                        Users_workers_shift_3[i_n][6] = day_current + 1
                                        
                        # fomites
                        HCW_pool = G_H_3 + G_H_1
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm1_rep)
                        
                    #    ----------  Close Near Field  ----------------------------

                    # ---- ROOM 2
                    if ROOM_2:
                        
                        G_H_2_2 = G_H_1_2
                        N_HCW_inf_1 = 0
                        N_HCW_inf_2 = 0
                        Inf_H_1 = []
                        Inf_H_2 = []
                        for i in range(len(G_H_3_2)):
                            if G_H_3_2[i][1] == 1:
                                N_HCW_inf_1 = N_HCW_inf_1 + 1
                                Inf_H_1.append(G_H_3_2[i])
                        for i in range(len(G_H_2_2)):
                            if G_H_2_2[i][1] == 1:
                                N_HCW_inf_2 = N_HCW_inf_2 + 1
                                Inf_H_2.append(G_H_2_2[i])
                        N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_2
                        if N_HCW_inf_tot:
                            if N_HCW_inf_tot > 9:
                                N_HCW_inf_tot = 9
                                TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                             N_HCW_inf_tot]*TP_pyth
                                # TP = TP * Nur_B_fact
                                # TP = TP * T_NB
                                TP = TP * TP_Farf_HCW_B_INT
               
                                for i in range(len(G_H_3_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_3_2[i][1] == 0 and 
                                            G_H_3_2[i][6] == 0):
                                            i_n = Users_workers_shift_3.index(G_H_3_2[i])
                                            Users_workers_shift_3[i_n][3] = day_current + 1 
                                            Users_workers_shift_3[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_3[i_n][5] = 'Staff3_HCW_BASE'
                              
                                for i in range(len(G_H_2_2)):
                                    Trnasmiss = random.random() < TP
                                    if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                        if (G_H_2_2[i][1] == 0 and 
                                            G_H_2_2[i][6] == 0):
                                            i_n = Users_workers_shift_1.index(G_H_2_2[i])
                                            Users_workers_shift_1[i_n][3] = day_current + 1 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                            if N_HCW_inf_1 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff1_HCW_BASE'
                                            if N_HCW_inf_2 != 0:
                                                Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE'
                                            
                                # ------------- Nurse Base - Near field
                                if N_HCW_inf_1 > 0:
                                    Sus_2 = random.randint(0, len(G_H_2_2)-1)
                                    if (G_H_2_2[Sus_2][1] == 0 and 
                                                        G_H_2_2[Sus_2][6] == 0):
                                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                        diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                        index = diff.argmin()
                                        # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                        # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                        #         Mask[random.randint(0, 1)]]*TP_pyth_Near
                                        TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                        Trnasmiss = random.random() < TP
                                        if Trnasmiss:
                                            i_n = Users_workers_shift_1.index(G_H_2_2[Sus_2])
                                            Users_workers_shift_1[i_n][3] = day_current + 1
                                            Users_workers_shift_1[i_n][5] = 'Staff3_HCW_BASE' 
                                            Users_workers_shift_1[i_n][6] = day_current + 1 
                                
                                if N_HCW_inf_2 > 0:
                                    Sus_1 = random.randint(0, len(G_H_3_2)-1)
                                    if (G_H_3_2[Sus_1][1] == 0 and 
                                                        G_H_3_2[Sus_1][6] == 0):
                                        A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                                        diff = np.absolute(A1 - Prop_H_H_Nur_B)
                                        index = diff.argmin()
                                        # Mask = ['F_SP','F_SP','F_SP','F_BR']
                                        # TP = Tr_Pr_NEAR['Near'].loc[index, 
                                        #             Mask[random.randint(0, 1)]]*TP_pyth_Near
                                        # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                                        TP = TP_Near_HCW_B_INT * hcw_hcw_nurse
                                        Trnasmiss = random.random() < TP
                                        if Trnasmiss:
                                            i_n = Users_workers_shift_3.index(G_H_3_2[Sus_1])
                                            Users_workers_shift_3[i_n][3] = day_current + 1
                                            Users_workers_shift_3[i_n][5] = 'Staff1_HCW_BASE' 
                                            Users_workers_shift_3[i_n][6] = day_current + 1
                                            
                        # fomites
                        HCW_pool = G_H_3_2 + G_H_1_2
                        # run light and door once on entry
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_once)
                        # run PC and sink 3-5 times for repeated contact
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                        fomite_function(HCW_pool, HCW_B, fomite_EDBase_int_Rm2_rep)
                                            
                        #    ----------  Close Near Field  ----------------------------  
                        
                    # # ------- fomites
                    # # if fomites treated as 50% probability of non-ED base intervention:
                    # HCW_pool = [V_recep_1[0], V_recep_1[1], V_recep_1[2],
                    #             V_triag_1[0], V_triag_1[1],
                    #             V_nurse_No_Urg_1[0], V_nurse_No_Urg_1[1], V_nurse_No_Urg_1[2], V_nurse_No_Urg_1[3],
                    #             dr_No_Urg_V_1[0], dr_No_Urg_V_1[1], dr_No_Urg_V_1[2], dr_No_Urg_V_1[3],
                    #             V_imagin_1[0], V_imagin_1[1],
                    #             V_labor_1[0],
                    #             V_recep_3[0], 
                    #             V_triag_3[0], 
                    #             V_nurse_No_Urg_3[0], V_nurse_No_Urg_3[1], V_nurse_No_Urg_3[2],
                    #             dr_No_Urg_V_3[0], dr_No_Urg_V_3[1], dr_No_Urg_V_3[2], 
                    #             V_imagin_3[0], V_imagin_3[1], 
                    #             V_labor_3[0]]
                    # fomite_function(HCW_pool, HCW_B, [Fomite[9], Fomite[10]], 0.5)
                    # ------- Close intervention
                        
                else:
                
                    N_HCW_inf_tot = 0
                    N_HCW_inf_1 = 0
                    N_HCW_inf_3 = 0
                    Users_workers_shift_1 = []
                    Users_workers_shift_2= []
                    Users_workers_shift_3= []
                    # Create worker_shifts 
                    staff_shift  = workers_settings(Users_workers_shift_1, 
                                 Users_workers_shift_2, Users_workers_shift_3)
                    Users_workers_shift_1 = staff_shift[0]
                    Users_workers_shift_2 = staff_shift[1]
                    Users_workers_shift_3 = staff_shift[2]
                    
                    Inf_H_1 = []
                    Inf_H_3 = []
                    for i in range(len(Users_workers_shift_1)):
                        if Users_workers_shift_1[i][1] == 1:
                            N_HCW_inf_1 = N_HCW_inf_1 + 1
                            Inf_H_1.append(Users_workers_shift_1[i])
                    for i in range(len(Users_workers_shift_3)):
                        if Users_workers_shift_3[i][1] == 1:
                            N_HCW_inf_3 = N_HCW_inf_3 + 1
                            Inf_H_3.append(Users_workers_shift_3[i])
                    N_HCW_inf_tot = N_HCW_inf_1 + N_HCW_inf_3
                    if N_HCW_inf_tot:
                        TP_major = 1
                        if N_HCW_inf_tot > 9:
                            N_HCW_inf_tot = 9
                            TP_major = 3
                        # if HCW_BASES:
                        #     if N_HCW_inf_tot > 5:
                        #         N_HCW_inf_tot = 5
                        
                        if NB_ROOM:
                            if N_HCW_inf_tot > 5:
                                N_HCW_inf_tot = 5                           
                            TP = Tr_Pr['8_Laborat'].loc[7, N_HCW_inf_tot]
                            # TP = TP * Labor_fact
                            # TP = TP*TP_pyth*TP_major
                            # TP_major = 1
                            TP = TP * TP_Farf_HCW_B_INT
                            
                        else:
                            TP = Tr_Pr['9_Pflegestützpunkt'].loc[0, 
                                                     N_HCW_inf_tot]*TP_pyth
                            # TP = TP * Nur_B_fact
                            # TP = TP * T_NB
                            
                            TP = TP * TP_Farf_HCW_B
                            
                        for i in range(len(Users_workers_shift_1)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_1[i][1] == 0 and Users_workers_shift_1[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_1[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_1[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_1[i][5] = 'Staff3_HCW_BASE'
                      
                        for i in range(len(Users_workers_shift_3)):
                            Trnasmiss = random.random() < TP
                            if (Trnasmiss and (N_HCW_inf_tot != 0 )):
                                if Users_workers_shift_3[i][1] == 0 and Users_workers_shift_3[i][6] == 0:
            #                        V_recep[i][1] = 1        # Worker potential infection
                                    Users_workers_shift_3[i][3] = day_current + 1 
                                    # V_nurse_No_Urg_1[i][5] = PATIEN+'_ATTEN_URGE'
                                    Users_workers_shift_3[i][6] = day_current + 1 
                                    if N_HCW_inf_1 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff1_HCW_BASE'
                                    if N_HCW_inf_3 != 0:
                                        Users_workers_shift_3[i][5] = 'Staff3_HCW_BASE'
    
                    # ------------- Nurse Base - Near field
                    if len(Inf_H_1) > 0:
                        Sus_2 = random.randint(0, len(Users_workers_shift_1)-1)
                        if (Users_workers_shift_1[Sus_2][1] == 0 and 
                                            Users_workers_shift_1[Sus_2][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_1[Sus_2][3] = day_current + 1
                                Users_workers_shift_1[Sus_2][5] = 'Staff3_HCW_BASE' 
                                Users_workers_shift_1[Sus_2][6] = day_current + 1 
                    if len(Inf_H_3) > 0:
                        Sus_1 = random.randint(0, len(Users_workers_shift_3)-1)
                        if (Users_workers_shift_3[Sus_1][1] == 0 and 
                                            Users_workers_shift_3[Sus_1][6] == 0):
                            A1 = Tr_Pr_NEAR['Near'].loc[:,'m']
                            # Share_time = abs(agent[5] - Sucep_Area[SUS][5])
                            # Share_time = int(agent[4]*(Prop_P_H_M))
                            diff = np.absolute(A1 - Prop_H_H_Nur_B)
                            index = diff.argmin()
                            # Mask = ['F_SP','F_SP','F_SP','F_BR']
                            # TP = Tr_Pr_NEAR['Near'].loc[index, Mask[random.randint(0, 1)]]*TP_pyth_Near
                            # TP = Tr_Pr_NEAR['Near'].loc[index, 'S_SP']
                            TP = TP_Near_HCW_B * hcw_hcw_nurse
                            Trnasmiss = random.random() < TP
                            if Trnasmiss:
                                Users_workers_shift_3[Sus_1][3] = day_current + 1
                                Users_workers_shift_3[Sus_1][5] = 'Staff1_HCW_BASE' 
                                Users_workers_shift_3[Sus_1][6] = day_current + 1
                    #  ------------  Close Near Field  ----------------------------
                
                    # ------- Fomites
                    # HCW_pool = [V_recep_1[0], V_recep_1[1], V_recep_1[2],
                    #             V_triag_1[0], V_triag_1[1],
                    #             V_nurse_No_Urg_1[0], V_nurse_No_Urg_1[1], V_nurse_No_Urg_1[2], V_nurse_No_Urg_1[3],
                    #             dr_No_Urg_V_1[0], dr_No_Urg_V_1[1], dr_No_Urg_V_1[2], dr_No_Urg_V_1[3],
                    #             V_imagin_1[0], V_imagin_1[1],
                    #             V_labor_1[0],
                    #             V_recep_3[0], 
                    #             V_triag_3[0], 
                    #             V_nurse_No_Urg_3[0], V_nurse_No_Urg_3[1], V_nurse_No_Urg_3[2],
                    #             dr_No_Urg_V_3[0], dr_No_Urg_V_3[1], dr_No_Urg_V_3[2], 
                    #             V_imagin_3[0], V_imagin_3[1], 
                    #             V_labor_3[0]]
                    HCW_pool = Users_workers_shift_1 + Users_workers_shift_3
                    # run light and door once on entry
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_once)
                    # run PC and sink 3-5 times for repeated contact
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
                    fomite_function(HCW_pool, HCW_B, fomite_EDBase_rep)
            
            # Cleaning routine (decide how/when we want to handle cleaning)
            # if Time_var == (shift_1[0] + 1):
            #     fomite_cleaning(HCW_B, 0.5, [Fomite[9], Fomite[10]])
            # ------- End fomites
                
            Time_var = Time_var + 1
        
        # print(day+1)
        
        
        
        for k in range(len(Users)):
            if Users[k][2] != 'EXIT':
                action_desit_tree(Users[k], k, day, 1439) # Same day attendance
                Users[k][8] = Users[k][2]
                Users[k][2] = 'EXIT'
        
        
        Users_workers_shift_1 = []
        Users_workers_shift_2 = []
        Users_workers_shift_3 = []
        
        
        # Create worker_shifts 
        staff_shift  = workers_settings(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3)
        Users_workers_shift_1 = staff_shift[0]
        Users_workers_shift_2 = staff_shift[1]
        Users_workers_shift_3 = staff_shift[2]
        
       
        
        
        cont_1 = 0
        # HCW_inf_1 = []
        for i in range(len(Users_workers_shift_1)):
            if Users_workers_shift_1[i][6] == (day + 1):
                cont_1 = cont_1 + 1
        HCW_inf_1.append([day,cont_1])
        
        cont_2 = 0
        # HCW_inf_2 = []
        for i in range(len(Users_workers_shift_2)):
            if Users_workers_shift_2[i][6] == (day + 1):
                cont_2 = cont_2 + 1
        HCW_inf_2.append([day,cont_2])
        
        cont_3 = 0
        # HCW_inf_3 = []
        for i in range(len(Users_workers_shift_3)):
            if Users_workers_shift_3[i][6] == (day + 1):
                cont_3 = cont_3 + 1
        HCW_inf_3.append([day,cont_3])
            
        
        HCW_propo_num = [Recep_port_HCW,Triag_port_HCW, AtteU_port_HCW,
                         AtteN_port_HCW,Imagi_port_HCW,Labot_port_HCW,
                         Base1_port_HCW, Base2_port_HCW, Base3_port_HCW]    
        
        HCW_propo = proport_HCW_day(day,Users_workers_shift_1,
                                    Users_workers_shift_2,
                    Users_workers_shift_3,HCW_propo_num)
        
        
        
        #  HCW status - immune | infected | symptoms -
        staff_shift_status = workers_settings_status(Users_workers_shift_1, Users_workers_shift_2, Users_workers_shift_3, day_current)
        Users_workers_shift_1 = staff_shift_status[0]
        Users_workers_shift_2 = staff_shift_status[1]
        Users_workers_shift_3 = staff_shift_status[2]
        
        
            
        curr_user = Users
        Result_user.extend(curr_user)
        
        cont_use_day = 0
        for i in range(len(Users)):
            if ((Users[i][1] == 2) and (Users[i][9] != UNDEF) and (
                (Users[i][11] == PATIEN+'_RECEPTION') or
                (Users[i][11] == PATIEN+'_TRIAGE') or
                (Users[i][11] == 'WAIT_NO_URGENT') or
                (Users[i][11] == 'WAIT_URGENT') or
                (Users[i][11] == PATIEN+'_ATTEN_URGE') or
                (Users[i][11] == PATIEN+'_ATTE_N_URG') or 
                (Users[i][11] == PATIEN+'_LABORATORY') or 
                (Users[i][11] == PATIEN +'_IMAGING') ) ) :
                cont_use_day = cont_use_day + 1
        N_new_day.append([day,cont_use_day])
        

        User_propo_num = [Recep_port,Triag_port,WaitU_port,WaitN_port,
                          AtteU_port,AtteN_port,Imagi_port,Labot_port]
        User_propot = proport_user_day(day,Users,User_propo_num)
        Recep_port = User_propot[0]
        Triag_port = User_propot[1]
        WaitU_port = User_propot[2]
        WaitN_port = User_propot[3]
        AtteU_port = User_propot[4]
        AtteN_port = User_propot[5]
        Imagi_port = User_propot[6]
        Labot_port = User_propot[7]
        
        
        
        # Pat_new_Fom = []
        # HCW_new_Fom = []
        # Fomite_new = []
        
        Pat_f = 0
        for k in range(len(Users)):
            if (Users[k][1] == 3):
                Pat_f = Pat_f + 1
                # print('Pat from Fom:',Users[k][16])
        Pat_new_Fom.append([day,Pat_f])
                
        HCW_f = 0
        for k in range(len(Users_workers_shift_1)):
            if (Users_workers_shift_1[k][1] == 3):
                HCW_f = HCW_f + 1
                # print('HCW from Fom:',Users_workers_shift_1[k][15])
        for k in range(len(Users_workers_shift_2)):
            if (Users_workers_shift_2[k][1] == 3):
                HCW_f = HCW_f + 1
                # print('HCW from Fom:',Users_workers_shift_2[k][15])
        for k in range(len(Users_workers_shift_3)):
            if (Users_workers_shift_3[k][1] == 3):
                HCW_f = HCW_f + 1
                # print('HCW from Fom:',Users_workers_shift_3[k][15])
        HCW_new_Fom.append([day,HCW_f])  
             
        Fom_f = 0
        for k in range(len(Fomite)):
            if ((Fomite[k][2] == 'Contaminated') and
                (Fomite[k][8] != 'UNDEFINED')):
                Fom_f = Fom_f + 1
                # print('Fom from:',Fomite[k][8])
        Fomite_new.append([day,Fom_f])  
        
        # if ((day == 10) or (day == 15) or (day == 5) or (day == 20) 
        #     or (day == 3)):
        #     print (day)

        

        """------------------ Patients read next day ---------------------------
        """
        if day < len(Aget_day)-1:
            t_arriv = []
            for i in range(hrs):
                pati = int( Df['D'+str(day + 2)].loc[i, "DAY"] )
                if pati > 0:
                    for k in range(pati):
                        t_ar = random.randint(h_ranges[i][0], h_ranges[i][1])   
                        t_arriv.append(t_ar)
                        t_arriv.sort()
                        
                        
            color = ['RED','ORANGE','YELLLOW','GREEN','BLUE','WITHOUT']            
            triag_pat = []
            for i in range(hrs):
                for k in range(len(color)):
                    if (int( Df['D'+str(day + 2)].loc[i,color[k]] )) > 0:
                        for qq in range(int(Df['D'+str(day + 2)].loc[i,color[k]])):
                            if ('WITHOUT' == color[k]):
                                k1 = random.randint(2, 4)
                                triag_pat.append(color[k1])
                            else:    
                                triag_pat.append(color[k])

            if len(Users) < Aget_day.loc[day+1, "tot"]:
                tam = Aget_day.loc[day+1, "tot"] - len(Users)
                for i in range(tam):
                    Users.append([i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, 
                            UNDEF, UNDEF, 0, UNDEF, UNDEF, UNDEF, UNDEF, UNDEF, UNDEF, UNDEF, 0])  # note: read in users again
            elif len(Users) > Aget_day.loc[day+1, "tot"]:
                tam = len(Users) - Aget_day.loc[day+1, "tot"]
                for i in range(tam):
                    Users.pop()
            
            # day_users = Users

            for i in range(Aget_day.loc[day+1, "tot"]):
                Users[i] = [i+1, 0, UNDEF, 0, 0, t_arriv[i],0, 0, 
                            UNDEF, UNDEF, 0, UNDEF, triag_pat[i], UNDEF, UNDEF, UNDEF, UNDEF, UNDEF, 0]  # note: read in users again

            # infec = np.random.randint(1,len(Users), size=(N_infected))

            # for i in range(len(infec)):
            #     Users[infec[i]][1] = 1
            #     Users[infec[i]][9] = INFEC
            
    
        # """------------------Seat Map Waiting Area  ---------------------------
        # """
        # # for i in range(Seat_map.shape[0]):
        # #     for j in range(Seat_map.shape[1]):
        # #         Seat_map[i,j] = 0
    
        # ATT_NU_ROOM_1 = 1
        # ATT_NU_ROOM_2 = 1
        # ATT_NU_ROOM_3 = 1
        
        # ATT_U_BED_1 = 1
        # ATT_U_BED_2 = 1
        # ATT_U_BED_3 = 1
        
        # ROMS_G = [ATT_NU_ROOM_1, ATT_NU_ROOM_2, ATT_NU_ROOM_3]
        # BEDS_G = [ATT_U_BED_1, ATT_U_BED_2, ATT_U_BED_3]    
        
        ROMS_G = []
        for i in range(0, N_rooms_):
            ROMS_G.append(1)

        BEDS_G = []
        for i in range(0, N_beds_):
            BEDS_G.append(1)
    
        # if (day == 20):
        # print(day)
        

    
        Time_var = 0
    
    #  Counting infected patients by patients and HCW
    Tot_pat = 0
    Tot_HCW = 0
    for i in range(len(User_propot)):
        for k in range(len(Recep_port)):
            Tot_pat = Tot_pat + User_propot[i][k][0]
            Tot_HCW = Tot_HCW + User_propot[i][k][1]     
    Total_patien_inf = Tot_pat + Tot_HCW
    
    #  Counting infected HCW by patients and HCW
    Tot_pat_HCW = 0
    Tot_HCW_HCW = 0
    for i in range(len(HCW_propo)):
        for k in range (len(HCW_propo[i])):
            Tot_pat_HCW = Tot_pat_HCW + HCW_propo[i][k][0]
            Tot_HCW_HCW = Tot_HCW_HCW + HCW_propo[i][k][1]     
    Total_HCW_inf = Tot_pat_HCW + Tot_HCW_HCW
    
    
    
    propo_area = [Recep_propo,Triag_propo,WaitU_propo,WaitN_propo,
                          AtteU_propo,AtteN_propo,Imagi_propo,Labot_propo]
    User_proport = proportion_user_tot(User_propot,propo_area,Total_patien_inf)
    Recep_propo = User_proport[0]
    Triag_propo = User_proport[1]
    WaitU_propo = User_proport[2]
    WaitN_propo = User_proport[3]
    AtteU_propo = User_proport[4]
    AtteN_propo = User_proport[5]
    Imagi_propo = User_proport[6]
    Labot_propo = User_proport[7]
    
    
    propo_HCW = [Recep_prop_H,Triag_prop_H, AtteU_prop_H,AtteN_prop_H,
                  Imagi_prop_H,Labot_prop_H,Base1_prop_H,Base2_prop_H,
                  Base3_prop_H]
    HCWs_proport = propor_HCW_tot(HCW_propo, propo_HCW, Total_HCW_inf)
    Recep_prop_H = HCWs_proport[0]
    Triag_prop_H = HCWs_proport[1]
    AtteU_prop_H = HCWs_proport[2]
    AtteN_prop_H = HCWs_proport[3]
    Imagi_prop_H = HCWs_proport[4]
    Labot_prop_H = HCWs_proport[5]
    Base1_prop_H = HCWs_proport[6]
    Base2_prop_H = HCWs_proport[7]
    Base3_prop_H = HCWs_proport[8]
    
    
    H_coun_by_p = []
    H_coun_by_H = []
    # for i in range(len(HCW_propo)):
    #     for k in range (len(HCW_propo[0])):
            
    for k in range (len(HCW_propo[0])):      
        H_coun_by_p.append( (  HCW_propo[0][k][0] + HCW_propo[1][k][0] +
                               HCW_propo[2][k][0] + HCW_propo[3][k][0] +
                               HCW_propo[4][k][0] + HCW_propo[5][k][0] +
                               HCW_propo[6][k][0] + HCW_propo[7][k][0] +
                               HCW_propo[8][k][0] ) ) 
        H_coun_by_H.append( (  HCW_propo[0][k][1] + HCW_propo[1][k][1] +
                               HCW_propo[2][k][1] + HCW_propo[3][k][1] +
                               HCW_propo[4][k][1] + HCW_propo[5][k][1] +
                               HCW_propo[6][k][1] + HCW_propo[7][k][1] +
                               HCW_propo[8][k][1] ) )
    
    P_coun_by_p = []
    P_coun_by_H = []
    for k in range (len(User_propot[0])):    
        P_coun_by_p.append( ( User_propot[0][k][0] + User_propot[1][k][0] +
                              User_propot[2][k][0] + User_propot[3][k][0] +
                              User_propot[4][k][0] + User_propot[5][k][0] +
                              User_propot[6][k][0] + User_propot[7][k][0] ) )
        P_coun_by_H.append( ( User_propot[0][k][1] + User_propot[1][k][1] +
                              User_propot[2][k][1] + User_propot[3][k][1] +
                              User_propot[4][k][1] + User_propot[5][k][1] +
                              User_propot[6][k][1] + User_propot[7][k][1] ) )
        
    
    
    pat_tot = []
    days_plot = []
    staff_plot = []
    staff_1 = []
    staff_2 = []
    staff_3 = []
    
    HCW_infec_1 = []
    HCW_infec_2 = []
    HCW_infec_3 = []
    for i in range(len(N_new_day)):
        pat_tot.append(N_new_day[i][1])
        # staff_plot.append(cont_from_w_shift_1[i][1] +
        #             cont_from_w_shift_2[i][1] + cont_from_w_shift_3[i][1])
        # staff_1.append(cont_from_w_shift_1[i][1])
        # staff_2.append(cont_from_w_shift_2[i][1])
        # staff_3.append(cont_from_w_shift_3[i][1])
        days_plot.append(N_new_day[i][0]+1)
        HCW_infec_1.append(HCW_inf_1[i][1] + HCW_inf_2[i][1] + HCW_inf_3[i][1] )
        HCW_infec_2.append(HCW_inf_2[i][1])
        HCW_infec_3.append(HCW_inf_3[i][1])
    
    # width = 0.5   
    # ax=plt.figure(figsize=(12,5), facecolor='w', edgecolor='k')
    # p1 = plt.bar(days_plot, P_coun_by_H, width)
    # p2 = plt.bar(days_plot, P_coun_by_p, width,
    #               bottom=P_coun_by_H)
    # # p3 = plt.bar(days_plot, staff_1, width,
    # #               bottom=staff_plot)
    # #plt.ylabel('Newly infected')
    # plt.title('Newly infected patients per day (numbers)', fontsize=14)
    # plt.xticks(days_plot, fontsize=12)
    # plt.yticks(fontsize=12)
    # plt.ylim(0, 40) 
    # # plt.legend((p1[0], p2[0]), ('By HCW (month = {})'.format( sum(P_coun_by_H)), 
    # #   'By patients (month = {})\n\nTotal month: {}'.format(sum(P_coun_by_p), sum(P_coun_by_H) + sum(P_coun_by_p))), 
    # #                                                         fontsize = 14)
    # # ax.savefig('P_inf_day_3_intev.pdf', format='pdf', dpi=1400)
    # plt.show()
    
    
    # ax1=plt.figure(figsize=(12,5), facecolor='w', edgecolor='k')
    # p1 = plt.bar(days_plot, H_coun_by_H, width, 
    #        label='Infected by HCW (month = {})'.format(sum(H_coun_by_H)) )
    # p2 = plt.bar(days_plot, H_coun_by_p, width,
    #      bottom=H_coun_by_H, label='Infected by patients (month = {})\n Total month = {}'.format(
    #              sum(H_coun_by_p), sum(H_coun_by_H) + sum(H_coun_by_p) ))
    # # p2 = plt.bar(days_plot, pat_tot, width,
    # #               bottom=staff_plot)
    # # p3 = plt.bar(days_plot, staff_1, width,
    # #               bottom=staff_plot)
    # #plt.ylabel('Newly infected')
    # plt.title('Newly infected HCW per day (numbers)', fontsize = 14)
    # plt.xticks(days_plot, fontsize=12)
    # plt.yticks(fontsize=12)
    # plt.ylim(0, 30) 
    # plt.legend(fontsize=14)
    # # ax1.savefig('HCW_inf_day_3_intev.pdf', format='pdf', dpi=1400)
    # plt.show()
    
    
    
    # ax=plt.figure(figsize=(10,5), facecolor='w', edgecolor='k')
    # # p1 = plt.bar(days_plot, staff_plot, width)
    # p5 = plt.bar(days_plot, staff_3, width)
    # p4 = plt.bar(days_plot, staff_2, width, bottom = staff_3)
    # p3 = plt.bar(days_plot, staff_1, width, bottom = staff_3)
    # # p2 = plt.bar(days_plot, pat_tot, width, bottom=staff_1)
    # # p2 = plt.bar(days_plot, pat_tot, width)
    # # p3 = plt.bar(days_plot, staff_1, width)
    # # p4 = plt.bar(days_plot, staff_2, width, bottom=staff_3)
    # # p5 = plt.bar(days_plot, staff_3, width, bottom=staff_3)
    # #plt.ylabel('Newly infected')
    # plt.title('Newly infected patients per day (numbers)', fontsize=14)
    # plt.xticks(days_plot, fontsize=12)
    # plt.yticks(fontsize=12)
    # plt.ylim(0, 40) 
    # plt.legend((p3[0], p4[0], p5[0] ), ('Staff 1', 'Staff 2', 'Staff 3'), fontsize=12)
    # # ax.savefig('new_infec_4.pdf', format='pdf', dpi=1400)
    # plt.show()
    
    # result_list = {
    #                   # "Number of infected patient": (sum(P_coun_by_H)+sum(P_coun_by_p)), #  Total PATIENT + HCW
    #                   # "Numb agent":Num_Aget,
    #                   # "N_days":N_days,
    #                   # "Number of infected staff":N_new_day, # PATIENTS
    #                   # # "Number of days":days_plot,
    #                   # "Users workers shift 1":Users_workers_shift_1,
    #                   # "Users workers shift 2":Users_workers_shift_2,
    #                   # "Users workers shift 3":Users_workers_shift_3,
    #                   # "workers_count_1" : workers_count_1,
    #                   # "workers_count_2" : workers_count_2,
    #                   # "workers_count_3" : workers_count_3,
    #                   # "workers_count_1, percentage prop" : per_staff_count_1,
    #                   # "workers_count_2, percentage prop" : per_staff_count_2,
    #                   # "workers_count_3, percentage prop" : per_staff_count_3,
    #                   # "cont_from_w_shift_1" : cont_from_w_shift_1, # HCW 1
    #                   # "cont_from_w_shift_2" : cont_from_w_shift_2, # HCW 2
    #                   # "cont_from_w_shift_3" : cont_from_w_shift_3, # HCW 3
    #                   "Users_numbers"       : User_proport,
    #                   "HCW_numbers"         : HCWs_proport} 

    
    # result_list = {"Users_numbers"       : User_proport,
    #                "HCW_numbers"         : HCWs_proport}
    Total_Fomi = 0
    Total_Fomi_new = 0
    Total_Pat_new_Fom = 0
    Total_HCW_new_Fom = 0


    for i in range(len(Pat_new_Fom)):
        Total_Fomi = Total_Fomi + (Pat_new_Fom[i][1] + 
                                   HCW_new_Fom[i][1] + 
                                   Fomite_new[i][1])
        Total_Fomi_new = Total_Fomi_new + Fomite_new[i][1]
        Total_Pat_new_Fom = Total_Pat_new_Fom + Pat_new_Fom[i][1]
        Total_HCW_new_Fom = Total_HCW_new_Fom + HCW_new_Fom[i][1]
        
    Total_Fom_Relat = (len(trans_Fom_User) + len(trans_Fom_HCW) +
                       len(trans_User_Fom) + len(trans_HCW_Fom))
    
    res_tupple = tuple(tuple(sub) for sub in Users_workers_shift_1)
            
    HCWs_proporttuple = tuple(HCWs_proport)
    User_proporttuple = tuple(User_proport)
    Fomit_tuple = tuple([Total_Fomi, Total_Fomi_new, Total_Pat_new_Fom,
                         Total_HCW_new_Fom, Total_Fom_Relat])
    result_monthly.append((User_proporttuple, HCWs_proporttuple, 
                                sum(H_coun_by_p) + sum(H_coun_by_H),
                                sum(P_coun_by_p) + sum(P_coun_by_H),
                               (sum(H_coun_by_p) + sum(H_coun_by_H) +
                                sum(P_coun_by_p) + sum(P_coun_by_H)),
                               res_tupple, Fomit_tuple))
    
    return(result_monthly)
    
    # return [User_proport, HCWs_proport, sum(H_coun_by_p) + sum(H_coun_by_H),
    #                                     sum(P_coun_by_p) + sum(P_coun_by_H),
    #                                    (sum(H_coun_by_p) + sum(H_coun_by_H) +
    #                                     sum(P_coun_by_p) + sum(P_coun_by_H))
    #                                   ]

# Res = main_funct()
# print(Res)

# t2 = time.perf_counter()
        
# print("\nFinished in " + str(round((t2-t1)/60,2))   + " minute(s)")  

# cols = sns.color_palette("Set2",8)
# names = ['Base\n total', 'Base\n Pat', 'Base\n HCW']
# f, ax3 = plt.subplots(figsize=(13,6), facecolor='w', edgecolor='k')
# # ax3.set_yscale("log")
# plt.rc('xtick', labelsize = 17) 
# plt.rc('ytick', labelsize = 17) 
# # sns.stripplot(data=[Base_TOT, F_co_TOT, Curt_TOT, Vent_TOT, V_Cu_TOT, 
# #                       N_VC_TOT, scre_TOT], color=".4")
# sns.boxplot(data=[Total_infect, Total_infe_P, Total_infe_H], palette = cols)
# plt.xticks(np.arange(3), names) 
# # plt.ylim(top=400) 
# plt.title('Total of newly infected', fontsize = 22)

# with open('results/Result'+str(1) +'.txt', 'w') as f:
#     wr = csv.writer(f,Res)
#     wr.writerows(Res)