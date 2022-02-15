from mesa import Agent

class Robot(Agent):
	#This is the robot agent that moves around the grid fufilling customer orders.

	def __init__(self, unique_id, model, y, x):
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