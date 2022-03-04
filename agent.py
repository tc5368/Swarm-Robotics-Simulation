from mesa import Agent

class Robot(Agent):
	#This is the robot agent that moves around the grid fufilling customer orders.

	def __init__(self, unique_id, model, y, x, gridInfo,pathFindingType):
		super().__init__(unique_id, model)

		#Unique ID
		self.unique_id = unique_id

		#Denotes Robot or Bin
		self.type = "Robot"
		self.pathFindingType = pathFindingType

		#The robot is initated with random coordinates (for now)
		#When the place robot function adds the robot to the grids it gives
		#the robot a self.pos which is a tuple containing (x,y)
		self.x = x
		self.y = y

		self.goal = None
		self.busy = False
		self.deadLock = 5

		#Current task the robot is doing, used to aid understanding can see when the robot is carrying an item or going to pick something up.
		#Currently randomly chosen will be changed!
		self.holding = []
		#Queue containing the tasks assigned to the robot in some implementations.
		self.tasks = []

		self.warehouseMaxY = gridInfo[0]-1
		self.warehouseMaxX = gridInfo[1]-1

		#If the agent is 'dead' and should be removed - not needed in final implementation
		self.dead = False


	def step(self):

		#print('------------------------')

		self.x, self.y = self.pos

		if self.model.openJobs == []:
			return

		if self.pathFindingType == 'Blind Goal':

			if self.deadLock <= 0:
				#print('deadlock detected')
				self.moveRandom()

			elif self.busy == True:
				self.moveTowardsGoal()

			else:
				self.getJob()
				#print('picking up a Job:',self.goal)
				self.moveTowardsGoal()

			self.checkValidCoords()
			self.checkCellEmpty()
			self.checkDeadLock()
			self.moveRobot()

		elif self.pathFindingType == 'A* Search':
			print('--------------------')
			if self.busy == False:
				self.getJob()
				self.pathFind()
			else:
				print('Follwing Route: self.route eventully')
			print('--------------------')


	def pathFind(self):
		self.openList = {}
		self.closedList = {}

		startingCell = self.getCell()
		self.openList.update({startingCell:0})

		while len(self.openList) != 0:
			nextCell = self.getLowestCell()
			cellCost = self.openList.pop(nextCell)

			print('At cell',nextCell.pos,'with a cost of',cellCost,'trying to go to',self.goal)

			childCells = self.removeBots(self.model.grid.get_neighbors(pos=nextCell.pos, moore=False))

			if self.checkGoalFound(childCells):
				print('Goal Found')
				break

			else:
				for cell in childCells:
					g = 1
					h = self.getManhattenDistance(cell)
					print('From ',cell.pos,'manhatten distance to goal:',h)
					f = g+h
					print('Estimate cost to goal:',f)

					self.openList.update({cell:f})

	def getManhattenDistance(self,cell):
		return abs(cell.pos[0] - self.goal[0]) + abs(cell.pos[1] - self.goal[1])


	def checkGoalFound(self,neighbors):
		for cell in neighbors:
			if cell.pos == self.goal:
				return True
		return False

	def getLowestCell(self):
		return min(self.openList, key=self.openList.get)

	def removeBots(self,neighbors):
		returning = []
		for agent in neighbors:
			if agent.type in ['Bin','DropOff']:
				returning.append(agent)
		return returning


	def getCell(self):
		agentsInCell = self.model.grid.get_cell_list_contents((self.x,self.y))
		for agent in agentsInCell:
			if agent.type in ['Bin','DropOff']:
				return agent

	def getJob(self):
		toCollect = self.model.openJobs.pop(0)
		self.goal = self.model.getItemLocation(toCollect)
		self.busy = True

	def checkDeadLock(self):
		#print(self.x, self.y, self.pos,(self.x, self.y) == self.pos)
		if (self.x, self.y) == self.pos:
			self.deadLock -= 1
		else:
			self.deadLock = 5
		#print(self.deadLock)

	def moveRobot(self):
		#print('moving to ',self.x,self.y,'from ',self.pos)
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
			self.x,self.y = self.pos

	def moveRandom(self):
		#print('trying to move randomly to break lock')
		if self.random.choice([True,False]):
			self.x += self.random.randint(-1,1)
		else:
			self.y += self.random.randint(-1,1)
		#print('randomly trying:',self.x,self.y,'from ',self.pos)

	def moveTowardsGoal(self):

		#print('trying to get to goal: ',self.goal,'from ',self.x,self.y)
		
		#Moving diagonally... Need to remove.
		#
		#Could add bias here, can work out a x,y vector and then change the probability of which direction to go based on the angle of the vector.
		#
		if self.pos == self.goal:
			if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'DropOff':
				self.dropOff()
				#print('item dropped off at goal, deleting goal')
				self.goal = None
				self.busy = False
			else:
				hovering_over = self.model.grid.get_cell_list_contents(self.pos)[0].peekItem()
				#print('Found current Job item',hovering_over)
				self.checkOpenOrders(hovering_over)

		else:
			directionVec = (abs(self.goal[0] - self.x), abs(self.goal[1] - self.y))
			#print(self.goal)
			#print(self.pos)
			prob_x = directionVec[0]/(directionVec[0]+directionVec[1])
			prob_y = directionVec[1]/(directionVec[0]+directionVec[1])
			#print(prob_x,prob_y)
			direction = self.model.random.choices([True,False],(prob_x,prob_y))[0]
			#print(direction)

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
		#Gets the cell it's currently in's contents and then select the cell object which is first in the list hence [0]
		#It then calls the cell objects giveItem function and takes the output of that as it's new inventory.
		if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'Bin':
			self.holding = self.model.grid.get_cell_list_contents(self.pos)[0].giveItem()


	def dropOff(self):
		#For dropping into a bin
		if self.model.grid.get_cell_list_contents(self.pos)[0].type in ['Bin','DropOff']:
			if self.model.grid.get_cell_list_contents(self.pos)[0].recieveItem(self.holding[0]):
				self.holding = []
				self.busy = False

	def checkOpenOrders(self,item):
		for i in range(self.warehouseMaxY+1):
			itemsNeeded = self.model.grid.get_cell_list_contents((self.warehouseMaxX,i))[0].lookingFor()
			# print('------------------')
			# print('Currently over bin holding: ',item)
			# print('dropOff',i,'needs:',itemsNeeded)
			# print('------------------')
			if item in itemsNeeded:
				self.goal = (self.warehouseMaxX,i)
				self.pickupItem()
				return True
		#print('Robot current goal',self.goal,item)
		self.goal = None
		self.busy = False
		#print('goal removed')
		return False

	def burnItem(self):
		#Just for testing
		self.holding = []


