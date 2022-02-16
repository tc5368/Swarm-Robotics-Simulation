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

		if self.random.choice([True,False]):
			self.x += self.random.randint(0,1)
		else:
			self.y += self.random.randint(0,1)

		#print(self.pos)
		if self.x > self.warehouseMaxX or self.y > self.warehouseMaxY or self.x <= 0 or self.y <= 0:
			#print('triggers')
			self.model.kill_agents.append(self)
		else:
			self.newpos = (self.x,self.y)
			self.model.grid.move_agent(self, self.newpos)


class Bin(Agent):
	#Idea for how to implement letting the user mouseover a grid cell to see what gorcery item it is holding.

	def __init__(self, unique_id, model, x, y, contains, stock):
		super().__init__(unique_id, model)

		self.unique_id = unique_id

		self.x = x
		self.y = y

		self.type = "Bin"

		self.contains = contains
		self.stock = stock

