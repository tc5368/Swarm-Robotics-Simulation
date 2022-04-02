from mesa import Agent


class Robot(Agent):
	# This is the robot agent that moves around the grid fufilling customer orders.

	def __init__(self, unique_id, model, y, x, gridInfo, pathFindingType, devMode):
		super().__init__(unique_id, model)

		# Unique ID
		self.unique_id = unique_id

		# Denotes Robot or Bin
		self.type = "Robot"
		self.pathFindingType = pathFindingType

		# The robot is initated with random coordinates (for now)
		# When the place robot function adds the robot to the grids it gives
		# the robot a self.pos which is a tuple containing (x, y)
		self.x = x
		self.y = y

		self.goal = None
		self.busy = False
		self.deadLock = 5

		# Current task the robot is doing, used to aid understanding can see when the robot is carrying an item or going to pick something up.
		# Currently randomly chosen will be changed!
		self.holding = []
		# Queue containing the tasks assigned to the robot in some implementations.
		self.tasks = []

		self.route = []

		self.warehouseMaxY = gridInfo[0] - 1
		self.warehouseMaxX = gridInfo[1] - 1

		# If the agent is 'dead' and should be removed - not needed in final implementation
		self.dead = False

		self.devMode = devMode

	def step(self):

		if self.devMode:
			if self.unique_id not in [0, 1]:
				return

		self.x, self.y = self.pos

		if self.model.openJobs == []:
			self.moveRandom()
			return

		if self.pathFindingType == 'Blind Goal':

			if self.deadLock <= 0:
				# print('deadlock detected')
				self.moveRandom()

			elif self.busy:
				self.moveTowardsGoal()

			else:
				self.getJob()
				# print('picking up a Job:', self.goal)
				self.moveTowardsGoal()

			self.checkValidCoords()
			self.checkCellEmpty()
			self.checkDeadLock()
			self.moveRobot()

		elif self.pathFindingType == 'Path Finding':
			if not self.busy:
				self.getJob()
				self.planAndBid()
			else:
				if self.route is False:
					self.route = []
					self.planAndBid()
				else:
					print('Follwing Route:', self.route)

					if self.route == []:
						# print('goal found', self.goal)
						# This section should be made into a function as it's universal to both
						if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'DropOff':
							self.dropOff()
							self.goal = None
							self.busy = False
						else:
							hovering_over = self.model.grid.get_cell_list_contents(self.pos)[0].peekItem()
							if self.checkOpenOrders(hovering_over):
								self.planAndBid()
							else:
								self.busy = False
						# Until here
					else:
						self.x, self.y = self.route.pop(0)
						self.moveRobot()
						print(self.pos)
						self.clearBooking()

	def clearBooking(self):
		self.getBin(self.pos).clearBooking()

	def planAndBid(self):
		parents = self.pathFind()
		self.getRouteFromParents(parents)
		print(self.route)
		self.bookRoute()

	def bookRoute(self):
		if self.route is False:
			return
		else:
			for turnIndex in range(len(self.route)):
				print('	 Make bid for cell %s on turn %s' % (self.route[turnIndex], turnIndex + self.model.turnCount))
				print('    ', self.getBin(self.route[turnIndex]).getBookings(), ' are the exsisting bookings on that cell')
				if (turnIndex + self.model.turnCount) in self.getBin(self.route[turnIndex]).getBookings():
					print('		Cell already booked for this turn')
				self.getBin(self.route[turnIndex]).bidOn(turnIndex + self.model.turnCount + 1, self)
			print()

	def pathFind(self):

		# print('pathfinding from %s to %s' %(self.pos, self.goal))

		openList = {}
		closedList = {}
		parents = {}

		openList.update({self.pos: 0})

		while len(openList) > 0:

			node = self.getLowestCell(openList)
			cost = openList.pop(node)

			if node == self.goal:
				# print('Goal node found')
				return parents

			childNodes = self.removeBots(self.model.grid.get_neighbors(pos=node, moore=False))
			# childNodes = self.filterAvaliable(childNodes)

			# print('Looking at node', node)

			for childNode in childNodes:

				# print('Looking at child node', childNode)

				if childNode == self.goal:
					# print("Goal node found in the loop")
					parents.update({self.goal: node})
					return parents

				g = cost + 1
				h = self.getManhattenDistance(childNode)
				f_cost = g + h

				# print('child cost', f_cost)

				if childNode in openList:
					if cost < f_cost:
						continue

				elif childNode in closedList:
					if cost < f_cost:
						continue

				else:
					openList.update({childNode: f_cost})

				parents.update({childNode: node})

			closedList.update({node: cost})
		return parents

	def getRouteFromParents(self, parents):
		if parents == {}:
			self.route = []
			return

		if self.goal not in parents:
			self.route = False
			print('Cell is not found, busy', self.goal)
			return

		beforeNode = parents[self.goal]
		self.route.insert(0, self.goal)
		while True:
			self.route.insert(0, beforeNode)
			if beforeNode == self.pos:
				break
			else:
				beforeNode = parents[beforeNode]

	def cleanGetNeighbors(self, rawNodes):
		childNodes = []
		for i in rawNodes:
			if i.type in ['Bin', 'DropOff']:
				childNodes.append(i.pos)
		return childNodes

	def removeBots(self, neighbors):
		botLocations = []
		returning = []
		for agent in neighbors:
			if agent.type == "Robot":
				botLocations.append(agent.pos)
		for agent in neighbors:
			if agent.type in ['Bin', 'DropOff'] and agent.pos not in botLocations:
				returning.append(agent.pos)
		return returning

	def getManhattenDistance(self, cell):
		try:
			return abs(cell[0] - self.goal[0]) + abs(cell[1] - self.goal[1])
		except TypeError:
			print('ERROR with ', cell, self.goal)
			exit()

	def getLowestCell(self, openList):
		return min(openList, key=openList.get)

	def getBin(self, posistion):
		contents = self.model.grid.get_cell_list_contents(posistion)
		for agent in contents:
			if agent.type in ["Bin", "DropOff"]:
				return agent

	def getJob(self):
		toCollect = self.model.openJobs.pop(0)
		print('Need to update this function')
		print('the job should include the dropoff that ordered the item.')
		self.goal = self.model.getItemLocation(toCollect)
		self.busy = True

	def checkDeadLock(self):
		# print(self.x, self.y, self.pos,(self.x, self.y) == self.pos)
		if (self.x, self.y) == self.pos:
			self.deadLock -= 1
		else:
			self.deadLock = 5
		# print(self.deadLock)

	def moveRobot(self):
		# print('moving to ', self.x, self.y, 'from ', self.pos)
		self.checkCellEmpty()
		self.model.grid.move_agent(self, (self.x, self.y))

	def checkValidCoords(self):
		if self.x > self.warehouseMaxX:
			self.x = self.warehouseMaxX
		if self.y > self.warehouseMaxY:
			self.y = self.warehouseMaxY
		if self.x < 0:
			self.x = 0
		if self.y < 0:
			self.y = 0

	def checkCellEmpty(self):
		if len(self.model.grid.get_cell_list_contents((self.x, self.y))) != 1:
			self.x, self.y = self.pos

	def moveRandom(self):
		# print('trying to move randomly to break lock')
		if self.random.choice([True, False]):
			self.x += self.random.randint(-1, 1)
		else:
			self.y += self.random.randint(-1, 1)
		# print('randomly trying:', self.x, self.y, 'from ', self.pos)

	def moveTowardsGoal(self):

		# print('trying to get to goal: ', self.goal, 'from ', self.x, self.y)
		if self.pos == self.goal:
			if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'DropOff':
				self.dropOff()
				# print('item dropped off at goal, deleting goal')
				self.goal = None
				self.busy = False
			else:
				hovering_over = self.model.grid.get_cell_list_contents(self.pos)[0].peekItem()
				# print('Found current Job item', hovering_over)
				self.checkOpenOrders(hovering_over)

		else:
			directionVec = (abs(self.goal[0] - self.x), abs(self.goal[1] - self.y))
			# print(self.goal)
			# print(self.pos)
			prob_x = directionVec[0] / (directionVec[0] + directionVec[1])
			prob_y = directionVec[1] / (directionVec[0] + directionVec[1])
			# print(prob_x, prob_y)
			direction = self.model.random.choices([True, False], (prob_x, prob_y))[0]
			# print(direction)

			if direction:
				if self.goal[0] > self.x:
					self.x += 1
				elif self.goal[0] < self.x:
					self.x -= 1
			else:
				if self.goal[1] > self.y:
					self.y += 1
				elif self.goal[1] < self.y:
					self.y -= 1

	def pickupItem(self):
		# Gets the cell it's currently in's contents and then select the cell object which is first in the list hence [0]
		# It then calls the cell objects giveItem function and takes the output of that as it's new inventory.
		if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'Bin':
			self.holding = self.model.grid.get_cell_list_contents(self.pos)[0].giveItem()

	def dropOff(self):
		# For dropping into a bin
		if self.model.grid.get_cell_list_contents(self.pos)[0].type in ['Bin', 'DropOff']:
			if self.model.grid.get_cell_list_contents(self.pos)[0].recieveItem(self.holding[0]):
				self.holding = []
				self.busy = False

	def checkOpenOrders(self, item):
		for i in range(self.warehouseMaxY + 1):
			itemsNeeded = self.model.grid.get_cell_list_contents((self.warehouseMaxX, i))[0].lookingFor()
			# print('------------------')
			# print('Currently over bin holding: ', item)
			# print('dropOff', i, 'needs:', itemsNeeded)
			# print('------------------')
			if item in itemsNeeded:
				self.goal = (self.warehouseMaxX, i)
				self.pickupItem()
				return True
		# print('Robot current goal', self.goal, item)
		self.goal = None
		self.busy = False
		# print('goal removed')
		return False

	def advance(self):
		None
