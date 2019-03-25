#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:27:30 2019

@author: niranjana
"""
import sys
from igraph import *
import numpy as np
import random

random.seed(19950807)

print("Executing")

num_nodes = int(sys.argv[1])
#num_nodes = int(input("Enter number of nodes"))

num_services = int(sys.argv[2])
#num_services = int(input("Enter number of services"))
num_qos = 4



def getSubgraph1(startNode, endNode, g):

    g1 = g

    #The subgraph is 5 nodes big, therefore divide by 5
    for i in range((startNode/5), (endNode/5)):
        #print("I is: ",i)
        node = i*5 #- 4
        g1.add_edges([(node,node+1), (node,node+2)])
        g1.add_edges([(node+1, node+3), (node+1, node+4)])
        g1.add_edges([(node+2, node+3), (node+2, node+4)])
        g1.add_edges([(node+3, node+4)])
        
        if (i == 0):
            prevnode = node
            continue
        else:
            prevnode = (i-1)*5
            g1.add_edges([( prevnode + 3, node), (prevnode + 4, node)])
                
#    adjacencyMatrix = g1.get_adjacency(type=2).data
#    adjacencyMatrix = np.asarray(adjacencyMatrix)
#    
#    name = 'STRUCTURED_g1_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
#    np.save(name,adjacencyMatrix, delimiter=',',newline='\n')
#    fmt = np.loadtxt(name, delimiter=',')
    
    return g1

################################################################################################################

def getSubgraph2(startNode, endNode, g):
    g2 = g

    
    #The subgraph is 5 nodes big, therefore divide by 5
    for i in range((startNode/5), (endNode/5)):
        #print("I is: ",i)
        node = i*5 #- 4
        g2.add_edges([(node,node+1), (node,node+2)])
        g2.add_edges([(node+1, node+2)])
        g2.add_edges([(node+2, node+3), (node+2, node+4)])
        g2.add_edges([(node+3, node+4)])
        
        if (i == 0):
            prevnode = node
            continue
        else:
            prevnode = (i-1)*5
            g2.add_edges([(prevnode + 4, node)])
            
        
#    adjacencyMatrix = g2.get_adjacency(type=2).data
#    adjacencyMatrix = np.asarray(adjacencyMatrix)
#    
#    name = 'STRUCTURED_g2_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
#    np.save(name,adjacencyMatrix, delimiter=',',newline='\n')
#    fmt = np.loadtxt(name, delimiter=',')
    
    return g2
################################################################################################################

def getSubgraph3(startNode, endNode, g):
    g3 = g
    
    #The subgraph is 5 nodes big, therefore divide by 5
    for i in range((startNode/5), (endNode/5)):
        #print("I is: ",i)
        node = i*5 #- 4
        g3.add_edges([(node,node+1), (node,node+2), (node,node+3)])
        g3.add_edges([(node+1, node+2)])
        g3.add_edges([(node+2, node+3), (node+2, node+4)])
        g3.add_edges([(node+3, node+4)])
        
        if (i == 0):
            prevnode = node
            continue
        else:
            prevnode = (i-1)*5
            g3.add_edges([(prevnode + 4, node), (prevnode + 4, node+3)])
    
#    adjacencyMatrix = g3.get_adjacency(type=2).data
#    adjacencyMatrix = np.asarray(adjacencyMatrix)
#    
#    name = 'STRUCTURED_g3_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
#    np.save(name,adjacencyMatrix, delimiter=',',newline='\n')
#    fmt = np.loadtxt(name, delimiter=',')
    
    return g3

################################################################################################################
def getSubgraph4(startNode, endNode, g):
    g4 = g

    
    #The subgraph is 5 nodes big, therefore divide by 5
    for i in range((startNode/5), (endNode/5)):
        #print("I is: ",i)
        node = i*5
        g4.add_edges([(node,node+1)])
        g4.add_edges([(node+1, node+2), (node+1, node+3)])
        g4.add_edges([(node+2, node), (node+2, node+1), (node+2, node+3)])
        g4.add_edges([(node+3, node+4)])
        
        if (i == 0):
            prevnode = node
            continue
        else:
            prevnode = (i-1)*5
            g4.add_edges([(prevnode + 4, node)])
    
    
#    adjacencyMatrix = g4.get_adjacency(type=2).data
#    adjacencyMatrix = np.asarray(adjacencyMatrix)
#    
#    name = 'STRUCTURED_g4_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
#    np.save(name,adjacencyMatrix, delimiter=',',newline='\n')
#    fmt = np.loadtxt(name, delimiter=',')

    return g4
################################################################################################################

def getSubgraph5(startNode, endNode, g):
    g5 = g
    
    #The subgraph is 5 nodes big, therefore divide by 5
    for i in range((startNode/5), (endNode/5)):
        #print("I is: ",i)
        node = i*5
        g5.add_edges([(node,node+1)])
        g5.add_edges([(node+1, node+2)])
        g5.add_edges([ (node+2, node+3), (node+2, node+4)])
        g5.add_edges([(node+3, node+4),(node+3, node+1)])
        
        if (i == 0):
            prevnode = node
            continue
        else:
            prevnode = (i-1)*5
            g5.add_edges([(prevnode + 4, node)])
    


    return g5

def getConcreteMatrix(adjacencyMatrix):
    length_dict = np.asarray([len(value) for key, value in abstractNodeDict.items()])
    s = np.sum(length_dict)
    concreteAdjacencyMatrix = np.zeros((s, s, num_qos))
    print("NEW MATRIX SHAPE: ",concreteAdjacencyMatrix.shape)
    
    
    running_index = 0
    for i in range(0,nodes):
        
        temp = abstractNodeDict["Node"+str(i)]
        numserv = len(temp)
        running_index += numserv
        nodeat = i*numserv
        running_index_j = 0
        for j in range(0,nodes):
            new_num_serv = len(abstractNodeDict["Node"+str(j)])
            running_index_j += new_num_serv
            #print("J MAT",running_index_j)
            if adjacencyMatrix[i,j]!=0:
                #DONE: TODO: this will be a problem when the number of services per node changes, use the code from optimal()
                concreteAdjacencyMatrix[running_index-numserv:running_index, running_index_j-new_num_serv:running_index_j, :] = adjacencyMatrix[i,j]*temp
    
    return concreteAdjacencyMatrix

    


def getOrderedAdjacencyMatrix(adjacencyMatrix):
    adjacencyMatrix_new = adjacencyMatrix#np.zeros(shape=adjacencyMatrix.shape)
    for i in range(0,len(adjacencyMatrix)):
        for j in range(0,len(adjacencyMatrix)):
            if (i>j) and (adjacencyMatrix[i,j]!=0):
               adjacencyMatrix_new[i,j] = -1*adjacencyMatrix[i,j] 
    
    return adjacencyMatrix_new


########################################################################################################

nodes = num_nodes#+2

abstractNodeDict = dict()

qos = []
for j in range(0, num_services):
   rt = random.uniform(0.0001,0.34) #120000*(float(i*num_services/num_nodes)/100)
   cost = random.uniform(0.0001,0.50) #10000*(float(i*num_services/num_nodes)/100)
   reliability =  random.uniform(0.95, 1.0) #0.95 + (float(i*num_services/num_nodes)/100)
   availability = random.uniform(0.97, 1.0) #0.97 + (float(i*num_services/num_nodes)/100)
   temp = [rt , cost , reliability , availability]
   qos.append(temp)
   
for i in range(0, nodes):
    node_str = "Node"+str(i)
    abstractNodeDict[node_str] = np.asarray(qos)

#print(abstractNodeDict)
unnorm_qos_services = np.zeros((num_nodes*num_services, num_qos))
for i in range(0,num_nodes):
    current_qos = abstractNodeDict["Node"+str(i)]
    #for j in range(0,len(current_qos)):
    unnorm_qos_services[i*len(current_qos):(i+1)*len(current_qos)] = current_qos
name = "massive_qos_services_nodes"+str(num_nodes)+"_services"+str(num_services)+'.npy'
np.save(name, unnorm_qos_services)


numservs = []
for i in range(0, nodes):
    numservs.append(len(abstractNodeDict["Node"+str(i)]))
numservs = np.asarray(numservs)

##################################################################################################################

    
#if __name__=='__main__':

g = Graph()
g.add_vertices(num_nodes)#+2
g.to_directed()


for i in range(0, num_nodes):
    if i%5 == 0:
        start = i
        end = start + 5
        sub_num = random.randint(0,4)
        print("subgraph selected: ", sub_num+1)
        if sub_num == 0:
            g = getSubgraph1(start, end, g)
        elif sub_num == 1:
            g = getSubgraph2(start, end, g)
        elif sub_num == 2:
            g = getSubgraph3(start, end, g)
        elif sub_num == 3:
            g = getSubgraph4(start, end, g)
        elif sub_num == 4:
            g = getSubgraph5(start, end, g)
        else:
            print("Invalid subgraph",sub_num)

    
adjacencyMatrix = g.get_adjacency(type=2).data
adjacencyMatrix = np.asarray(adjacencyMatrix)
adjacencyMatrix = getOrderedAdjacencyMatrix(adjacencyMatrix)

name = 'STRUCTURED_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
np.save(name,adjacencyMatrix)#, delimiter=',',newline='\n'
#fmt = np.loadtxt(name, delimiter=',')

concreteAdjacencyMatrix = getConcreteMatrix(adjacencyMatrix)
name = 'STRUCTURED_concrete_autogen_nodes'+str(num_nodes)+"_serv"+str(num_services)+'.npy'
#np.save(name,concreteAdjacencyMatrix, delimiter=',',newline='\n')
np.save(name, concreteAdjacencyMatrix)
#fmt = np.load(name)
#
#
'''

############################################################################################################################################
SEQUENTIAL GRAPH

'''
g = Graph()
g.add_vertices(num_nodes)#+2
g.to_directed()


#g.add_edges([(0,1)])
#The subgraph is 5 nodes big, therefore divide by 5
for i in range(0,(num_nodes/5)):
    print("I is: ",i)
    node = i*5 #- 4
    g.add_edges([(node,node+1)])
    g.add_edges([(node+1, node+2)])
    g.add_edges([(node+2, node+3)])
    g.add_edges([(node+3, node+4)])
    
    if (i == 0):
        prevnode = node
        continue
    else:
        prevnode = (i-1)*5
        g.add_edges([( prevnode + 4, node)])
        

adjacencyMatrix = g.get_adjacency(type=2).data
adjacencyMatrix = np.asarray(adjacencyMatrix)
adjacencyMatrix = getOrderedAdjacencyMatrix(adjacencyMatrix)

name = 'SEQUENTIAL_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
np.save(name,adjacencyMatrix)#, delimiter=',',newline='\n'
#fmt = np.loadtxt(name, delimiter=',')


concreteAdjacencyMatrix = getConcreteMatrix(adjacencyMatrix)
name = 'SEQUENTIAL_concrete_autogen_nodes'+str(num_nodes)+"_serv"+str(num_services)+'.npy'
#np.save(name,concreteAdjacencyMatrix, delimiter=',',newline='\n')
np.save(name, concreteAdjacencyMatrix)
#fmt = np.load(name)

'''

############################################################################################################################################
FULLY CONNECTED GRAPH

'''
g = Graph()
g.add_vertices(num_nodes)#+2
g.to_directed()


#g.add_edges([(0,1)])
#The subgraph is 5 nodes big, therefore divide by 5
for i in range(0,(num_nodes/5)):
    print("I is: ",i)
    node = i*5 #- 4
    g.add_edges([(node,node+1), (node,node+2), (node,node+3), (node,node+4)])
    g.add_edges([(node+1, node+2), (node+1, node+3), (node+1, node+4), (node+1, node)])
    g.add_edges([(node+2, node+3), (node+2, node+4), (node+2, node+1), (node+2, node)])
    g.add_edges([(node+3, node+4), (node+3, node+2), (node+3, node+1), (node+3, node)])
    
    if (i == 0):
        prevnode = node
        continue
    else:
        prevnode = (i-1)*5
        g.add_edges([( prevnode + 4, node), ( prevnode + 3, node), ( prevnode + 2, node), ( prevnode + 1, node), ( prevnode , node)])
        


adjacencyMatrix = g.get_adjacency(type=2).data
adjacencyMatrix = np.asarray(adjacencyMatrix)
adjacencyMatrix = getOrderedAdjacencyMatrix(adjacencyMatrix)

name = 'FULLY_CONNECTED_autogen_nodes'+str(num_nodes)+'_serv'+str(num_services)+'.npy'
np.save(name,adjacencyMatrix)#, delimiter=',',newline='\n'
#fmt = np.loadtxt(name, delimiter=',')

concreteAdjacencyMatrix = getConcreteMatrix(adjacencyMatrix)
name = 'FULLY_CONNECTED_concrete_autogen_nodes'+str(num_nodes)+"_serv"+str(num_services)+'.npy'
#np.save(name,concreteAdjacencyMatrix, delimiter=',',newline='\n')
np.save(name, concreteAdjacencyMatrix)
#fmt = np.load(name)
