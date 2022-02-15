from mesa import Model
from agent import *
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class WarehouseModel(Model):
	#This is the warehouse model works as the base controller to creat all of the robots

	def __init__(self, robotCount, width, height):
		#Allows the model to continue to run.
		self.running = True
		#Number of robots in the warehouse
		self.num_agents = robotCount
		#The matrix that that is the warehouse floor.
		self.grid = MultiGrid(width, height, False)

		#To be considered later, for now random activation means: "A scheduler which activates each agent once per step, in random order, with the order reshuffled every step."
		self.schedule = RandomActivation(self)

		# Creating the Robots
		for i in range(self.num_agents):
			#Creates the robots starting at random points on the warehouse floor.
			newRobot = Robot(i, self, y = self.random.randrange(height), x = self.random.randrange(width),gridInfo=[height,width])
			#Adds the new robot to the scheduler
			self.schedule.add(newRobot)

			#Adds the robot to the grid according to its starting coordinates
			self.grid.place_agent(newRobot, (newRobot.x, newRobot.y))

	#Activates the scheduler to move all robots forward 1 step.
	def step(self):
		self.schedule.step()