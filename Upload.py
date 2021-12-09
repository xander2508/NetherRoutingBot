import json
from os import listdir
from os.path import isfile, join
import sys,os #pygame,
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re,pygraphviz,math,graphviz
import networkx as nx
import matplotlib.image as mpimg
import threading
import time
from PIL import Image
import discord,os
from discord.ext import commands
import difflib

class Waypoint:
    def __init__(self,x,y,z,direction,directionWalk,directionWalkElvList,floating):
        self.x = x
        self.y = y
        self.z = z
        self.floating = floating
##        if self.x==-3080 and self.z==2384:
##            print(direction)
        self.enabled = True
        self.direction = direction
        self.directionWalk = directionWalk
        self.directionWalkElvList = directionWalkElvList
        self.connectedTo = [()]
        self.connectedToWalk = [()]
        self.connectedToWalkElvList = [()]
        self.graphID = -1
    def calculateConnected(self,waypointClasses):
        self.connectedTo = self.calculateConnectedDirection(waypointClasses,self.direction,"I")
        self.connectedToWalk = self.calculateConnectedDirection(waypointClasses,self.directionWalk,"W")
        self.connectedToWalkElvList =self.calculateConnectedDirection(waypointClasses,self.directionWalkElvList,"WU")

            
    def returnName(self):
        return ""
    def calculateConnectedDirection(self,waypointClasses,directionList,dirofway):
        #DO DIAG#########
        outputConnections = []
        for directionNum,direction in enumerate(directionList):
            if direction:
                if directionNum == 0:
                    closest = []
                    for waypoint in waypointClasses:
                        if self.x == waypoint.x:
                            if self.z > waypoint.z:
                                if dirofway == "I":
                                    if waypoint.direction[4] == True:
                                        closest.append(waypoint.z)
                                elif dirofway == "W":
                                    if waypoint.directionWalk[4] == True:
                                        closest.append(waypoint.z)
                                else:
                                    if waypoint.directionWalkElvList[4] == True:
                                        closest.append(waypoint.z)
                    closest.sort()
                    if len(closest)>=1:
                        closest.reverse()
                    chosen = False
                    for k in closest:
                        
                        if k != self.z and not chosen:
                            outputConnections.append((self.x,k,False))
                            chosen = True
                    if not chosen:
                        outputConnections.append((self.x,self.z-20,True))

                        
                elif directionNum == 1:
                    #North East
                    #+1 -1
                    #1000 800 = 200
                    #2000 2200 = 200
                    closest = []
                    closest2= {}
                    for waypoint in waypointClasses:
                        if waypoint.x-self.x == self.z-waypoint.z:
                            if dirofway == "I":
                                if waypoint.direction[5] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            elif dirofway == "W":
                                if waypoint.directionWalk[5] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            else:
                                if waypoint.directionWalkElvList[5] == True:
                                    
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                                
                    closest.sort()
                    if len(closest)>=1:
                        if closest[0] == 0.0:
                            try:
                                outputConnections.append((closest2[str(closest[1])][0],closest2[str(closest[1])][1],False))
                            except:
                                outputConnections.append((self.x+20,self.z-20,True))
                        else:
                            outputConnections.append((closest2[str(closest[0])][0],closest2[str(closest[0])][1],False))
                    else:
                        outputConnections.append((self.x+20,self.z-20,True))
                
                elif directionNum == 2:
                    closest = []
                    for waypoint in waypointClasses:
                        if self.z == waypoint.z:
                            if self.x <= waypoint.x:
                                if dirofway == "I":
                                    if waypoint.direction[6] == True:
                                        closest.append(waypoint.x)
                                elif dirofway == "W":
                                    if waypoint.directionWalk[6] == True:
                                        closest.append(waypoint.x)
                                else:
                                    if waypoint.directionWalkElvList[6] == True:
                                        closest.append(waypoint.x)
                                
                    closest.sort()
                    chosen = False
                    for k in closest:
                        if k != self.x and not chosen:
                            outputConnections.append((k,self.z,False))
                            chosen = True
                    if not chosen:
                        outputConnections.append((self.x+20,self.z,True))
                    
                elif directionNum == 3:
                    #South East
                    #+1 +1
                    #1000 800 = 200
                    #2000 1800 = 200
                    closest = []
                    closest2= {}
                    for waypoint in waypointClasses:
                        if waypoint.x-self.x == waypoint.z-self.z:
                            if dirofway == "I":
                                if waypoint.direction[7] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            elif dirofway == "W":
                                if waypoint.directionWalk[7] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            else:
                                if waypoint.directionWalkElvList[7] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                    closest.sort()
                    
                    if len(closest)>=1:
                        if closest[0] == 0.0:
                            try:
                                outputConnections.append((closest2[str(closest[1])][0],closest2[str(closest[1])][1],False))
                            except:
                                outputConnections.append((self.x+20,self.z+20,True))
                        else:
                            outputConnections.append((closest2[str(closest[0])][0],closest2[str(closest[0])][1],False))
                    else:
                        outputConnections.append((self.x+20,self.z+20,True))
                        
                elif directionNum == 4:
                    closest = []
                    for waypoint in waypointClasses:
                        if self.x == waypoint.x:
                            if self.z <= waypoint.z:
                                if dirofway == "I":
                                    if waypoint.direction[0] == True:
                                        closest.append(waypoint.z)
                                elif dirofway == "W":
                                    if waypoint.directionWalk[0] == True:
                                        closest.append(waypoint.z)
                                else:
                                    if waypoint.directionWalkElvList[0] == True:
                                        closest.append(waypoint.z)

                    closest.sort()
                    chosen = False
                    for k in closest:
                        if k != self.z and not chosen:
                            outputConnections.append((self.x,k,False))
                            chosen = True
                    if not chosen:
                        outputConnections.append((self.x,self.z+20,True))
                    
                elif directionNum == 5:
                    #South West
                    #1000 800 = 200
                    #2000 1800 = 200
                    
                    -1 +1
                    closest = []
                    closest2= {}
                    for waypoint in waypointClasses:
                        if self.x-waypoint.x == waypoint.z-self.z:
                            if dirofway == "I":
                                if waypoint.direction[1] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            elif dirofway == "W":
                                if waypoint.directionWalk[1] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            else:
                                if waypoint.directionWalkElvList[1] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            
                    closest.sort()
                    if len(closest)>=1:
                        if closest[0] == 0.0:
                            try:
                                outputConnections.append((closest2[str(closest[1])][0],closest2[str(closest[1])][1],False))
                            except:
                                outputConnections.append((self.x-20,self.z+20,True))
                        else:
                            outputConnections.append((closest2[str(closest[0])][0],closest2[str(closest[0])][1],False))
                    else:
                        outputConnections.append((self.x-20,self.z+20,True))
                    
                elif directionNum == 6:
                    closest = []
                    for waypoint in waypointClasses:
                        if self.z == waypoint.z:
                            if self.x >= waypoint.x:
                                if dirofway == "I":
                                    if waypoint.direction[2] == True:
                                        closest.append(waypoint.x)
                                elif dirofway == "W":
                                    if waypoint.directionWalk[2] == True:
                                        closest.append(waypoint.x)
                                else:
                                    if waypoint.directionWalkElvList[2] == True:
                                        closest.append(waypoint.x)

                    closest.sort()
                    chosen = False
                    for k in closest:
                        if k != self.x and not chosen:
                            outputConnections.append((k,self.z,False))
                            chosen = True
                    if not chosen:
                        outputConnections.append((self.x-20,self.z,True))
                        

                elif directionNum == 7:
                    #North West
                    #-1 -1
                    #1000 800 = 200
                    #2000 1800 = 200
                    closest = []
                    closest2= {}
                    for waypoint in waypointClasses:
                        if self.x-waypoint.x == self.z-waypoint.z:
                            if dirofway == "I":
                                if waypoint.direction[3] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            elif dirofway == "W":
                                if waypoint.directionWalk[3] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                            else:
                                if waypoint.directionWalkElvList[3] == True:
                                    h = math.hypot(abs(waypoint.x-self.x), abs(self.z-waypoint.z))
                                    closest.append(h)
                                    closest2[str(h)] = (waypoint.x,waypoint.z)
                    closest.sort()
                    if len(closest)>=1:
                        if closest[0] == 0.0:
                            try:
                                outputConnections.append((closest2[str(closest[1])][0],closest2[str(closest[1])][1],False))
                            except:
                                outputConnections.append((self.x-20,self.z-20,True))
                        else:
                            outputConnections.append((closest2[str(closest[0])][0],closest2[str(closest[0])][1],False))
                    else:
                        outputConnections.append((self.x-20,self.z-20,True))
        
        return outputConnections
    def drawConnections(self,screen,offset,offsetMinecraft):
        widths = 3
        shrink = 6
        for destination in self.connectedTo:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,0,255),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        for destination in self.connectedToWalk:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,255,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        for destination in self.connectedToWalkElvList:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        return screen
       
                    
                
            
