# -*- coding: utf-8 -*-
"""
InnoBRI Emergency Department Simulation Platform
Platform parallelization
Main file
Functions driver file 
29.10.2021

@author: Gustavo"""
import matplotlib.pyplot as plt

from main_plat_ED_airborne_WWU import *
from functions_plat_ED_WWU import *

import scipy.stats
import seaborn as sns
import collections, numpy

import concurrent.futures


 
t1 = time.perf_counter()
runs = 10 # N of simulations

save_PAT = []
save_HCW = []

if __name__ == '__main__': 
    save_results = []
    save_results1 = []
    # save_PAT = [ [0,0,0,0], ]
    # save_HCW = []
    with concurrent.futures.ProcessPoolExecutor() as executor: 
        future_results =  [executor.submit(main_funct) for _ in range(runs)]
        for fut in concurrent.futures.as_completed(future_results):
            # print(fut.result())
            print(fut.done())
            save_results.append(fut.result()) 
            counter = 0
            # for i in save_results:
            #     from collections import Counter
            #     with open('results/Result_parall_'+str(counter)+'.txt', 'w') as f:
            #         wr = csv.writer(f,delimiter=":")
            #         wr.writerows(Counter(i).items())
            #         counter = counter + 1
        # Res = average_funct(save_results, save_PAT, save_HCW)
          
        Recep_P = []
        Triag_P = []
        WaitU_P = []
        WaitN_P = []
        AtteU_P = []
        AtteN_P = []
        Imagi_P = []
        Labot_P = []
        
        Recep_prop_H = []
        Triag_prop_H = []
        AtteU_prop_H = []
        AtteN_prop_H = []
        Imagi_prop_H = []
        Labot_prop_H = []
        Base1_prop_H = []
        Base2_prop_H = []
        Base3_prop_H = []
        
        Total_infect = []
        Total_infe_P = []
        Total_infe_H = []
        Total_fomite = []
        Total_fomite_1 = []
        
        Recep_num_P_P = []
        Recep_num_P_H = []
        Recep_num_H_P = []
        Recep_num_H_H = []
        
        Triag_num_P_P = []
        Triag_num_P_H = []
        Triag_num_H_P = []
        Triag_num_H_H = []
        
        WaitU_P_P = []
        WaitN_P_P = []
        
        AtteU_num_P_P = []
        AtteU_num_P_H = []
        AtteU_num_H_P = []
        AtteU_num_H_H = []
        
        AtteN_num_P_P = []
        AtteN_num_P_H = []
        AtteN_num_H_P = []
        AtteN_num_H_H = []
        
        Imagi_num_P_P = []
        Imagi_num_P_H = []
        Imagi_num_H_P = []
        Imagi_num_H_H = []
        
        Labot_num_P_P = []
        Labot_num_P_H = []
        Labot_num_H_P = []
        Labot_num_H_H = []
        
        Base1_num_H = []
        Base2_num_H = []
        Base3_num_H = []

        for i in range(len(save_results)):
            Recep_P.append(save_results[i][0][0][0])
            Triag_P.append(save_results[i][0][0][1])
            WaitU_P.append(save_results[i][0][0][2])
            WaitN_P.append(save_results[i][0][0][3])
            AtteU_P.append(save_results[i][0][0][4])
            AtteN_P.append(save_results[i][0][0][5])
            Imagi_P.append(save_results[i][0][0][6])
            Labot_P.append(save_results[i][0][0][7])
            
            Recep_prop_H.append(save_results[i][0][1][0])
            Triag_prop_H.append(save_results[i][0][1][1])
            AtteU_prop_H.append(save_results[i][0][1][2])
            AtteN_prop_H.append(save_results[i][0][1][3])
            Imagi_prop_H.append(save_results[i][0][1][4])
            Labot_prop_H.append(save_results[i][0][1][5])
            Base1_prop_H.append(save_results[i][0][1][6])
            Base2_prop_H.append(save_results[i][0][1][7])
            Base3_prop_H.append(save_results[i][0][1][8])

        
        for i in range(len(save_results)):
            Recep_num_P_P.append(Recep_P[i][2])
            Recep_num_P_H.append(Recep_P[i][3])
            Recep_num_H_P.append(Recep_prop_H[i][2])
            Recep_num_H_H.append(Recep_prop_H[i][3])
            
            Triag_num_P_P.append(Triag_P[i][2])
            Triag_num_P_H.append(Triag_P[i][3])
            Triag_num_H_P.append(Triag_prop_H[i][2])
            Triag_num_H_H.append(Triag_prop_H[i][3])
            
            WaitU_P_P.append(WaitU_P[i][2])
            WaitN_P_P.append(WaitN_P[i][2])
            
            AtteU_num_P_P.append(AtteU_P[i][2])
            AtteU_num_P_H.append(AtteU_P[i][3])
            AtteU_num_H_P.append(AtteU_prop_H[i][2])
            AtteU_num_H_H.append(AtteU_prop_H[i][3])
            
            AtteN_num_P_P.append(AtteN_P[i][2])
            AtteN_num_P_H.append(AtteN_P[i][3])
            AtteN_num_H_P.append(AtteN_prop_H[i][2])
            AtteN_num_H_H.append(AtteN_prop_H[i][3])
            
            Imagi_num_P_P.append(Imagi_P[i][2])
            Imagi_num_P_H.append(Imagi_P[i][3])
            Imagi_num_H_P.append(Imagi_prop_H[i][2])
            Imagi_num_H_H.append(Imagi_prop_H[i][3])
            
            Labot_num_P_P.append(Labot_P[i][2])
            Labot_num_P_H.append(Labot_P[i][3])
            Labot_num_H_P.append(Labot_prop_H[i][2])
            Labot_num_H_H.append(Labot_prop_H[i][3])
            
            Base1_num_H.append(Base1_prop_H[i][3])
            Base2_num_H.append(Base2_prop_H[i][3])
            Base3_num_H.append(Base3_prop_H[i][3])
        
        
        Tot_Recep_P = [x + y for x, y in zip(Recep_num_P_P, Recep_num_P_H)]
        Tot_Recep_H = [x + y for x, y in zip(Recep_num_H_P, Recep_num_H_H)]
        Tot_Recep = [x + y for x, y in zip(Tot_Recep_P, Tot_Recep_H)]
        
        Tot_Triag_P = [x + y for x, y in zip(Triag_num_P_P, Triag_num_P_H)]
        Tot_Triag_H = [x + y for x, y in zip(Triag_num_H_P, Triag_num_H_H)]
        Tot_Triag = [x + y for x, y in zip(Tot_Triag_P, Tot_Triag_H)]
        
        Tot_WaitU = WaitU_P_P
        Tot_WaitN = WaitN_P_P
        
        Tot_AtteU_P = [x + y for x, y in zip(AtteU_num_P_P, AtteU_num_P_H)]
        Tot_AtteU_H = [x + y for x, y in zip(AtteU_num_H_P, AtteU_num_H_H)]
        Tot_AtteU  = [x + y for x, y in zip(Tot_AtteU_P, Tot_AtteU_H)]
        
        Tot_AtteN_P = [x + y for x, y in zip(AtteN_num_P_P, AtteN_num_P_H)]
        Tot_AtteN_H = [x + y for x, y in zip(AtteN_num_H_P, AtteN_num_H_H)]
        Tot_AtteN  = [x + y for x, y in zip(Tot_AtteN_P, Tot_AtteN_H)]
        
        Tot_Imagi_P = [x + y for x, y in zip(Imagi_num_P_P, Imagi_num_P_H)]
        Tot_Imagi_H = [x + y for x, y in zip(Imagi_num_H_P, Imagi_num_H_H)]
        Tot_Imagi  = [x + y for x, y in zip(Tot_Imagi_P, Tot_Imagi_H)]
        
        Tot_Labot_P = [x + y for x, y in zip(Labot_num_P_P, Labot_num_P_H)]
        Tot_Labot_H = [x + y for x, y in zip(Labot_num_H_P, Labot_num_H_H)]
        Tot_Labot  = [x + y for x, y in zip(Tot_Labot_P, Tot_Labot_H)]
        
        Tot_Base1 = Base1_num_H
        Tot_Base2 = Base2_num_H
        Tot_Base3 = Base3_num_H
        
        
        Total_infect = [(x + y + q + w + r + t + z + u + a + s + f) 
                     for x, y, q, w, r, t, z, u, a, s, f in zip(Tot_Recep, 
              Tot_Triag, Tot_WaitU, Tot_WaitN, Tot_AtteU, Tot_AtteN, Tot_Imagi,
                     Tot_Labot, Tot_Base1, Tot_Base2, Tot_Base3)]
        
        Total_infe_P = [(x + y + q + w + r + t + z + u) 
                     for x, y, q, w, r, t, z, u in zip(Tot_Recep_P, 
                  Tot_Triag_P, Tot_WaitU, Tot_WaitN, Tot_AtteU_P, Tot_AtteN_P, 
                                                     Tot_Imagi_P, Tot_Labot_P)]
        
        Total_infe_H = [(x + y + q + w + r + t + z + u + f) 
                     for x, y, q, w, r, t, z, u, f in zip(Tot_Recep_H, 
                  Tot_Triag_H, Tot_AtteU_H, Tot_AtteN_H, Tot_Imagi_H, 
                  Tot_Labot_H, Tot_Base1, Tot_Base2, Tot_Base3 )]
        
        
        for i in range(len(save_results)):
            Total_fomite.append(save_results[i][0][6][0])
            Total_fomite_1.append(save_results[i][0][6][4])
        
        
        
        
        
        # arrays = [np.array(x) for x in Recep_P]
        # Recep_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Triag_P]
        # Triag_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in WaitU_P]
        # WaitU_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in WaitN_P]
        # WaitN_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in AtteU_P]
        # AtteU_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in AtteN_P]
        # AtteN_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Imagi_P]
        # Imagi_P_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Labot_P]
        # Labot_P_stat = [np.mean(k) for k in zip(*arrays)]
        
        # arrays = [np.array(x) for x in Recep_prop_H]
        # Recep_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Triag_prop_H]
        # Triag_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in AtteU_prop_H]
        # AtteU_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in AtteN_prop_H]
        # AtteN_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Imagi_prop_H]
        # Imagi_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Labot_prop_H]
        # Labot_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Base1_prop_H]
        # Base1_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Base2_prop_H]
        # Base2_H_stat = [np.mean(k) for k in zip(*arrays)]
        # arrays = [np.array(x) for x in Base3_prop_H]
        # Base3_H_stat = [np.mean(k) for k in zip(*arrays)]
        
        # Tot_Inf_stat = np.mean(Total_infect) 
        
        # save_PAT = [Recep_P_stat, Triag_P_stat, WaitU_P_stat, WaitN_P_stat,
        #             AtteU_P_stat, AtteN_P_stat, Imagi_P_stat, Labot_P_stat]
        
        # save_HCW = [Recep_H_stat, Triag_H_stat, AtteU_H_stat, AtteN_H_stat,
        #             Imagi_H_stat, Labot_H_stat, Base1_H_stat, Base2_H_stat,
        #             Base3_H_stat]
        
        # mean_total = scipy.stats.bayes_mvs(Total_infect, alpha = 0.95)
        # mean_inf_P = scipy.stats.bayes_mvs(Total_infe_P, alpha = 0.95)
        # mean_inf_H = scipy.stats.bayes_mvs(Total_infe_H, alpha = 0.95)
        
        # mean_total1 = scipy.stats.bayes_mvs(Total_infect1, alpha = 0.95)
        
        # a = 1.0 * np.array(data)
        # n = len(a)
        # m, se = np.mean(a), scipy.stats.sem(a)
        # h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        
        # mean, low_m, upp_m = stats.bayes_mvs(data, alpha = 0.95)
        
        # Base3_H_stat1 = [scipy.stats.bayes_mvs(k, alpha = 0.95) for k in zip(*arrays)]
    
    
    # ax2 = plt.figure(figsize=(6,7), facecolor='w', edgecolor='k')
    # sns.violinplot(data=[Total_infect, Total_infe_P], 
    #                             palette="Set2", inner="quartile")
    
    # ax1 = plt.figure(figsize=(5,7), facecolor='w', edgecolor='k')
    # sns.violinplot(data=[Total_infect, Total_infe_P])
    
    
    palettes = iter(sns.husl_palette(7))

