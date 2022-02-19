from model import *
from agent import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def Apperance(agent):
	#Changes the robots colour based on the task it is undertaking
	if agent.type == "Robot":
		if agent.current_job == 'Collecting':
			robotColour = 'blue'
		else:
			robotColour = 'red'

		name = agent.unique_id

		portrayal = {"Shape": "rect",
					 "Filled": "true",
					 "Layer": 'WarehouseFloor',
					 "Number":agent.unique_id,
					 "Job": agent.current_job,
					 "Carrying": agent.holding,
					 "text_color": "white",
					 "Color": robotColour,
					 "w": 0.5,
					 "h": 0.5}

	elif agent.type == "Bin":
		name = agent.unique_id

		portrayal = {"Shape": "rect",
					 "Filled": "true",
					 "Layer": 'WarehouseFloor',
					 "Reference":agent.unique_id,
					 "Contains": agent.contains,
					 "Stock": agent.stock,
					 "Color": 'grey',
					 "w": 0.1,
					 "h": 0.1}

	# elif agent.type == "Start":

	# 	portrayal = {"Shape": "rect",
	# 				 "Filled": "true",
	# 				 "Layer": 'WarehouseFloor',
	# 				 "Name": "Starting Point",
	# 				 "Color": 'green',
	# 				 "w": 1,
	# 				 "h": 1}

	elif agent.type == "DropOff":

		portrayal = {"Shape": "rect",
					 "Filled": "true",
					 "Layer": 'WarehouseFloor',
					 "Reference": agent.unique_id,
					 "Order": str(agent.order),
					 "Contains": str(agent.contains),
					 "Color": agent.checkComplete(),
					 "w": 1,
					 "h": 1}

	return portrayal

#Default values that control the visulisation can eventully be changed to sliders
RobotCount = 1
UniqueItemsPerOrder = 3
MaxStockPerOrder = 3

GridCellHeight = 5; GridCellWidth = 5;
GridSizeHeight = 500; GridSizeWidth = 500;

#Confirms that the robot placing wont get stuck in an infite loop trying to fit robots.
if RobotCount >= GridCellHeight * (GridCellWidth-1):
	print('Invalid Setup too many robots for the grid')
	exit()

#Generates the canvas, parameters of how many cells in x and y diretion then pixel size of grid.
grid = CanvasGrid(Apperance, GridCellHeight, GridCellWidth, GridSizeHeight, GridSizeWidth)

#Startes the visuliation using the given model, sets the page title and the model starting settings.
server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",{"robotCount":RobotCount, "height":GridCellHeight, "width":GridCellWidth, "UniqueItems":UniqueItemsPerOrder,"MaxStockPerOrder":MaxStockPerOrder})

#Launch the server
server.port = 8521 # The default
server.launch()