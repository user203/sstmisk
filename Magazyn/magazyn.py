from Source import *
from Source import vrep
from Source import vrepConst

def getPalettePosition(paletteName):
	errorCode, handle = vrep.simxGetObjectHandle(clientID, paletteName, vrepConst.simx_opmode_oneshot_wait)
	errorCode, Position = vrep.simxGetObjectPosition(clientID, handle, -1, vrepConst.simx_opmode_oneshot_wait)
	P = Point(Position[0], Position[1])
	return P

def getPalettePositionsList(PaletteNames):
	palettePlaces = []
	for i in PaletteNames:
		palettePlaces.append(getPalettePosition(PaletteNames[i]))
		return palettePlaces

# create paths
d = Dimentions(4, 5, 1, 16)
print(d.getDimX())
b = BlockOfPaletts(Point(1,1), Point(14,1), Point(14,6), Point(1,6), d)
print(b.getDimX())
p = CreatePaths()
p.addBlock(b)
p.createPathsAroundBlocks()

# start symulation
port = 19999
vrep.simxFinish(-1) # just in case, close all opened connections
global clientID
clientID = vrep.simxStart('127.0.0.1',port,True,True,5000,5) # Connect to V-REP
if clientID == -1:
	print('Failed connecting to remote API server')
	exit()

robot = MoveRobot("Pioneer_p3dx_0", clientID)

robot.setSpeed(12)
robot.goToDestinationPoint(Point(23,55))
robot.rotate(90)
robot.goToDestinationPoint(Point(23,55))

moveRobotinStorehouse = MoveRobotsInStorehouse()
moveRobotinStorehouse.setSpeed(Robots.Robot1, 12)

storehouse = Storehouse(places, palletNames, stations, dockStations, stationBuffors, paths)
print(storehouse.getPalletePosition(0).getX(), storehouse.getPalletePosition(0).getY())
print(storehouse.getStationPosition(Stations.A).getX(), storehouse.getStationPosition(Stations.A).getY())

vrep.simxFinish(clientID)
print('Program ended')