class Portal(Waypoint):
    def __init__(self,x,y,z,direction,directionWalk,directionWalkElvList,Floating,name):
        super().__init__(x,y,z,direction,directionWalk,directionWalkElvList,Floating)
        self.name = name
    def returnName(self):
        return self.name
    def drawConnections(self,screen,offset,offsetMinecraft):
        widths = 3
        shrink = 6
        for destination in self.connectedTo:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,0,255),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        for destination in self.connectedToWalk:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,255,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        for destination in self.connectedToWalkElvList:
            if destination[2]:
                pygame.draw.line(screen,(255,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=int(widths/2))
            else:
                pygame.draw.line(screen,(0,0,0),(offset[0]+(self.x-offsetMinecraft[0])/shrink,offset[1]+(self.z-offsetMinecraft[1])/shrink),(offset[0]+(destination[0]-offsetMinecraft[0])/shrink,offset[1]+(destination[1]-offsetMinecraft[1])/shrink), width=widths)
        pygame.draw.circle(screen, (0,0,0), (offset[0]+(self.x-offsetMinecraft[0])/shrink, offset[1]+(self.z-offsetMinecraft[1])/shrink), widths+10)

        return screen

        
def findJSON(path):
    fileList = [f for f in listdir(path) if isfile(join(path, f))]
    return fileList
def getWaypointData(path):
    fileList = findJSON(path)
    waypointsRaw = []
    for i in fileList:
        with open(path+i) as json_file:
            data = json.load(json_file)
            if "the_nether" in data["dimensions"][0]:
                waypointsRaw.append(data)
    return waypointsRaw
def assignDirection(waypointSpaceList,typeof,directionList):
    if waypointSpaceList[-1] == typeof:
        for directions in waypointSpaceList:
            if directions == "North":
                directionList[0] = True
            elif directions == "NorthEast":
                directionList[1] = True
            elif directions == "East":
                directionList[2] = True
            elif directions == "SouthEast":
                directionList[3] = True
            elif directions == "South":
                directionList[4] = True
            elif directions == "SouthWest":
                directionList[5] = True
            elif directions == "West":
                directionList[6] = True
            elif directions == "NorthWest":
                directionList[7] = True
            elif directions == "All":
                directionList[0] = True
                directionList[2] = True
                directionList[4] = True
                directionList[6] = True
            elif directions == "All8":
                directionList = [True,True,True,True,True,True,True,True]
    return directionList
def mapWaypointsToClass(path):
    waypointsRaw = getWaypointData(path)
    waypointClasses = []
    for waypoint in waypointsRaw:
        typew = True
        directionList = [False,False,False,False,False,False,False,False]
        directionWalkList = [False,False,False,False,False,False,False,False]
        directionWalkElvList = [False,False,False,False,False,False,False,False]
        name = ""
        waypointComList = waypoint["name"].split(",")
        if waypointComList[0].split()[-1] == "I" or waypointComList[0].split()[-1] == "W" or waypointComList[0].split()[-1] == "WU":
            for count,waypointCom in enumerate(waypointComList):
                
                waypointSpaceList = waypointCom.split()
                typew = True
                directionList = assignDirection(waypointSpaceList,"I",directionList)
                directionWalkList = assignDirection(waypointSpaceList,"W",directionWalkList)
                directionWalkElvList = assignDirection(waypointSpaceList,"WU",directionWalkElvList)
                
        else:
            for count,waypointCom in enumerate(waypointComList):
                name = waypointComList[0]
                typew = False
                waypointSpaceList = waypointCom.split()
                directionList = assignDirection(waypointSpaceList,"I",directionList)
                directionWalkList = assignDirection(waypointSpaceList,"W",directionWalkList)
                directionWalkElvList = assignDirection(waypointSpaceList,"WU",directionWalkElvList)
        if typew:
            
            waypointClasses.append(Waypoint(waypoint["x"],waypoint["y"],waypoint["z"],directionList,directionWalkList,directionWalkElvList,False))
            
        else:
            waypointClasses.append(Portal(waypoint["x"],waypoint["y"],waypoint["z"],directionList,directionWalkList,directionWalkElvList,False,name))

    return waypointClasses

def generateGraph(waypointClasses,draw):
    G=nx.Graph()
    G.clear()
    #Remove circles for non portals
    #Colours
    Portals = []
    Waypoints=[]
    Ice = []
    Walk = []
    WalkUp = []
    UnMapped = []
    labels = {}
    labels2 = {}
    maxNodeID = 0
    names = []
    for count, waypoint in enumerate(waypointClasses):
        if waypoint.returnName() != "":
            Portals.append(count)
            labels[count] = waypoint.name
            #print(waypoint.x)
            labels2[count] = ("("+str(waypoint.x)+","+str(waypoint.y)+","+str(waypoint.z)+")/("+str(waypoint.x/8)+","+str(waypoint.y)+","+str(waypoint.z/8)+")")
            if not draw:
                names.append(waypoint.name)
        else:
            Waypoints.append(count)
        
        G.add_node(count,pos=(waypoint.x,waypoint.z*-1))
        waypoint.graphID = count
        maxNodeID+=1

    for waypoint in waypointClasses:
        for direction in waypoint.connectedTo:
            if direction[2]:
                                   
                G.add_node(maxNodeID,pos=(direction[0],direction[1]*-1))
                G.add_edge(waypoint.graphID,maxNodeID,weight=10)
                Waypoints.append(maxNodeID)
                UnMapped.append((waypoint.graphID,maxNodeID))
                maxNodeID+=1
            else:
                for waypoint2 in waypointClasses:
                    for direction2 in waypoint2.connectedTo:
                        if direction[0] == waypoint2.x and direction[1] == waypoint2.z:
                            
                            G.add_edge(waypoint.graphID,waypoint2.graphID, weight=(math.hypot(abs(waypoint.x-waypoint2.x), abs(waypoint.z-waypoint2.z)))/2)
                            #print(waypoint.x,waypoint.z,waypoint2.x,waypoint2.z)
                            Ice.append((waypoint.graphID,waypoint2.graphID))
        for direction in waypoint.connectedToWalk:
            if direction[2]:
                                                            
                G.add_node(maxNodeID,pos=(direction[0],direction[1]*-1))
                G.add_edge(waypoint.graphID,maxNodeID,weight=10)
                Waypoints.append(maxNodeID)
                UnMapped.append((waypoint.graphID,maxNodeID))
                maxNodeID+=1
            else:
                for waypoint2 in waypointClasses:
                    for direction2 in waypoint2.connectedToWalk:
                        if direction[0] == waypoint2.x and direction[1] == waypoint2.z:
                            G.add_edge(waypoint.graphID,waypoint2.graphID, weight=(math.hypot(abs(waypoint.x-waypoint2.x), abs(waypoint.z-waypoint2.z))))   
                            Walk.append((waypoint.graphID,waypoint2.graphID))
        
        for direction in waypoint.connectedToWalkElvList:
            if direction[2]:                                   
                G.add_node(maxNodeID,pos=(direction[0],direction[1]*-1))
                G.add_edge(waypoint.graphID,maxNodeID,weight=10)
                Waypoints.append(maxNodeID)
                UnMapped.append((waypoint.graphID,maxNodeID))
                maxNodeID+=1
            else:
                for waypoint2 in waypointClasses:
                    for direction2 in waypoint2.connectedToWalkElvList:
                        if direction[0] == waypoint2.x and direction[1] == waypoint2.z:
                            G.add_edge(waypoint.graphID,waypoint2.graphID, weight=(math.hypot(abs(waypoint.x-waypoint2.x), abs(waypoint.z-waypoint2.z))))     
                            WalkUp.append((waypoint.graphID,waypoint2.graphID))
        if waypoint.floating:
            distanceTo = []
            for waypoint2 in waypointClasses:
                distanceTo.append([math.hypot(abs(waypoint.x-waypoint2.x), abs(waypoint.z-waypoint2.z)),waypoint2.graphID])
            distanceTo.sort(key=lambda x: x[0])
            if distanceTo[0][1] != waypoint.graphID:
                G.add_edge(waypoint.graphID,distanceTo[0][1], weight=distanceTo[0][0])
            else:
                G.add_edge(waypoint.graphID,distanceTo[1][1], weight=distanceTo[1][0])
                
        
####    print(Ice)
####    print(Walk)
####    print(WalkUp)
##    #pos = nx.drawing.nx_agraph.graphviz_layout(G,'dot', args='-Grankdir=LR')
    pos=nx.get_node_attributes(G,'pos')
    #for i in  Portals:
        #print(i)
    #Portals
    options = {"node_size": 100, "alpha": 0.5}
    nx.draw_networkx_nodes(G, pos, nodelist=Portals, node_color="tab:purple", **options)
    #Waypoints
    options = {"node_size": 0, "alpha": 0}
    nx.draw_networkx_nodes(G, pos, nodelist=Waypoints, node_color="tab:red", **options)
    
    
    #Edges Ice
    
    nx.draw_networkx_edges(G, pos, edgelist=Ice,width=2.0, alpha=1,edge_color="tab:blue")
    #Edges Walk
    nx.draw_networkx_edges(G, pos, edgelist=Walk,width=2.0, alpha=1,edge_color="tab:green")
    
    #Edges Walk up

    nx.draw_networkx_edges(G, pos, edgelist=WalkUp, width=2.0, alpha=1)
    #Edge Unmapped
    nx.draw_networkx_edges(G, pos, edgelist=UnMapped,width=2.0, alpha=1,edge_color="tab:red")
    
    if draw:
        nx.draw_networkx_labels(G, pos, labels2, font_size=6, font_color="black", verticalalignment="top" )
        nx.draw_networkx_labels(G, pos, labels,font_weight="bold", font_size=8, font_color="black", verticalalignment="bottom" )
    #plt.tight_layout()
    #nx.draw(G, pos)
    #plt.show()
    if draw:
        XList = []
        ZList = []
        for i in waypointClasses:
            XList.append(i.x)
            ZList.append(i.z)
        
        XList.sort()
        ZList.sort()
        LowestX = XList[0]-5000
        HighestX = XList[-1]-2000
        LowestZ = ZList[0]-7000
        HighestZ = ZList[-1]-5000
        ListofNames=[]
        for XCount,i in enumerate(range(LowestX,HighestX,2000)):
            for ZCount,j in enumerate(range(LowestZ,HighestZ,2000)):
                #plt.plot(range(1000))
                plt.xlim(i,i+2000)
                plt.ylim(j,j+2000)
                plt.axis('off')
                plt.gca().spines['left'].set_visible(False)
                plt.gca().set_aspect('equal', adjustable='box')
                ListofNames.append("test"+str(XCount)+","+str(ZCount)+".png")
                plt.savefig("test"+str(XCount)+","+str(ZCount)+".png",dpi=200, bbox_inches='tight',pad_inches=0)

        CurrentRow = 0
        a = len(range(HighestZ,LowestZ,-2000))-1
        b = len(range(HighestX,LowestX,-2000))-1
        blank_image = Image.new('RGB', (b*739, a*739), color = 'white')
        blank_image.save("MainMap.jpg")
        blank_image = Image.open("MainMap.jpg")

        for ZCount,j in enumerate(range(HighestZ,LowestZ,-2000)):
            for XCount,i in enumerate(range(HighestX,LowestX,-2000)):          
                image64 = Image.open("test"+str(XCount)+","+str(a-ZCount)+".png")
                blank_image.paste(image64, (XCount*739,ZCount*739))
        blank_image.save("MainMap.jpg")
        for i in ListofNames:
            os.remove(i)
        blank_image.save("MainMap.jpg")
        blank_image = Image.open("MainMap.jpg")
        key = Image.open("NetherKey.png")
        b -=1
        blank_image.paste(key, (b*739,0))
        blank_image.save("MainMap.jpg")
        
    return G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,names

def drawGraphRouted(G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,StartID,EndID,name,waypointClasses,count=1):
    ListHighLighted = []
    ListHighLighted = nx.dijkstra_path(G, StartID, EndID)
    if len(ListHighLighted) > 1:
        pos=nx.get_node_attributes(G,'pos')
        #Portals
        options = {"node_size": 500, "alpha": 1}
        nx.draw_networkx_nodes(G, pos, nodelist=Portals, node_color="tab:purple", **options)
        
        options = {"node_size": 500, "alpha": 1}
        nx.draw_networkx_nodes(G, pos, nodelist=[ListHighLighted[0],ListHighLighted[-1]], node_color="#FFD700", **options)
        
        #ListHighLighted.pop(-1)
        #Waypoints
        options = {"node_size": 0, "alpha": 0}
        nx.draw_networkx_nodes(G, pos, nodelist=Waypoints, node_color="tab:red", **options)
        
        #Edges Ice
        nx.draw_networkx_edges(G, pos, edgelist=Ice,width=2.0, alpha=1,edge_color="tab:blue")
        #Edges Walk
        nx.draw_networkx_edges(G, pos, edgelist=Walk,width=2.0, alpha=1,edge_color="tab:green")
        
        #Edges Walk up
        
        nx.draw_networkx_edges(G, pos, edgelist=WalkUp, width=2.0, alpha=1)
        #Edge Unmapped
        nx.draw_networkx_edges(G, pos, edgelist=UnMapped,width=2.0, alpha=1,edge_color="tab:red")
        #gold
        for i in range(0,len(ListHighLighted)):
            try:
                nx.draw_networkx_edges(G, pos, edgelist=[(ListHighLighted[i],ListHighLighted[i+1])],width=2.0, alpha=0.7,edge_color="#FFD700")
            except:
                pass
        #plt.tight_layout()
        testl = {}
        for i in labels:
            if i == StartID or i == EndID:
                testl[i] = labels[i]
        testll = {}
        for i in labels2:
            if i == StartID or i == EndID:
                testll[i] = labels2[i]
        nx.draw_networkx_labels(G, pos, testll, font_size=10, font_color="black", verticalalignment="top" )
        nx.draw_networkx_labels(G, pos, testl,font_weight="bold", font_size=10, font_color="black", verticalalignment="bottom" )
        XList = []
        ZList = []
        for i in waypointClasses:
            if i.graphID in ListHighLighted:
                XList.append(i.x)
                ZList.append(i.z*-1)
        
        XList.sort()
        ZList.sort()
        LowestX = XList[0]-1000
        HighestX = XList[-1]+1000
        LowestZ = ZList[0]-1000
        HighestZ = ZList[-1]+1000

        ListofNames=[]
        for XCount,i in enumerate(range(LowestX,HighestX,2000)):
            for ZCount,j in enumerate(range(LowestZ,HighestZ,2000)):
                #plt.plot(range(1000))
                plt.xlim(i,i+2000)
                plt.ylim(j,j+2000)
                plt.axis('off')
                plt.gca().spines['left'].set_visible(False)
                plt.gca().set_aspect('equal', adjustable='box')
                ListofNames.append("test"+str(XCount)+","+str(ZCount)+".png")
                plt.savefig("test"+str(XCount)+","+str(ZCount)+".png",dpi=200, bbox_inches='tight',pad_inches=0)

        CurrentRow = 0
        diffX = HighestX-LowestX
        diffZ = HighestZ-LowestZ
        a = len(range(HighestZ,LowestZ,-2000))-1
        b = len(range(HighestX,LowestX,-2000))-1
        blank_image = Image.new('RGB', (b*739+700, a*739+700), color = 'white')
        blank_image.save(name+'.jpg')
        blank_image = Image.open(name+'.jpg')
        for ZCount,j in enumerate(range(HighestZ,LowestZ,-2000)):
            for XCount,i in enumerate(range(HighestX,LowestX,-2000)):          
                image64 = Image.open("test"+str(XCount)+","+str(a-ZCount)+".png")
                blank_image.paste(image64, (XCount*739,ZCount*739))
        G.clear()
        plt.figure().clear()
        blank_image.save(name+'.jpg')
        #blank_image = Image.open(name+'.jpg')
        #key = Image.open("NetherKey.png")
        #b -=1
        #blank_image.paste(key, (b*739,0))
        #blank_image.save(name+'.jpg')
        for i in ListofNames:
            os.remove(i)
        
    
def UpdateExport(waypointClasses):
    file = open("MapStorage.txt","r")
    dictionary = []
    for i in file.readlines():
        dictionary.append(i)
    dictionary2 =[]
    file.close()
    for waypoint in waypointClasses:
        dictionary2.append(str(waypoint.returnName())+";"+str(waypoint.x)+";"+str(waypoint.y)+";"+str(waypoint.z)+";"+str(waypoint.direction)+";"+str(waypoint.directionWalk)+";"+str(waypoint.directionWalkElvList)+"\n")
    dictionary3 = list(((set(dictionary)).union(set(dictionary2))))
    file = open("MapStorage.txt","w")
    for i in dictionary3:
        file.write(i)
    file.close()

def createWaypointClassList():
    waypointClasses=[]
    path = "/home/opc/PersonalProjects/Mapping/waypoints/"
    waypointClasses = mapWaypointsToClass(path)
    offsetMinecraft = (0,0)
    for i in waypointClasses:
        i.calculateConnected(waypointClasses)
        if i.returnName() == HomeName:
            offsetMinecraft = (i.x,i.z)
    return waypointClasses
def drawRoutedMap(X,Y):
    waypointClasses = createWaypointClassList()
    draw = False
    done = False
    StartID = 0
    EndID = 0
    G = ""
    G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,names = generateGraph(waypointClasses,draw)
    for waypoint in waypointClasses:
        if not done:
            if waypoint.returnName() == X:
                StartID = waypoint.graphID
            elif waypoint.returnName() == Y:
                EndID = waypoint.graphID
            if StartID != 0 and EndID !=0:
                done = True
                try:
                    drawGraphRouted(G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,StartID,EndID,X+"_"+Y,waypointClasses)
                    return "1"
                except:
                    return "6"
    if StartID ==0 and EndID == 0:
        return "2"
    elif StartID == 0:
        return "3"
    elif EndID == 0:
        return "4"
    else:
        return "5"
def drawXZ(X,Y,T):
    XCoord = False
    YCoord = False
    if type(X) == list:
        X[0] = int(X[0])
        X[1] = int(X[1])
        XCoord = True
        if T == "N":
            X[0] *= 8
            X[1] *= 8
    if type(Y) == list:
        Y[0] = int(Y[0])
        Y[1] = int(Y[1])
        YCoord = True
        if T == "N":
            Y[0] *= 8
            Y[1] *= 8
    directionList = [False,False,False,False,False,False,False,False]
    directionWalkList = [False,False,False,False,False,False,False,False]
    directionWalkElvList = [False,False,False,False,False,False,False,False]
    waypointClasses = createWaypointClassList()
    if XCoord:
        waypointClasses.append(Portal(int(X[0]),75,int(X[1]),directionList,directionWalkList,directionWalkElvList,True,"To"))
        waypointClasses[-1].calculateConnected(waypointClasses)
    if YCoord:
        waypointClasses.append(Portal(int(Y[0]),75,int(Y[1]),directionList,directionWalkList,directionWalkElvList,True,"From"))
        waypointClasses[-1].calculateConnected(waypointClasses)
    draw = False
    done = False
    G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,names = generateGraph(waypointClasses,draw)
    for waypoint in waypointClasses:
        if not done:
            if waypoint.returnName() == X:
                StartID = waypoint.graphID
    if XCoord:
        Xname = "To"
    else:
        Xname = X
    if YCoord:
        Yname = "From"
    else:
        Yname = Y
    StartID = 0
    EndID = 0
    for waypoint in waypointClasses:
        if not done:
            if waypoint.returnName() == Xname:
                StartID = waypoint.graphID
            elif waypoint.returnName() == Yname:
                EndID = waypoint.graphID
            if StartID != 0 and EndID !=0:
                done = True
                try:
                    drawGraphRouted(G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,StartID,EndID,Xname+"_"+Yname,waypointClasses)
                    return Xname+"_"+Yname
                except:
                    return "6"
    if StartID ==0 and EndID == 0:
        return "2"
    elif StartID == 0:
        return "3"
    elif EndID == 0:
        return "4"
    else:
        return "5"


TOKEN = 
GUILD="The Mapping Server"
client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True)
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command(name='searchportal',help='Search for a portal name: !searchportal X')
async def portals(ctx,X):

    waypointClasses=[]
    path = "/home/opc/PersonalProjects/Mapping/waypoints/"
    waypointClasses = mapWaypointsToClass(path)
    offsetMinecraft = (0,0)
    for i in waypointClasses:
        i.calculateConnected(waypointClasses)
        if i.returnName() == HomeName:
            offsetMinecraft = (i.x,i.z)
    draw = False
    done = False
    StartID = 0
    EndID = 0
    G = ""
    G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,names = generateGraph(waypointClasses,draw)
    await ctx.send(difflib.get_close_matches(X, names))
    
