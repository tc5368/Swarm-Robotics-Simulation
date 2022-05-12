from mesa import Model
from agent import *
from binAgent import *
from dropOffAgent import *
from labelAgent import *
from floorAgent import *
from mesa.time import *
from mesa.space import *
from mesa.datacollection import DataCollector


class WarehouseModel(Model):
	"""
	A model for simulating robotic workers moving around a simulated warehouse fufilling customer orders.
	"""
	# This is the warehouse model works as the base controller to creat all of the robots

	def __init__(self, robotCount, gridSize, UniqueItems, MaxStockPerOrder, pathFindingType, devMode, displayMode):
		# Allows the model to continue to run.
		self.running = True

		# Number of robots in the warehouse
		self.num_agents = robotCount

		# Open jobs is the items currently needed, will be assigned later
		self.openJobs = []

		# The size of the warehouse floor.
		self.width = gridSize
		self.height = gridSize

		# If the display mode is on will create a longer grid to place the labels in
		self.widthWithOrderQueue = gridSize + UniqueItems

		# Creates the grid object from the MESA Space module
		if displayMode:
			self.grid = MultiGrid(self.widthWithOrderQueue, self.height, False)
		else:
			self.grid = MultiGrid(self.width, self.height, False)

		# Creates the schedular to activate the agents
		self.schedule = RandomActivation(self)

		# Initialises the count that is used by the data collectors to plot the graphs
		self.turnCount = 0
		self.itemsDelivered = 0
		self.robotMoves = 0

		# self.random.seed(1)


		self.grocery_items = ["tropical fruit", "whole milk", "pip fruit", "other vegetables", "rolls/buns", "pot plants", "citrus fruit", "beef", "frankfurter", "chicken", "butter", "fruit/vegetable juice", "packaged fruit/vegetables", "chocolate", "specialty bar", "butter milk", "bottled water", "yogurt", "sausage", "brown bread", "hamburger meat", "root vegetables", "pork", "pastry", "canned beer", "berries", "coffee", "misc. beverages", "ham", "turkey", "curd cheese", "red/blush wine", "frozen potato products", "flour", "sugar", "frozen meals", "herbs", "soda", "detergent", "grapes", "processed cheese", "fish", "sparkling wine", "newspapers", "pasta", "popcorn", "beverages", "bottled beer", "dessert", "dog food", "specialty chocolate", "condensed milk", "cleaner", "white wine", "meat", "ice cream", "hard cheese", "cream cheese ", "liquor", "pickled vegetables", "liquor (appetizer)", "UHT-milk", "candy", "onions", "hair spray", "photo/film", "domestic eggs", "margarine", "shopping bags", "salt", "oil", "whipped/sour cream", "frozen vegetables", "sliced cheese", "dish cleaner", "baking powder", "specialty cheese", "salty snack", "Instant food products", "pet care", "white bread", "cling film/bags", "soap", "frozen chicken", "house keeping products", "decalcifier", "frozen dessert", "vinegar", "nuts/prunes", "potato products", "frozen fish", "light bulbs", "canned vegetables", "chewing gum", "canned fish", "cookware", "semi-finished bread", "cat food", "bathroom cleaner", "prosecco", "liver loaf", "zwieback", "canned fruit", "frozen fruits", "brandy", "baby cosmetics", "spices", "napkins", "waffles", "sauces", "rum", "chocolate marshmallow", "long life bakery product", "bags", "sweet spreads", "soups", "mustard", "instant coffee", "snack products", "organic sausage", "soft cheese", "dental care", "roll products ", "kitchen towels", "flower soil/fertilizer", "cereals", "meat spreads", "dishes", "male cosmetics", "candles", "whisky", "tidbits", "cooking chocolate", "seasonal products", "liqueur", "abrasive cleaner", "syrup", "ketchup", "rubbing alcohol", "cocoa drinks", "softener", "cake bar", "honey", "jam", "kitchen utensil", "flower (seeds)", "rice", "tea", "salad dressing", "specialty vegetables", "pudding powder", "ready soups", "make up remover", "toilet cleaner", "preservation products"]

		# Adding dropoff bins that will each represent 1 order to be filled.
		# Idea to have the far right coloumn on the grid be all dropoff points.

		numberOfCells = ((self.width * self.height) - self.height)

		for i in range(self.height):
			DropOffCell = DropOffPoint('Drop off point ' + str(i),
										self,
										x=self.width - 1,
										y=i,
										order=self.generate_order(UniqueItems, MaxStockPerOrder, numberOfCells),
										displayMode=displayMode)

			self.grid.place_agent(DropOffCell, (DropOffCell.x, DropOffCell.y))

			if displayMode:
				# Adds in the labels on the right hand side of the grid based on the order in the dropoff.
				toLabel = DropOffCell.getOrder()

				for ix in range(UniqueItems):
					newFloor = Floor("Floor", self, x=self.width + ix, y=i)
					self.grid.place_agent(newFloor, (newFloor.x, newFloor.y))

				for ix in range(len(toLabel)):
					item, count = toLabel.popitem()
					labelAgent = Label(item, self, x=self.width + ix, y=i, item=item, count=count)
					self.grid.place_agent(labelAgent, (labelAgent.x, labelAgent.y))

		# Adding a static agent to every cell, they allow mouseover information about what the cell is holding
		GridContents = self.allocate_items_to_grid(((self.width * self.height) - self.height))
		# Iterates over every cell in the grid
		for Cellx in range(self.width - 1):
			for Celly in range(self.height):

				# The name of the cell it just the coordinates in the grid
				cellReference = (str(Cellx) + str(" ") + str(Celly))
				# Creates a new agent to sit in the cell as a marker
				newCell = Bin(cellReference, self, x=Cellx, y=Celly, contains=[GridContents.pop()])
				# Places the cell agent into their place in the grid
				self.grid.place_agent(newCell, (newCell.x, newCell.y))

		# Creating the Robots
		for i in range(self.num_agents):
			# Creates the robots starting at random points on the warehouse floor.
			# Loop to create the new robots and to add them into a grid cell that is empty
			while True:
				x = self.random.randint(0, self.width - 2)
				y = self.random.randint(0, self.height - 1)
				# When the random values find an empty grid cell break the loop and place the robot
				if len(self.grid.get_cell_list_contents((x, y))) == 1:
					break

			newRobot = Robot(i, self, y=y, x=x, gridInfo=[self.height, self.width], pathFindingType=pathFindingType, devMode=devMode)

			# Adds the new robot to the scheduler
			self.schedule.add(newRobot)

			# If in example mode then robots that don't move need to have items they start
			# on top of removed from all the orders.
			if devMode:
				cell = self.grid.get_cell_list_contents((newRobot.x, newRobot.y))[0]
				toRemove = cell.peekItem()
				for Celly in range(self.height):
					gridCell = self.grid.get_cell_list_contents((self.width - 1, Celly))[0]
					if toRemove in gridCell.order:
						gridCell.order.pop(toRemove)

			# Adds the robot to the grid according to its starting coordinates
			self.grid.place_agent(newRobot, (newRobot.x, newRobot.y))

			# Starting the data collectors
			self.datacollector = DataCollector({
				"% Ordes Filled": lambda m: self.countComplete(),
				"Items Delivered": lambda m: self.getItemsDelivered(),
				"Average Robot Moves": lambda m: self.getAvgRobotMoves()})

		self.step()

	def testComplete(self):
		for i in range(self.height):
			# print('Cell %s not complete' %i)
			# print(self.grid.get_cell_list_contents((self.width - 1, i))[0].checkComplete())
			if not self.grid.get_cell_list_contents((self.width - 1, i))[0].checkComplete():
				return False
		return True

	def countComplete(self):
		count = 0
		for i in range(self.height):
			if self.grid.get_cell_list_contents((self.width - 1, i))[0].checkComplete():
				count += 1
		return (count / self.height) * 100

	def getItemsDelivered(self):
		return self.itemsDelivered

	def getAvgRobotMoves(self):
		averageStepsPerRobot = self.robotMoves // self.num_agents
		# print(averageStepsPerRobot)
		return averageStepsPerRobot

	def getOrderLength(self):
		count = 0
		for i in range(self.height):
			orderVal = self.grid.get_cell_list_contents((self.width - 1, i))[0].order.values()
			for ix in orderVal:
				count += ix
		return count

	def getItemLocation(self, item):
		for Cellx in range(self.width - 1):
			for Celly in range(self.height):
				checking = self.grid.get_cell_list_contents((Cellx, Celly))[0]
				if checking.type == 'Bin':
					if item == checking.peekItem():
						if item is None:
							print('Bin needs restocking at %s %s' % (Cellx, Celly))
						return (Cellx, Celly)
		else:
			print('Invalid starting setup, not enough items to fufil orders')
			exit()

	def getOpenJobs(self):
		needed = []
		self.openJobs = []
		for Celly in range(self.height):
			gridCell = self.grid.get_cell_list_contents((self.width - 1, Celly))[0]
			itemsNeeded = gridCell.lookingFor()
			for item in itemsNeeded:
				needed.append([Celly, item])
		self.random.shuffle(needed)
		for i in needed:
			self.openJobs.append(i)

	def getTurnCount(self):
		return self.turnCount

	def allocate_items_to_grid(self, num_cells):
		if num_cells < len(self.grocery_items):
			grid = self.grocery_items[0:num_cells]
		else:
			grid = self.grocery_items + self.random.choices(self.grocery_items, k=num_cells - len(self.grocery_items))
		grid.sort()
		return grid

	def generate_order(self, number_of_items=10, maxStockperItem=3, maxNum=10):
		if maxNum < len(self.grocery_items):
			items = self.random.choices(self.grocery_items[0:maxNum], k=number_of_items)
		else:
			items = self.random.choices(self.grocery_items, k=number_of_items)
		items.sort()
		order = {}
		for item in items:
			order.update({item: self.random.randint(1, maxStockperItem)})
		return(order)

	# Activates the scheduler to move all robots forward 1 step.
	def step(self):
		self.turnCount += 1
		self.schedule.step()
		self.datacollector.collect(self)

		if self.testComplete():
			# print(self.getOrderLength())
			self.running = False

		self.getOpenJobs()
		# print(self.openJobs)

		# Any agents marked for execution are summimarily killed here.
		# For use in development no robots should be killed when working
		# for agent in self.kill_agents:
		# 	print('removing agent at ', agent.pos)
		# 	self.grid.remove_agent(agent)
		# 	self.schedule.remove(agent)
		# Once all agents are killed clear the to execute list
		# self.kill_agents = []
