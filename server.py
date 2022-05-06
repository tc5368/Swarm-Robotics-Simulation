from model import *
from agent import *
from binAgent import *
from dropOffAgent import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def Apperance(agent):
	# Changes the robots colour based on the task it is undertaking
	if agent.type == "Robot":
		if agent.holding == []:
			robotImage = 'resources/Robot.png'
		else:
			robotImage = 'resources/Robot Busy.png'

		robotColor = "Red"
		robotLayer = 'Interaction'

		if not model_params["displayMode"].value:
			robotImage = 'rect'
			robotLayer = 'WarehouseFloor'

		if agent.holding == []:
			robotColor = "Blue"

		# if True:
		if model_params["devMode"].value:
			if agent.unique_id in [0, 1]:
				robotColor = "Orange"

		portrayal = {"Shape": robotImage,
					"Filled": "true",
					"Color": robotColor,
					"Layer": robotLayer,
					"Number": agent.unique_id,
					"Carrying": agent.holding,
					"w": 0.6,
					"h": 0.6}

	elif agent.type == "Bin":

		if model_params["displayMode"].value:
			formattedItem = str(agent.contains[0]).replace(' ', '').replace('/', '').replace('(', '').replace(')', '').replace('-', '')
			bin_image = "resources/" + formattedItem + ".png"
		else:
			bin_image = 'rect'

		binColour = "grey"

		portrayal = {"Shape": bin_image,
					"Filled": "true",
					"Layer": 'WarehouseFloor',
					"Reference": agent.unique_id,
					"Contains": agent.contains,
					# "Stock": agent.stock,
					"Bookings": str(agent.bookings),
					"Color": binColour,
					"w": 1,
					"h": 1,
					"scale": 0.75}

	elif agent.type == "Floor":

		portrayal = {"Shape": 'rect',
					"Filled": "true",
					"Layer": 'WarehouseFloor',
					"Color": 'grey',
					"w": 1,
					"h": 1,
					"scale": 1}

	elif agent.type == "Label":

		formattedItem = str(agent.item).replace(' ', '').replace('/', '').replace('(', '').replace(')', '').replace('-', '')
		label_image = "resources/" + formattedItem + ".png"

		portrayal = {"Shape": label_image,
					"Filled": "true",
					"Layer": 'WarehouseFloor',
					"Name": agent.unique_id,
					"Color": 'White',
					"text": agent.count,
					"w": 1,
					"h": 1,
					"scale": 0.75}

	elif agent.type == "DropOff":

		if agent.checkComplete():
			dropOffColour = "Green"
		else:
			dropOffColour = agent.getPercentageDone()

		if not model_params["displayMode"].value:
			dropOffLayer = 'WarehouseFloor'
		else:
			dropOffLayer = 'Interaction'

		# this.drawRectangle in the mesa library only draws diagonaly gradients, can try and turn to use only horizontal
		# need to just change line 159 so it uses y1 = 0 not y1=y0+cellHeight

		portrayal = {"Shape": "rect",
			"Filled": "true",
					"Layer": dropOffLayer,
					"Reference": agent.unique_id,
					"Order": str(agent.order),
					"Contains": str(agent.contains),
					"Color": dropOffColour,
					"w": 1,
					"h": 1}

	return portrayal


# Grid size and charts cannot be changed while running.
GridSize = 8
enableCharts = True
# enableCharts = False

# # Added slides to be used but also for development will continue using default settings
model_params = {
	"robotCount": UserSettableParameter("slider", "Robot Initial Count", (round((GridSize ** 2 - GridSize) * 0.15) // 3) + 1, 1, (GridSize ** 2 - GridSize) // 3),
	"gridSize": GridSize,
	"UniqueItems": UserSettableParameter("slider", "Unique Items Per Order", 10, 1, 10),
	"MaxStockPerOrder": UserSettableParameter("slider", "Maximum of a stock per order", 1, 1, 20),
	"devMode": UserSettableParameter('checkbox', 'Example Mode', value=False),
	"displayMode": UserSettableParameter('checkbox', 'Display Mode', value=True),
	"pathFindingType": UserSettableParameter('choice', 'Pathfinding Type', value='Path Finding', choices=['Path Finding', 'Blind Goal'])
}

CellSize = 750 / GridSize
GridSizeHeight = CellSize * GridSize
GridSizeWidth = CellSize * (GridSize + model_params["UniqueItems"].value)
grid = CanvasGrid(Apperance, model_params["gridSize"] + model_params["UniqueItems"].value, model_params["gridSize"], GridSizeWidth, GridSizeHeight)

# Generates the canvas, parameters of how many cells in x and y diretion then pixel size of grid.
# grid = CanvasGrid(Apperance, model_params["gridSize"] + model_params["UniqueItems"], model_params["gridSize"], GridSizeWidth, GridSizeHeight)

# Startes the visuliation using the given model, sets the page title and the model starting settings.
#
# server = ModularServer(WarehouseModel,[grid],"Robot Swarm Order Packing Simulation",
# {"robotCount":RobotCount, "height":GridCellHeight, "width":GridCellWidth, "UniqueItems":UniqueItemsPerOrder,"MaxStockPerOrder":MaxStockPerOrder})


chart_element_of = ChartModule([{"Label": "% Ordes Filled", "Color": "#AA0000"}])
chart_element_im = ChartModule([{"Label": "Items Delivered", "Color": "#666666"}, {"Label": "Average Robot Moves", "Color": "#2BA7AD"}])

if enableCharts:
	settings = [grid, chart_element_of, chart_element_im]
else:
	settings = [grid]

server = ModularServer(WarehouseModel, settings, "Robot Swarm Order Packing Simulation", model_params)

# Launch the server
server.port = 8521  # The default
server.launch()
