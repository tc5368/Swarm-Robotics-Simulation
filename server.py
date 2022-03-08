from model import *
from agent import *
from binAgent import *
from dropOffAgent import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def Apperance(agent):
	#Changes the robots colour based on the task it is undertaking
	if agent.type == "Robot":
		if agent.holding == []:
			robotImage = 'resources/Robot.png'
		else:
			robotImage = 'resources/Robot Busy.png'

		robotColor = "Red"
		if DevMode:
			robotImage = 'rect'
		if agent.holding == []:
			robotColor = "Blue"
		if agent.unique_id == 0:
			robotColor = "Orange"

		name = agent.unique_id

		portrayal = {"Shape": robotImage,
					 "Filled": "true",
					 "Color": robotColor,
					 "Layer": 'WarehouseFloor',
					 "Number":agent.unique_id,
					 "Carrying": agent.holding,
					 "w": 0.6,
					 "h": 0.6}

	elif agent.type == "Bin":
		name = agent.unique_id
		formattedItem = str(agent.contains[0]).replace(' ','').replace('/','').replace('(','').replace(')','').replace('-','')
		bin_image = "resources/"+formattedItem+".png"

		if DevMode:
			bin_image = 'rect'

		binColour = "grey"
		if agent.bookings != {}:
			binColour = "green"

		portrayal = {"Shape": bin_image,
					 "Filled": "true",
					 "Layer": 'WarehouseFloor',
					 "Reference":agent.unique_id,
					 "Contains": agent.contains,
					 "Stock": agent.stock,
					 "Bookings": str(agent.bookings),
					 "Color": binColour,
					 "w":0.1,
					 "h":0.1,
					 "scale": 0.5}

	# elif agent.type == "Start":

	# 	portrayal = {"Shape": "rect",
	# 				 "Filled": "true",
	# 				 "Layer": 'WarehouseFloor',
	# 				 "Name": "Starting Point",
	# 				 "Color": 'green',
	# 				 "w": 1,
	# 				 "h": 1}

	elif agent.type == "DropOff":

		if agent.checkComplete():
			dropOffColour = "Green"
		else:
			dropOffColour = agent.getPercentageDone()

		#this.drawRectangle in the mesa library only draws diagonaly gradients, can try and turn to use only horizontal
		#need to just change line 159 so it uses y1 = 0 not y1=y0+cellHeight

		portrayal = {"Shape": "rect",
					 "Filled": "true",
					 "Layer": 'WarehouseFloor',
					 "Reference": agent.unique_id,
					 "Order": str(agent.order),
					 "Contains": str(agent.contains),
					 "Color": dropOffColour,
					 "w": 1,
					 "h": 1}

	return portrayal


# DevMode - just changes visulisations.
DevMode = True
# DevMode = False

#Grid size cannot be changed while running.
GridSize = 20
GridSizeHeight = 1000; GridSizeWidth = 1000;

pathFindingType = "Path Finding"
# pathFindingType = "Blind Goal"


# Default values that control the visulisation can eventully be changed to sliders
model_params = {
	"robotCount" : 150,
	"gridSize" : GridSize,
	"UniqueItems" : 3,
	"MaxStockPerOrder" : 2,
	"pathFindingType":pathFindingType
}


# Added slides to be used but also for development will continue using default settings
# model_params = {
#     "robotCount": UserSettableParameter("slider", "Robot Initial Count", 1, 1, 50),
#     "gridSize": GridSize,
#     "UniqueItems": UserSettableParameter("slider", "Unique Items Per Order", 5, 1, 10),
#     "MaxStockPerOrder": UserSettableParameter("slider", "Maximum of a stock per order", 3, 1, 10)
# }


#Confirms that the robot placing wont get stuck in an infite loop trying to fit robots.
# if model_params["robotCount"].value >= (model_params["gridSize"].value * (model_params["gridSize"].value-1)):
# 	print('Invalid Setup too many robots for the grid')
# 	exit()


#Generates the canvas, parameters of how many cells in x and y diretion then pixel size of grid.
grid = CanvasGrid(Apperance, model_params["gridSize"], model_params["gridSize"], GridSizeHeight, GridSizeWidth)

#Startes the visuliation using the given model, sets the page title and the model starting settings.
#
#server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",{"robotCount":RobotCount, "height":GridCellHeight, "width":GridCellWidth, "UniqueItems":UniqueItemsPerOrder,"MaxStockPerOrder":MaxStockPerOrder})
server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",model_params)

#Launch the server
server.port = 8521 # The default
server.launch()



















