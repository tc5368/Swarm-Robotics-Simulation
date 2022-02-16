from model import *
from agent import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def robot_cell_Apperance(agent):
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
	else:
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


	return portrayal

#Default values that controll the visulisation
RobotCount = 5
GridCellHeight = 10; GridCellWidth = 10;
GridSizeHeight = 500; GridSizeWidth = 500;

#Generates the canvas, parameters of how many cells in x and y diretion then pixel size of grid.
grid = CanvasGrid(robot_cell_Apperance, GridCellHeight, GridCellWidth, GridSizeHeight, GridSizeWidth)

#Startes the visuliation using the given model, sets the page title and the model starting settings.
server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",{"robotCount":RobotCount, "height":GridCellHeight, "width":GridCellWidth})

#Launch the server
server.port = 8521 # The default
server.launch()