# ax2 = plt.figure(figsize=(13,6), facecolor='w', edgecolor='k')
# plt.rc('xtick', labelsize=20) 
# plt.rc('ytick', labelsize=20) 
# sns.violinplot(data=[Base_TOT, F_co_TOT, Curt_TOT, Vent_TOT, V_Cu_TOT, 
#                  N_VC_TOT, scre_TOT], palette="Set2", inner="quartile")
# # ax2.set_xticklabels(('x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'))
# plt.show()
    mark_s = "6"
    cols = sns.color_palette("Set2",8)
    names = ['Total', 'Patients', 'HCWs', 'Fomites', 'Transm. events\nwith Fomites']
    names = ['Total', 'Patients', 'HCWs', 'Fomites']
    f, ax3 = plt.subplots(figsize=(13,6), facecolor='w', edgecolor='k')
    # ax3.set_yscale("log")
    plt.rc('xtick', labelsize = 17) 
    plt.rc('ytick', labelsize = 17) 
    # sns.stripplot(data=[Base_TOT, F_co_TOT, Curt_TOT, Vent_TOT, V_Cu_TOT, 
    #                       N_VC_TOT, scre_TOT], color=".4")
    
    # sns.boxplot(data=[Total_infect, Total_infe_P,
    #                   Total_infe_H], 
    #   palette = cols,
    #   showmeans = True, 
    #   meanprops={"marker":"s","markerfacecolor":"white", 
    #             "markeredgecolor":"blue","markersize":mark_s})   
    
    # sns.boxplot(data=[Total_infect, Total_infe_P,
    #                   Total_infe_H, Total_fomite, Total_fomite_1], 
                
    sns.boxplot(data=[Total_infect, Total_infe_P,
                      Total_infe_H, Total_fomite], 
      palette = cols,
      showmeans = True, 
      meanprops={"marker":"s","markerfacecolor":"white", 
                "markeredgecolor":"blue","markersize":mark_s})   
    # plt.xticks(np.arange(5), names) 
    plt.xticks(np.arange(4), names) 
    # plt.ylim(top=400) 
    plt.title('Total of newly infected', fontsize = 22)
    #plt.savefig('15_Fom_Base/totals_BCase.pdf', format='pdf', dpi=1400)
    plt.show()
    # 
    
    
    
    # ax3 = plt.figure(figsize=(10,7), facecolor='w', edgecolor='k')
    # sns.boxplot(data=[Tot_Recep_P, 
    #               Tot_Triag_P, Tot_WaitU, Tot_WaitN, Tot_AtteU_P, Tot_AtteN_P, 
    #                                                  Tot_Imagi_P, Tot_Labot_P])
    
    # ax4 = plt.figure(figsize=(10,7), facecolor='w', edgecolor='k')
    # sns.boxplot(data=[Tot_Recep_H, 
    #                   Tot_Triag_H, Tot_AtteU_H, Tot_AtteN_H, Tot_Imagi_H, 
    #                   Tot_Labot_H, Tot_Base1, Tot_Base2, Tot_Base3])
    
    # ax5 = plt.figure(figsize=(10,7), facecolor='w', edgecolor='k')
    # sns.pointplot(data=[Tot_Recep_P, 
    #               Tot_Triag_P, Tot_WaitU, Tot_WaitN, Tot_AtteU_P, Tot_AtteN_P, 
    #              Tot_Imagi_P, Tot_Labot_P] , capsize=.2, join=False, ci=95)
    
    # ax6 = plt.figure(figsize=(10,7), facecolor='w', edgecolor='k')
    # sns.pointplot(data=[Tot_Recep_H, Tot_Triag_H, Tot_AtteU_H, Tot_AtteN_H, Tot_Imagi_H, 
    # Tot_Labot_H, Tot_Base1, Tot_Base2, Tot_Base3],capsize=.2,join=False,ci=95)
    
    # Save_Total_infect = [Tot_Recep, Tot_Triag, Tot_WaitU, Tot_WaitN, Tot_AtteU, 
    #         Tot_AtteN, Tot_Imagi, Tot_Labot, Tot_Base1, Tot_Base2, Tot_Base3]
    
    Save_Total_inf = {'Recep': Tot_Recep, 'Triag': Tot_Triag, 'WaitU': Tot_WaitU,
                      'WaitN': Tot_WaitN, 'AtteU': Tot_AtteU, 'AtteN': Tot_AtteN,
                      'Imagi': Tot_Imagi, 'Labot': Tot_Labot, 'Base1': Tot_Base1,
                      'Base2': Tot_Base2, 'Base3': Tot_Base3, 
                      'Total_inf': Total_infect}
    
    Save_Total_P = {'Recep_P': Tot_Recep_P, 'Triag_P': Tot_Triag_P, 
                    'WaitU_P': Tot_WaitU,   'WaitN_P': Tot_WaitN,  'AtteU_P': Tot_AtteU_P, 
                    'AtteN_P': Tot_AtteN_P, 'Imagi_P': Tot_Imagi_P,'Labot_P': Tot_Labot_P,
                    'Total_inf_P': Total_infe_P}
    
    Save_Total_H = {'Recep_H': Tot_Recep_H, 'Triag_H': Tot_Triag_H, 'AtteU_H': Tot_AtteU_H, 
                    'AtteN_H': Tot_AtteN_H, 'Imagi_H': Tot_Imagi_H, 
                    'Labot_H': Tot_Labot_H, 'Base1': Tot_Base1, 
                      'Base2': Tot_Base2,   'Base3': Tot_Base3,
                'Total_inf_H': Total_infe_H}
    
    Save_from_whom = {
            'Recep_num_P_P': Recep_num_P_P,'Recep_num_P_H': Recep_num_P_H,
            'Recep_num_H_P': Recep_num_H_P,'Recep_num_H_H': Recep_num_H_H,
    
            'Triag_num_P_P': Triag_num_P_P,'Triag_num_P_H': Triag_num_P_H,
            'Triag_num_H_P': Triag_num_H_P,'Triag_num_H_H': Triag_num_H_H,
            
            'WaitU_P_P': WaitU_P_P,'WaitN_P_P': WaitN_P_P,
            
            'AtteU_num_P_P': AtteU_num_P_P,'AtteU_num_P_H': AtteU_num_P_H,
            'AtteU_num_H_P': AtteU_num_H_P,'AtteU_num_H_H': AtteU_num_H_H,
            
            'AtteN_num_P_P': AtteN_num_P_P,'AtteN_num_P_H': AtteN_num_P_H,
            'AtteN_num_H_P': AtteN_num_H_P,'AtteN_num_H_H': AtteN_num_H_H,
            
            'Imagi_num_P_P': Imagi_num_P_P,'Imagi_num_P_H': Imagi_num_P_H,
            'Imagi_num_H_P': Imagi_num_H_P,'Imagi_num_H_H': Imagi_num_H_H,
            
            'Labot_num_P_P': Labot_num_P_P,'Labot_num_P_H': Labot_num_P_H,
            'Labot_num_H_P': Labot_num_H_P,'Labot_num_H_H': Labot_num_H_H,
            
            'Base1_num_H': Base1_num_H,'Base2_num_H': Base2_num_H,
            'Base3_num_H': Base3_num_H  }
    
    Save_Fomites = {'Total_fomites': Total_fomite}
    
    
    Save_Total_infect = pd.DataFrame(data=Save_Total_inf)
    Save_Total_infect.to_excel("15_Fom_Base/Base_Total.xlsx")
    
    Save_Total_Pat = pd.DataFrame(data=Save_Total_P)
    Save_Total_Pat.to_excel("15_Fom_Base/Base_Total_Pat.xlsx")
    
    Save_Total_HCW = pd.DataFrame(data=Save_Total_H)
    Save_Total_HCW.to_excel("15_Fom_Base/Base_Total_HCW.xlsx")

    Save_from = pd.DataFrame(data=Save_from_whom)
    Save_from.to_excel("15_Fom_Base/Base_from_whom.xlsx")
    
    Save_fomite = pd.DataFrame(data=Save_Fomites)
    Save_fomite.to_excel("15_Fom_Base/Base_fomite.xlsx")
    
    t2 = time.perf_counter()
            
    print("finished in " + str(round((t2-t1)/60,2))   + " minute(s)")         
            
# Data_sim = pd.read_excel('2_Case_curtains\curtains_Total.xlsx', index_col=0)
# r_E1 = 1.6
# # r_E2 = 1.5
# # r_E3 = 2
# vals = np.ones(12)
# vals[0] = 1
# vals2 = np.ones(12)
# vals2[0] = 1
# # vals3 = np.ones(11)
# for i in range(12-1):
#     vals[i+1]  = vals[i]  * r_E1
#     vals2[i+1]  = vals2[i]  + vals[i+1]
   # vals2[i+1] = vals2[i] * r_E2
   # vals3[i+1] = vals3[i] * r_E3
    
