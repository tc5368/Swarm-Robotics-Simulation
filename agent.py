from mesa import Agent

class Robot(Agent):
	#This is the robot agent that moves around the grid fufilling customer orders.

	def __init__(self, unique_id, model, y, x, gridInfo):
		super().__init__(unique_id, model)

		#Unique ID
		self.unique_id = unique_id

		#Denotes Robot or Bin
		self.type = "Robot"

		#The robot is initated with random coordinates (for now)
		#When the place robot function adds the robot to the grids it gives
		#the robot a self.pos which is a tuple containing (x,y)
		self.x = x
		self.y = y

		self.goal = None

		#Current task the robot is doing, used to aid understanding can see when the robot is carrying an item or going to pick something up.
		#Currently randomly chosen will be changed!
		self.current_job = self.random.choice(['Collecting','Moving'])
		self.holding = []
		#Queue containing the tasks assigned to the robot in some implementations.
		self.tasks = []

		self.warehouseMaxY = gridInfo[0]-1
		self.warehouseMaxX = gridInfo[1]-1

		#If the agent is 'dead' and should be removed - not needed in final implementation
		self.dead = False


	def step(self):

		self.x, self.y = self.pos

		#The robot picks up an item if it is not holding anything.
		#Will then check all the open orders to see if the item it's holding is needed
		#If it is listed in an open order then it will start to move the item towards the drop off
		#the checkOpenOrders will update a self.goal which will be a (x,y) tuple.
		#
		#For initial testing this will be sufficent but already a problem will arise as multiple
		#bots will try and carry a surplus of the items need to the drop off
		#
		#Need for the check open orders function to account for the stock ordered.
		#Maybe some kind of allocation system would work better in the long run.
		if self.holding == []:
			self.pickupItem()
			if self.holding != []:
				self.checkOpenOrders()

		#If the robot couldn't pick up an item and therefore has no goal will move randomly.
		if self.goal == None:
			if self.random.choice([True,False]):
				self.x += self.random.randint(-1,1)
			else:
				self.y += self.random.randint(-1,1)
		else:

			print('trying to get to ',self.goal,'from ',self.x,self.y)
			if self.goal[0] > self.x:
				self.x += 1
			elif self.goal[0] < self.x:
				self.x -= 1
			elif self.goal[1] > self.y:
				self.y += 1
			elif self.goal[1] < self.y:
				self.y -= 1

			if self.pos == self.goal:
				self.dropOff()
				self.goal = None

		#If the robot would  be making a move to try and move off the grid instead dont move.
		if self.x > self.warehouseMaxX:
			self.x = self.warehouseMaxX
		if self.y > self.warehouseMaxY:
			self.y = self.warehouseMaxY 
		if self.x < 0:
			self.x = 0
		if self.y < 0:
			self.y = 0


		if self.x > self.warehouseMaxX or self.y > self.warehouseMaxY or self.x < 0 or self.y < 0:
			#print('triggers')
			self.model.kill_agents.append(self)

		else:
			if len(self.model.grid.get_cell_list_contents((self.x, self.y))) == 1:
				self.newpos = (self.x,self.y)
				self.model.grid.move_agent(self, self.newpos)

			else:
				self.x,self.y = self.pos


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

	def checkOpenOrders(self):
		for i in range(self.warehouseMaxY+1):
			itemsNeeded = self.model.grid.get_cell_list_contents((self.warehouseMaxX,i))[0].lookingFor()
			print('------------------')
			print('robot holding: ',self.holding)
			print('dropOff',i,'needs:',itemsNeeded)
			print('------------------')
			if self.holding[0] in itemsNeeded:
				self.goal = (self.warehouseMaxX,i)
				return True
		self.burnItem()
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
		return self.contains


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

		self.order = order
		self.contains = {}
		self.complete = False

	def checkComplete(self):
		if sorted(self.contains) == sorted(self.order):
			return 'green'
		else:
			return 'black'

	def recieveItem(self,item):

		if item in self.order:			
			if item in self.contains:
				if self.order[item] < self.contains[item]:
					self.contains.update({item:(self.contains[item]+1)})
				else:
					return False
			else:
				self.contains.update({item:1})
			return True
		else:
			return False

	def lookingFor(self):
		itemsNeeded = []
		for item in self.order:
			if item in self.contains:
				if self.order[item] < self.contains[item]:
					itemsNeeded.append(item)
			else:
				itemsNeeded.append(item)
		return itemsNeeded













