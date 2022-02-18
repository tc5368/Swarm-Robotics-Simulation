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

		#For testing will be removed, if the robot is carrying nothing then it
		#will pickup the item held in the cell its currently in.
		if self.holding == []:
			self.pickupItem()
		else:
			self.dropOff()

		if self.random.choice([True,False]):
			self.x += self.random.randint(-1,1)
		else:
			self.y += self.random.randint(-1,1)

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
		#To be finished
		print('Dropping')
		if self.model.grid.get_cell_list_contents(self.pos)[0].type == 'Bin':
			if self.model.grid.get_cell_list_contents(self.pos)[0].recieveItem(self.holding[0]):
				print('Cell accepted the item')
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
			toGive = self.contains
			self.contains = []
			return [toGive]

		#If it has stock left will just give one item away and decremet the stock count
		else:
			self.stock -= 1
			return [self.contains]

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


class StartOffPoint(Agent):
	def __init__(self, unique_id, model):
		super().__init__(unique_id, model)

		#Starting cell will always be at 0,0
		self.x = 0
		self.y = 0
		self.type = 'Start'

class DropOffPoint(Agent):
	def __init__(self, unique_id, model, x, y, order):
		super().__init__(unique_id, model)

		self.x = x
		self.y = y
		self.type = 'DropOff'

		self.order = order
		self.contains = []














