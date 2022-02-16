from model import *
from agent import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def robotApperance(agent):
	#Changes the robots colour based on the task it is undertaking
	if agent.current_job == 'Collecting':
		robotColour = 'blue'
	else:
		robotColour = 'red'

	name = agent.unique_id

	portrayal = {"Shape": "rect",
				 "Filled": "true",
				 "Layer": 'Robot',
				 "Color": robotColour,
				 "w": 0.5,
				 "h": 0.5}

	return portrayal

#Default values that controll the visulisation
RobotCount = 5
GridCellHeight = 100; GridCellWidth = 100;
GridSizeHeight = 500; GridSizeWidth = 500;

#Generates the canvas, parameters of how many cells in x and y diretion then pixel size of grid.
grid = CanvasGrid(robotApperance, GridCellHeight, GridCellWidth, GridSizeHeight, GridSizeWidth)

#Startes the visuliation using the given model, sets the page title and the model starting settings.
server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",{"robotCount":RobotCount, "height":GridCellHeight, "width":GridCellWidth})

#Launch the server
server.port = 8521 # The default
server.launch()