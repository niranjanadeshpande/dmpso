#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 18:33:29 2019

@author: niranjana
"""
import numpy as np
import math

#path_length = [5]#[5,10,20, 30, 40, 50, 100, 200, 300, 400, 500]
#cand_serv = [10]#[5, 10, 15, 20, 25, 30, 35, 40, 50]
#selected_servs = [4, 8, 16, 40, 80, 160, 240, 320, 400]

path_length = [5, 10, 20]#, 30, 40,50, 100]#, 200, 300, 400, 500] #[]
cand_serv = [5, 10, 15, 20, 25, 30, 35, 40] #, 50
types = [0 , 1, 2]

Q_c = [0.0, 0.0, 0.0, 0.0]
Q_c = np.asarray(Q_c)

counter = -1

for i in path_length:
    counter = counter+1
    for j in cand_serv:
        for k in types:
            
            if k==0:
                graph_name="SEQUENTIAL_"
            elif k==1:
                graph_name="STRUCTURED_"
            elif k==2:
                graph_name="FULLY_CONNECTED_"
            
            #path_len_mat = np.load(graph_name+'autogen_nodes'+str(i)+'_serv'+str(j)+'.npy')
            path_len = i#3*(i/5)#len(path_len_mat)-2#path_lens[counter]#
            
            name = "massive_qos_services_nodes"+str(i)+"_services"+str(j)+'.npy'
            unnorm_qos_services = np.load(name)
            
            
            median_rt = np.median(unnorm_qos_services[:,0])#1e-4 + 1.0*0.3399/4.0#np.median(unnorm_qos_services[:,0])#np.max(unnorm_qos_services[:,0])#1e-4 + 3*0.3399/4.0###np.mean(unnorm_qos_services[:,0])
            #median_rt = median_rt - 0.25*median_rt
            
            median_cost = np.median(unnorm_qos_services[:,1])#1e-4 + 1.0*0.4999/4.0#np.median(unnorm_qos_services[:,1])#np.max(unnorm_qos_services[:,1])#1e-4 + 3*0.4999/4.0###np.mean(unnorm_qos_services[:,1])
            #median_cost = median_cost - 0.25*median_cost
            
            median_rel = np.median(unnorm_qos_services[:,2])#0.95 + 3*0.05/4.0#np.median(unnorm_qos_services[:,2]) #np.min(unnorm_qos_services[:,2])#0.95 + 3*0.05/4.0###np.mean(unnorm_qos_services[:,2])
            #median_rel = median_rel + 0.25*median_rel
            
            median_av = np.median(unnorm_qos_services[:,3])#0.97 + 3*0.03/4.0#np.median(unnorm_qos_services[:,3])#np.min(unnorm_qos_services[:,3])#0.97 + 3*0.03/4.0###np.mean(unnorm_qos_services[:,3])
            #median_av = median_av + 0.25*median_av
            
            if max(unnorm_qos_services[:,0])==median_rt or min(unnorm_qos_services[:,0])==median_rt:
                median_rt *=2
            if max(unnorm_qos_services[:,1])==median_cost or min(unnorm_qos_services[:,1])==median_cost:
                median_cost *=2
            if max(unnorm_qos_services[:,2])==median_rel or min(unnorm_qos_services[:,2])==median_rel:
                median_rel /=2
            if max(unnorm_qos_services[:,3])==median_av or min(unnorm_qos_services[:,3])==median_av:
                median_av /=2
            
            Q_c[0] = median_rt*path_len*1.1#(selected_servs[counter])#- 1
            #Q_c[0] = Q_c[0]*0.6
            Q_c[1] = median_cost*path_len*1.1#(selected_servs[counter] )#- 1
            #Q_c[1] = Q_c[1]*0.6
            Q_c[2] = median_rel**(path_len*1.09)#math.pow(median_rel,i)#(selected_servs[counter])#- 1
            #Q_c[2] = Q_c[2]*0.5
            Q_c[3] = median_av**(path_len*1.09)#math.pow(median_av,i)#(selected_servs[counter])#- 1
            #Q_c[3] = Q_c[3]*0.5
            #Q_c = Q_c*(3.0/5.0)
            print(Q_c)
            print(median_rt, median_cost, median_rel, median_av)
            name = graph_name+'q_c_nodes_'+str(i)+"_serv"+str(j)+'.npy'
            np.save(name, Q_c)