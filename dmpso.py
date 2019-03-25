#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:49:45 2019

@author: niranjana

Reference: Applying Particle Swarm Optimization to Quality-of-Service-Driven Web Service Composition , Simone A. Ludwig, https://www.researchgate.net/publication/254028211
"""
import itertools
import numpy as np
import bottleneck
import random
import sys
import math
import time 
import resource 

random.seed(0)
np.random.seed(0)

#Number of abstract nodes
num_nodes = 5#10#int(sys.argv[1])#5

#Number of candidate services
num_services = 5#10#int(sys.argv[2])#20



num_qos = 4
num_iters = 400

graph_name="SEQUENTIAL_"

source = 0
sink = num_nodes

adj_name = graph_name+'autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
adjacencyMatrix = np.load(adj_name)#, delimiter=','np.load('autogen_nodes5_serv5.npy')

qos_serv_name = name = "massive_qos_services_nodes"+str(num_nodes)+"_services"+str(num_services)+'.npy'
unnorm_qos_services = np.load(qos_serv_name)

conc_name = graph_name+'concrete_autogen_nodes'+str(num_nodes)+"_serv"+str(num_services)+'.npy'
concreteAdjacencyMatrix = np.load(conc_name) 

minimize = [0,1]
maximize = [2,3]


'''
Function calculates the Lp criterion utility function
Inputs: Two vectors with three QoS values. One vector is the ideal vector, the other the composed vector
Output: A scalar that is utility value of the composed service as opposed to the optimal service
'''

def calc_Lp(ideal_vector, composed_vector):
    minimized = sum(np.power(abs((ideal_vector[:2] - composed_vector[:2]) / ideal_vector[:2] ),2)) #+ np.power(abs((ideal_vector[3] - composed_vector[3]) / ideal_vector[3] ),2)
    maximized = sum(np.power(abs((ideal_vector[2:] - composed_vector[2:]) / composed_vector[2:] ),2))
    utility = math.pow( minimized+maximized ,0.5)
    if utility==0:
        utility = 1e-4
    return utility

'''
Function to obtain the optimal QoS values for given graph
'''
def optimal():
    arr = unnorm_qos_services
    optimal_arr = []
    
    for i in minimize:
        min_val_qos = 0
        running_index = 0
        for k in range(num_nodes):
            numserv = num_services
            running_index += numserv
            min_val_qos += np.min(arr[running_index - numserv: running_index,i])
        optimal_arr.append(min_val_qos)
    
    for i in maximize:
        max_val_qos = 1.0
        running_index = 0
        for k in range(num_nodes):
            numserv = num_services
            running_index += numserv
            max_val_qos *= np.max(arr[running_index - numserv: running_index,i])
        optimal_arr.append(max_val_qos)
    
    optimal_arr = np.asarray(optimal_arr)
    return optimal_arr


'''
Function to calculate aggregate QoS over a given path according to some objective functions. 
It calculates values and returns them for response time, cost , reliability and availability.
'''
def getAggQos(path):
    rt = 0
    cost = 0
    rel = 1.0
    av = 1.0

    for i in path:
        i = int(i)
        rt += unnorm_qos_services[i,0]
        cost += unnorm_qos_services[i,1]
        rel *= unnorm_qos_services[i,2]
        av *= unnorm_qos_services[i,3]
        
    return np.asarray([rt, cost, rel, av])
        
'''
Function to evaluate if Q is better than Q_n.
'''
def qosIsBetter(Q, Q_n):
    #returns True value if Q is better than Q_n, that is Q is within the constraints set by user.
    if Q[0]<=Q_n[0] and Q[1]<=Q_n[1] and Q[2]>=Q_n[2] and Q[3]>=Q_n[3]:
        return True
    else:
        return False
'''
Function that updates position based on provided velocity.
'''
def swap(position, swaps):
    for swap_sequence in swaps:
        i = swap_sequence[0]
        j = swap_sequence[1]
        position = np.asarray(position)
        position = np.where(position==i, j, position)
    return position

'''
Function to generate all possible solutions given the number of abstract abnd candidate services.
'''
def generate_particles():
    particles = []
    possible_permutations = []
    for i in range(0,num_nodes):
        temp = list(range(i*num_services,(i+1)*(num_services)))
        possible_permutations.append(temp)
    particles = list(itertools.product(*possible_permutations))
    return np.asarray(particles)


'''
Function to retrieve N best particles according to their L_p metric. 
It calculates the L_p metric of all possible solutions, sorts them and return the N best candidates.
'''
def get_particles(particles, num_particles, optimal_qos):
    particles_new = np.zeros(shape=particles.shape)
    particles_new[:, 0:num_nodes] = particles 
    column = np.zeros(shape=(len(particles),1))
    particles_new = np.append(particles_new, column, axis = 1)
    
    for i in range(0,len(particles_new)):
        particles_new[i, num_nodes] = 1.0/calc_Lp(getAggQos(particles[i, 0:num_nodes]),optimal_qos)
        
    #ind = np.argsort(particles_new[:,num_nodes])[::-1][:num_particles]
    ind = bottleneck.argpartition(particles_new[:,num_nodes], num_particles)[:num_particles]
    particles_pick = particles_new[ind,:-1]
    return particles_pick

'''
Function to calculate velocity or swap sequence that is needed to make sequence1 into sequence 2.
'''
def getVelocity(sequence1, sequence2):
    v = [[0,0]]
    for i in range(0,len(sequence1)):
        elem1 = sequence1[i]
        elem2 = sequence2[i]
        
        if elem1 != elem2:
            swap_sequence = [[elem2,elem1]]
            v=v+swap_sequence
    return v

'''
Function to update position of particle based on velocity provided. Returns new velocities based on cefiicient provided.
Update is done in the main loop after all three velocities have calculated - social, cognitive and current.
'''
def updatePosition(coeff, sequence, changes): 
    
    if coeff < 1:
        #delete single change
        if changes:
            ind = random.randint(0, len(changes)-1)
            if changes[ind]:
                flipped_swap_sequence = np.flip(changes[ind], axis=0)
                flipped_swap_sequence = [list(flipped_swap_sequence)]
                #sequence = swap(sequence, flipped_swap_sequence)
                changes.pop(ind)
        
    elif coeff > 1:
        #add random changes
        ind = random.randint(0, len(sequence)-1)
        elem1 = sequence[ind]
        elem2 = random.randint((ind)*num_services, (ind+1)*(num_services)-1)
        v = [elem1, elem2]
        changes.append(v)
        
    #elif coeff == 1: do nothing, continue as is
    
    return changes
       
if __name__=='__main__':
    print("-----------------------------------------------------------")
    num_particles = 20
    print("Nodes: ",num_nodes, "Services: ",num_services, "Num particles: ",num_particles)
    start = time.time()
    optimal_qos = optimal()
    name = graph_name+'q_c_nodes_'+str(num_nodes)+"_serv"+str(num_services)+'.npy'
    Q_c = np.load(name)
    particles = generate_particles()
    particles = get_particles(particles, num_particles, optimal_qos)

    
    p_best = float('inf')*np.ones(particles.shape)
    g_best = float('inf')
    g_best_pos = float('inf')*np.ones(num_nodes)
    p_best_pos = particles
    global_best_qos = float('inf')*np.ones(4)
    

    v_prev = [[[0,0]] for i in particles]
    velocity = [[[0,0]] for i in particles]
    
    
    for itera in range(0,num_iters):
        print("Iteration: ",itera, len(particles))
        
        velocity = [[[0,0]] for i in particles]

        for i in range(0, len(particles)):
            particle_fitness = 1.0/calc_Lp(getAggQos(particles[i]),optimal_qos)
#            print("Particle fitness evaluated")
            if itera == 0:
                personal_best = float('inf')
                global_best = float('inf')
            else:
                personal_best = 1.0/calc_Lp(getAggQos(p_best_pos[i]),optimal_qos)
#                global_best = 1.0/calc_Lp(getAggQos(g_best),optimal_qos)
#            print("Personal best",personal_best)
#            print("Global best", global_best)
            
            if  personal_best > particle_fitness:
                p_best[i] = particle_fitness
                p_best_pos[i] = particles[i] 
        
            if g_best > particle_fitness:
                g_best = particle_fitness
                #g_best = np.argmax(p_best)
                g_best_pos = particles[i]
                #global_best_qos = getAggQos(g_best_pos)
        
        term_criterion = qosIsBetter(getAggQos(g_best_pos),Q_c)  

        
        if(term_criterion): 
            print("Convergence at iteration ", itera)
            print("Values: ", g_best_pos)
            break
        
        for i in range(0,len(particles)):

            W = 0.9 * random.uniform(0,2)
            c1 = 0.5 * random.uniform(0,2)
            c2 = 0.69 * random.uniform(0,2)
            
            cognitive = getVelocity(p_best_pos[i] , particles[i])
            social = getVelocity(g_best_pos,particles[i])
            
            weight_vel = updatePosition(W, particles[i], v_prev[i])
            updated_vel_cog = updatePosition(c1, particles[i], cognitive)
            updated_vel_soc = updatePosition(c2, particles[i], social)
                  
            updated_velocity = weight_vel + updated_vel_cog + updated_vel_soc
            
            velocity[i] = velocity[i] + updated_velocity
            

            particles[i] = swap(particles[i] , velocity[i])    
            
        v_prev = velocity
    end =  time.time() - start
    print("Time taken to execute (s): ", end )
    print("Iterations taken: ", itera)
    res_var = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("Memory used (kB): ", res_var)
    print("Constraints: ",Q_c)
    print("Aggregate solution quality: ", getAggQos(g_best_pos))