class Bin(Agent):
	#Idea for how to implement letting the user mouseover a grid cell to see what grocery item it is holding.

	def __init__(self, unique_id, model, x, y, contains, stock):
		super().__init__(unique_id, model)

		#Sets the attributes for the cell object
		self.unique_id = unique_id

		self.x = x
		self.y = y

		self.type = "Bin"

		self.contains = contains
		self.stock = stock

	def giveItem(self):
		#This function hands the an item from the contents of the bin to the robot in the same cell.
		#it will then mark itself as empty if it gives away the last item it was holding.
		
		#If out of stock gives no item
		if self.stock == 0:
			return []

		#If only 1 item left in stock gives it away and updates it's contents to empty
		elif self.stock == 1:
			self.stock -= 1
			toGive = self.contains[0]
			self.contains = []
			return [toGive]

		#If it has stock left will just give one item away and decremet the stock count
		else:
			self.stock -= 1
			return self.contains

	def recieveItem(self,item):

		if self.contains == []:
			self.contains = [item]
			self.stock += 1
			return True

		elif item == self.contains[0]:
			self.stock += 1
			return True

		else:
			return False

	def peekItem(self):
		return self.contains[0]


# class StartOffPoint(Agent):
# 	def __init__(self, unique_id, model):
# 		super().__init__(unique_id, model)

# 		#Starting cell will always be at 0,0
# 		self.x = 0
# 		self.y = 0
# 		self.type = 'Start'

class DropOffPoint(Agent):
	def __init__(self, unique_id, model, x, y, order):
		super().__init__(unique_id, model)

		self.x = x
		self.y = y
		self.type = 'DropOff'
		self.unique_id = unique_id

		self.order = order
		self.contains = {}
		self.complete = False

	def checkComplete(self):
		if self.contains == self.order:
			return True
		else:
			return False

	def getPercentageDone(self):

		colorOutput = []
		numberTotal = sum(self.order.values())
		numberHolding = sum(self.contains.values())

		for i in range(numberHolding):
			colorOutput.append('#FFFF00')
		for i in range(numberTotal - numberHolding):
			colorOutput.append('#000000')
		return colorOutput

	def recieveItem(self,item):
		# print('Checking if can recieve ',item,'into',self.contains,'with order',self.order)
		if item in self.order:			
			if item in self.contains:
				if self.order[item] > self.contains[item]:
					self.contains.update({item:(self.contains[item]+1)})

				elif self.order[item] <= self.contains[item]:
					None

				else:
					return False
			else:
				self.contains.update({item:1})
			return True
		else:
			return False

	def lookingFor(self):
		itemsNeeded = []

		# print('checking',self.order,self.contains)
		for item in self.order:
			if item in self.contains:
				if self.order[item] > self.contains[item]:
					itemsNeeded.append(item)
			else:
				itemsNeeded.append(item)
		# print('needed',itemsNeeded)
		return itemsNeeded