@bot.command(name='route',help='Enter !route X Y with X and Y being locations. If you want to use coords for either please enter either N for nether or O for overworld dependant on the type of coords after eg: !route (100,100) (200,200) O',pass_context=True) 
async def route(ctx,X,Y,T="N"):
    X = X.title()
    Y = Y.title()
    drawn = ""
    role = discord.utils.get(ctx.guild.roles, name="Paid")
    role2 = discord.utils.get(ctx.guild.roles, name="Yaszumatti")
    if ctx.channel.id != 917148059882909767 and  ctx.channel.id != 916040242954375179:
        await ctx.send("Wrong channel!")
        return
    if role not in ctx.author.roles and role2 not in ctx.author.roles:
        await ctx.send("You do not have the correct role to access this bot!")
        return
    create = False
    if "," in X:
        X = X.strip(")")
        X = X.strip("(")
        X = X.split(",")
        create = True
    if "," in Y:
        Y = Y.strip(")")
        Y = Y.strip("(")
        Y = Y.split(",")
        create = True
    if create:
        drawn = drawXZ(X,Y,T)
        try:
            await ctx.send(file=discord.File(drawn+'.jpg'))
            drawn = "7"
        except:
            drawn = "5"
    else:
        await ctx.send("Creating the route, give it 10 secs") 
        drawn = drawRoutedMap(X,Y)
    if drawn == "1":
        await ctx.send(file=discord.File(X+"_"+Y+'.jpg'))
    elif drawn == "2":
        await ctx.send('Both Portals entered could not be found, try using !searchportal NAME first (use " around portal names with spaces)')
    elif drawn == "3":
        await ctx.send(str(X)+': Could not be found, try using !searchportal NAME first (use " around portal names with spaces)')
    elif drawn == "4":
        await ctx.send(str(Y)+': Could not be found, try using !searchportal NAME first (use " around portal names with spaces)')
    elif drawn == "5":
        await ctx.send("Something went wrong with the map, basically I messed up. Xander2508#8106")
    elif drawn == "7":
        return
    else:
        await ctx.send("Unknown error, contact Xander2508#8106")
    


    
