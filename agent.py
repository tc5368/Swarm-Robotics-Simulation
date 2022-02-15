from mesa import Agent

class Robot(Agent):
	#This is the robot agent that moves around the grid fufilling customer orders.

	def __init__(self, unique_id, model, y, x, gridInfo):
		super().__init__(unique_id, model)

		#Unique ID
		self.unique_id = unique_id

		#The robot is initated with random coordinates (for now)
		self.y = y
		self.x = x

		#Current task the robot is doing, used to aid understanding can see when the robot is carrying an item or going to pick something up.
		#Currently randomly chosen will be changed!
		self.current_job = self.random.choice(['Collecting','Moving'])
		#Queue containing the tasks assigned to the robot in some implementations.
		self.tasks = []

		self.warehouseMaxY = gridInfo[0]-1
		self.warehouseMaxX = gridInfo[1]-1


	def step(self):
		print(self.x,self.y)

		toMove = [self.x,self.y]
		if self.random.choice([True,False]):
			self.x += self.random.randint(-1,1)
		else:
			self.y += self.random.randint(-1,1)

		print(self.x,self.y)

		if 0 == self.x > self.warehouseMaxX or 0 == self.y > self.warehouseMaxY:
			print('triggers')
			self.model.grid.remove_agent(self)

		self.model.grid.move_agent(self,(self.x,self.y))
		#print('I am bot %s and I am at x coord: %s' %(self.unique_id,self.x))

