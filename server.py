from model import *
from agent import *
from binAgent import *
from dropOffAgent import *
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def Apperance(agent):
	if agent.type == "Robot":
		return robotAppearance(agent)

	elif agent.type == "Bin":
		return binAppearance(agent)

	elif agent.type == "Floor":
		return floorAppearance(agent)

	elif agent.type == "Label":
		return labelAppearance(agent)

	elif agent.type == "DropOff":
		return dropOffAppearance(agent)


def robotAppearance(agent):
	if model_params["displayMode"].value:
		if agent.holding == []:
			robotImage = 'resources/Robot.png'
		else:
			robotImage = 'resources/Robot Busy.png'
		robotLayer = 'Interaction'
	else:
		robotImage = 'rect'
		robotLayer = 'WarehouseFloor'

	if agent.holding == []:
		robotColor = "Blue"
	else:
		robotColor = "Red"

	if model_params["devMode"].value and agent.unique_id == 0:
		robotColor = "Orange"

	portrayal = {"Shape": robotImage,
				"Filled": "true",
				"Color": robotColor,
				"Layer": robotLayer,
				"Number": agent.unique_id,
				"Carrying": agent.holding,
				"w": 0.6,
				"h": 0.6}
	return portrayal


def binAppearance(agent):
	if model_params["displayMode"].value:
		formattedItem = str(agent.contains[0]).replace(' ', '').replace('/', '').replace('(', '').replace(')', '').replace('-', '')
		bin_image = "resources/" + formattedItem + ".png"
	else:
		bin_image = 'rect'

	if agent.bookings != {}:
		binColour = 'green'
	else:
		binColour = "grey"

	portrayal = {"Shape": bin_image,
				"Filled": "true",
				"Layer": 'WarehouseFloor',
				"Reference": agent.unique_id,
				"Contains": agent.contains,
				"Bookings": str(agent.bookings),
				"Color": binColour,
				"w": 1,
				"h": 1,
				"scale": 0.75}
	return portrayal


def floorAppearance(agent):
	portrayal = {"Shape": 'rect',
			"Filled": "true",
			"Layer": 'WarehouseFloor',
			"Color": 'grey',
			"w": 1,
			"h": 1,
			"scale": 1}
	return portrayal


def labelAppearance(agent):
	formattedItem = str(agent.item).replace(' ', '').replace('/', '').replace('(', '').replace(')', '').replace('-', '')
	label_image = "resources/" + formattedItem + ".png"
	portrayal = {"Shape": label_image,
				"Filled": "true",
				"Layer": 'WarehouseFloor',
				"Name": agent.unique_id,
				"Color": 'White',
				"text": agent.itemCount,
				"w": 1,
				"h": 1,
				"scale": 0.75}
	return portrayal


def dropOffAppearance(agent):
	if agent.checkComplete():
		dropOffColour = "Green"
	else:
		dropOffColour = agent.getPercentageDone()

	if model_params["displayMode"].value:
		dropOffLayer = 'Interaction'
	else:
		dropOffLayer = 'WarehouseFloor'

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
GridSize = 14
enableCharts = True
# enableCharts = False

# # Added sliders
model_params = {
	"robotCount": UserSettableParameter("slider", "Robot Initial Count", (round((GridSize ** 2 - GridSize) * 0.15) // 3) + 1, 1, (GridSize ** 2 - GridSize)),
	"gridSize": GridSize,
	"UniqueItems": UserSettableParameter("slider", "Unique Items Per Order", 5, 1, 10),
	"MaxStockPerOrder": UserSettableParameter("slider", "Maximum of a stock per order", 5, 1, 20),
	"devMode": UserSettableParameter('checkbox', 'Example Mode', value=False),
	"displayMode": UserSettableParameter('checkbox', 'Display Mode', value=True),
	"pathFindingType": UserSettableParameter('choice', 'Pathfinding Type', value='Path Finding', choices=['Path Finding', 'Blind Goal'])
}

# Dynamic sizing so that all grid sizes will not affect the aspect ratio of the visulisation
CellSize = 750 / GridSize
GridSizeHeight = CellSize * GridSize
GridSizeWidth = CellSize * (GridSize + model_params["UniqueItems"].value)

# Uses a class from the visulisation module of MESA and initialises the appearance of the brower page
grid = CanvasGrid(Apperance, model_params["gridSize"] + model_params["UniqueItems"].value, model_params["gridSize"], GridSizeWidth, GridSizeHeight)

# If the charts are enables will create the objects and then update the settings that will be passed to the brower
if enableCharts:
	chart_element_of = ChartModule([{"Label": "% Ordes Filled", "Color": "#AA0000"}])
	chart_element_im = ChartModule([{"Label": "Items Delivered", "Color": "#666666"}, {"Label": "Average Robot Moves", "Color": "#2BA7AD"}])
	settings = [grid, chart_element_of, chart_element_im]
else:
	settings = [grid]

# Initialises the serrver object and launches it on default port 8521
server = ModularServer(WarehouseModel, settings, "Robot Swarm Order Packing Simulation", model_params)
server.port = 8521
server.launch()