if __name__ == "__main__":

    #Roll out to that other server
    #XY gps + Closest waypoint
    #Get rathnir up - message that discord guy with skull kind of profile
    #Search by nations
    
    #scp C:\Users\alexa\OneDrive\Desktop\Mapping\M.py opc@132.226.208.50:/home/opc/PersonalProject

    
    
    HomeName = "Rannikko"
    #waypointClasses=[]

    
    #path = "C:/Users/alexa/AppData/Roaming/.minecraft/journeymap/data/mp/Minecraft~Server/waypoints/"
    #waypointClasses = mapWaypointsToClass(path)
        
    #offsetMinecraft = (0,0)
    #for i in waypointClasses:
    #    i.calculateConnected(waypointClasses)
    #    if i.returnName() == HomeName:
    #        offsetMinecraft = (i.x,i.z)

##    waypointClasses=[]
##    path = "C:/Users/alexa/AppData/Roaming/.minecraft/journeymap/data/mp/Minecraft~Server/waypoints/"
##    waypointClasses = mapWaypointsToClass(path)
##    offsetMinecraft = (0,0)
##    for i in waypointClasses:
##        i.calculateConnected(waypointClasses)
##        if i.returnName() == HomeName:
##            offsetMinecraft = (i.x,i.z)
##    draw = False
##    done = False
##    StartID = 0
##    EndID = 0
##    G = ""
##    draw = True
##    G,Ice,Walk,WalkUp,UnMapped,Portals,Waypoints,labels,labels2,names = generateGraph(waypointClasses,draw)
    bot.run(TOKEN)
    
    #UpdateExport(waypointClasses)
    
























    
