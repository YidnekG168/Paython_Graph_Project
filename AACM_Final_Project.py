#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:50:33 2018

@author: ous

store only two fitness -normal and special
graph = degree of only one sepecial node and one normal node
you don't need to store a snapshot of the graph at each timestep
"""

import matplotlib.pyplot as plt
from numpy import random
from collections import defaultdict
import json

class MyGraph:    
    def __init__(self, m, nc, maxNode, n_fraction, nNodeToGraph, sNodeToGraph):
        self.noOfPriviledgeNodes=m
        self.nc=nc
        self.maxNode= maxNode       
        self.specialFitnessGrowthLimit=(n_fraction/100) * self.maxNode

        self.normalDegreeForGraphing=nNodeToGraph
        self.specialDegreeForGraphing=sNodeToGraph
        self.specialNodeDegrees = defaultdict(dict)
        self.normalNodeDegrees = defaultdict(dict)

        self.specialNodeFitness = defaultdict(dict)
        self.normalNodeFitness = defaultdict(dict)

        self.timeStep=0
        self.sumDegreeAndFitness=0

        self.G=defaultdict(dict)
        self.GFitness=defaultdict(dict)
        #self.GFitness1=defaultdict(dict)

        self.addInitialNormalNodes()
        
    #Add inital 10 nodes and their fitnesses, including 4 special nodes
    def addInitialNormalNodes(self):
        for nn in range(1,11):
            self.timeStep +=1
            if nn == 1:
                self.G[nn]=[nn+1,10]
            elif nn==10:
                self.G[nn]=[1, nn-1]
            else:
                self.G[nn]=[nn-1, nn+1]

            #add special fitnesses
            if self.timeStep <= self.specialFitnessGrowthLimit:
                self.GFitness['special']=self.timeStep
                
            if(nn>=self.specialDegreeForGraphing):
                self.specialNodeFitness[self.timeStep] = self.getNodeFitness(self.specialDegreeForGraphing)

        #add normal fitnesses
        self.GFitness['normal']=self.nc

        self.normalNodeFitness[self.timeStep] = self.getNodeFitness(self.normalDegreeForGraphing)

    #check if a node is a special node
    def isSpecialNode(self, node):
        if node in [2,3,4,5]:
            return True
        else:
            return False
        
    #get degree of a node      
    def getNodeDegree(self, node):
        return len(self.G[node])
    
    #get fitness of a node
    def getNodeFitness(self, node):
        if self.isSpecialNode(node)==True:
            return self.GFitness['special']
        else:
            return self.GFitness['normal']
           
    #sum of derees * fitnesses
    def sumDegreeFitness(self):
        sumDF=0
        for n in self.G:
            sumDF +=(self.getNodeDegree(n)*self.getNodeFitness(n))
        return sumDF
    
    #node probability distribution formula
    def getNodeProbList(self):
        nProbList=list()
        for node in self.G:
            nProbList.append((self.getNodeDegree(node) * self.getNodeFitness(node)) / self.sumDegreeFitness())

        return nProbList
 
    #get random privilege nodes for attachment
    def getPrivilegeNodes(self):
        return random.choice(a=list(self.G.keys()),p=self.getNodeProbList(), replace=False, size=self.noOfPriviledgeNodes)
          
    #store special node and normal node degrees at the specified time step
    def storeDegreesAtTimeStep(self, atStep):
        self.specialNodeDegrees[self.timeStep] = self.getNodeDegree(self.specialDegreeForGraphing)
        self.normalNodeDegrees[self.timeStep] = self.getNodeDegree(self.normalDegreeForGraphing)

        self.specialNodeFitness[self.timeStep] = self.getNodeFitness(self.specialDegreeForGraphing)
        self.normalNodeFitness[self.timeStep] = self.getNodeFitness(self.normalDegreeForGraphing)


        """for n in self.G:
            if self.isSpecialNode(n):
                self.specialNodeDegrees[self.timeStep][n] = self.getNodeDegree(n)
            else:
                self.normalNodeDegrees[self.timeStep][n] = self.getNodeDegree(n)
        """
    #new node
    def newExtraNode(self, node):            
        self.timeStep +=1
        privNodes = self.getPrivilegeNodes()
        self.G[node] = privNodes.tolist()
        for pNode in privNodes:
            self.G[pNode].append([node])

        #store special node degrees and normal node degrees at this step  
        self.storeDegreesAtTimeStep(self.timeStep)
        
        #add special fitnesses
        if self.timeStep <= self.specialFitnessGrowthLimit:
            self.GFitness['special']=self.timeStep
            
        #store fitnesses at this timestep
        #special node fitnessed increase during the first stage (asumed to be n_fraction percent of the total nodes) of the growing network and then remain constant
        """for n in self.G:
            if self.isSpecialNode(n)==True:
                if self.timeStep > self.specialFitnessGrowthLimitTimestep:
                    #at this stage, the fiyness of n at timestanp self.specialFitnessGrowthLimitTimestep does not exist
                    if(self.specialFitnessGrowthLimitTimestep <= n):
                        self.GFitness[self.timeStep][n] = 0
                    else:
                        self.GFitness[self.timeStep][n] = self.GFitness[self.specialFitnessGrowthLimitTimestep][n]
                else:
                    self.GFitness[self.timeStep][n] = self.timeStep
            #if not special node
            else:
                self.GFitness[self.timeStep][n] = self.nc
                
                self.sumDegreeAndFitness +=(self.getNodeDegree(n)*self.getNodeFitness(n))"""
                
    #on two pdf files, draw graphs of normal nodes against their degrees and special nodes against their degrees
    def drawGraph(self, gtype):
        figure = plt.figure()
        #normalFinalTimeStepKey=list(self.normalNodeDegrees.keys())[-1]
        x0=list(self.normalNodeDegrees.keys())
        y0=list(self.normalNodeDegrees.values())
        plt.plot(x0, y0, label='normal node: '+str(self.normalDegreeForGraphing))
        
        #specialFinalTimeStepKey=list(self.specialNodeDegrees.keys())[-1]
        x1=list(self.specialNodeDegrees.keys())
        y1=list(self.specialNodeDegrees.values())
        plt.plot(x1, y1, label='special node: '+str(self.specialDegreeForGraphing))

        plt.legend()
        plt.xlabel('Time Step')
        plt.ylabel('Degree')
        
        if(gtype=='log'):
            ttp='Log-Log'
        elif(gtype=='linear'):
            ttp='Linear'
            
        plt.title('Normal and Special Nodes Time Step Against Degrees - '+ttp)
        plt.xscale(gtype)
        plt.yscale(gtype)
        plt.show()
        
        figure.savefig("m-"+str(self.noOfPriviledgeNodes)+"_"+"nc-"+str(self.nc)+"_max-"+str(self.maxNode)+"_"+ttp+"_output.pdf")

    def drawFitnessGraph(self, gtype):
        figure = plt.figure()
        #normalFinalTimeStepKey=list(self.normalNodeDegrees.keys())[-1]
        x0=list(self.normalNodeFitness.keys())
        y0=list(self.normalNodeFitness.values())
        plt.plot(x0, y0, label='normal node: '+str(self.normalDegreeForGraphing))
        
        #specialFinalTimeStepKey=list(self.specialNodeDegrees.keys())[-1]
        x1=list(self.specialNodeFitness.keys())
        y1=list(self.specialNodeFitness.values())
        plt.plot(x1, y1, label='special node: '+str(self.specialDegreeForGraphing))

        plt.legend()
        plt.xlabel('Time Step')
        plt.ylabel('Fitness')
        
        if(gtype=='log'):
            ttp='Log-Log'
        elif(gtype=='linear'):
            ttp='Linear'
            
        plt.title('Normal and Special Nodes Time Step Against Degrees - '+ttp)
        plt.xscale(gtype)
        plt.yscale(gtype)
        plt.show()
        
        figure.savefig("m-"+str(self.noOfPriviledgeNodes)+"_"+"nc-"+str(self.nc)+"_max-"+str(self.maxNode)+"_"+ttp+"_output.pdf")


# read input file
with open('input.json', 'r') as input_file:
    data=input_file.read()

# parse file
input_obj = json.loads(data)

#create an object of class MyGraph   
g=MyGraph(input_obj['m'],input_obj['nc'],input_obj['max_n'],input_obj['n_fraction'],input_obj['normal_node_to_graph'],input_obj['special_node_to_graph'])

for n in range(10, input_obj['max_n'], 1):
    g.newExtraNode(n)

print(g.drawGraph('linear'))
print(g.drawGraph('log'))

print(g.drawFitnessGraph('linear'))
print(g.drawFitnessGraph('log'))