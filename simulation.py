#!/usr/bin/python -u

import math,random,copy,os,sys
import visual

MAX_PHEROMONE=15
PHEROMONE_INCREMENT=2
PHEROMONE_DECAY=0.9
INITIAL_ANGLE=0.0*math.pi/180
pathLen=100
maxWind=5
iterations=10
wind=[]
pheromone=[]
maxPower=40
population=100
g=9.81
c=0.5
sScale=0.05
forceToAngle=0.1

''' generates an array of new Wind values or reads existing ones from path.dat '''
def genWind():
	if os.path.isfile("path.dat"):
		f=open("path.dat","r")
		for line in f:
			wind.append(float(line))
		f.close()
	else:
		print "Creating new path"
		f=open("path.dat","w")
		for i in range(pathLen):
			windVal=maxWind*random.random()-0.5*maxWind
			wind.append(windVal)
			f.write(str(windVal)+'\n')
		f.close()

''' Initialises pheromone array to 1's '''
def resetPheromone():
	return [[1 for i in range(maxPower)] for j in range(pathLen)]

''' Calculates a scaled force value with sign '''
def getRealForce(value):
	if value < 0.5*maxPower:
		return -1.0*sScale*value
	else: 
		return sScale*value
	
''' Objective function '''
def objective(angleArray):
	if len(angleArray) == 0:
		return 1
	sum=0
	for angle in angleArray:
		sum = sum + angle
	avg = sum/len(angleArray)
	var = 0
	for angle in angleArray:
		var = var + (angle-avg)**2
	if var == 0:
		return 1
	#return var # for using variance as objective function
	return 1/abs(avg)
	

class Ant:
	cAngle=[INITIAL_ANGLE]
	selectedForces=[0]
	c=1
	v=1
	strength=0
	
	def __init__(self):
		self.cAngle=[INITIAL_ANGLE]
		self.selectedForces=[0]
		
	def reset(self):
		self.cAngle=[INITIAL_ANGLE]
		self.selectedForces=[0]
		
	def nextAngle(self,Feff):
		cAngle=self.cAngle
		cAngle.append(cAngle[-1]+Feff)
		
	def nextStep(self,strength,wind,v=1):
		self.selectedForces.append(strength)
		cAngle=self.cAngle
		lastAngle = cAngle[-1]
		force = getRealForce(strength)
		Feff = forceToAngle*(wind-g*math.sin(lastAngle)+force)/v
		#print "Wind: "+str(wind)+"Force: "+str(sScale*strength)+" Result: "+str(Feff)
		self.nextAngle(Feff)
		return self.cAngle[len(cAngle)-1]
	
''' Picks the best ant in the current iteration '''
def getBestAnt():
	max = 0;
	bestAnt = 0;
	for i in range(len(ants)):
			#print ants[i].cAngle
			#print "Ant: "+str(i)+" objective value: "+str(objective(ants[i].cAngle))
			if max < objective(ants[i].cAngle):
				max = objective(ants[i].cAngle)
				bestAnt = ants[i];
	return bestAnt

''' Draws a random force value taking the pheromone into account '''
def getForceValue(step):
	
	den=0.0
	for i in range(maxPower):
		den = den + pheromone[step][i]
	#we are building a cumulative density function here
	roulette=[]
	roulette=maxPower*[0.0]
	roulette[0]=pheromone[step][0]/den
	#print "Divider "+str(den)
	for i in range(1,maxPower):
		roulette[i] = roulette[i-1]+pheromone[step][i]/den
		#print "Probability value for force "+str(i)+" "+str(pheromone[step][i]/den)
	seed=random.random()
	for i in range(maxPower):		
		if (seed <= roulette[i]):
				return i

''' Averaged result for the whole ant population '''
def averageResult(i):
	objSum=0
	f=open("avg.dat","a")
	for ant in ants:
		objSum = objSum + objective(ant.cAngle)
	f.write("%d %f\n"%(i,objSum/len(ants)))
	f.close()
		

''' Display 2d arrays such as pheromone '''	
def nicePrint(array):
	for row in array:
		print row

ants=[Ant() for i in range(population)]
genWind()
pheromone=resetPheromone()
bestPath=[]
globalBestAnt=Ant()
bestForces=[]
firstResult=0

#main program
if __name__ == '__main__':
	try:
		os.remove("rower.dat")
		os.remove("avg.dat")
		os.remove("bestPath.dat")
	except OSError:
		pass
	#algorithm iterations
	for it in range(iterations):
		print "Iteration "+str(it)
		#iterating over ants
		for i in range(pathLen):
			antNo=0
			for ant in ants:
				fVal=getForceValue(i)
				#print "Ant "+str(antNo)+" Feff "+str(fVal)
				angle=ant.nextStep(fVal,wind[i])
				antNo=antNo+1
				#selectedForces[i][fVal] = selectedForces[i][fVal] + 1
				#print "Step "+str(i)+" Ant "+str(antNo)+" deflection "+str(angle)
		
		bAnt = getBestAnt()
		averageResult(it)
		forces = bAnt.selectedForces
		bestPath=copy.copy(bAnt.cAngle)
		if objective(bAnt.cAngle) > objective(globalBestAnt.cAngle):
			globalBestAnt = copy.deepcopy(bAnt)
		for i in range(pathLen):
			pheromone[i][forces[i]] = int(pheromone[i][forces[i]]*PHEROMONE_DECAY)
			if pheromone[i][forces[i]] < MAX_PHEROMONE:
				pheromone[i][forces[i]] = pheromone[i][forces[i]] + PHEROMONE_INCREMENT
		
		#nicePrint(pheromone)
		#print "Best ant position "+str(180*bAnt.cAngle[-1]/math.pi)
		avga=180*(1/objective(bAnt.cAngle))/math.pi
		if it == 0:
			firstResult=objective(bAnt.cAngle)
		print "Best ant average angle "+str(avga)+" improvement = "+str(firstResult/avga)
		#append the improvement to a logfile
		f=open("rower.dat","a")
		f.write(str(it)+" "+str(objective(globalBestAnt.cAngle)/firstResult)+'\n')
		f.close()

		avg = 0
		for i in range(len(ants)):
			#print ants[i].cAngle
			#print "Ant: "+str(i)+" objective: "+str(objective(ants[i].cAngle))
			#avg = objective(ants[i].cAngle)+  avg
			ants[i].reset()
			

	#visualise the best control values using pygame
	visual.visualise(bestPath)

	#write the best control values and corresponding wind values for plotting
	f=open("bestPath.dat","w")
	for i in range(pathLen):
		# write every 4th value - improves readability
		if i % 4 == 0:
			f.write("%d %f %f %f\n"%(i,wind[i],getRealForce(globalBestAnt.selectedForces[i]),180.0*globalBestAnt.cAngle[i]/math.pi))
	f.close()
