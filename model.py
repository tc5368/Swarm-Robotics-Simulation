from mesa import Model
from agent import *
from mesa.time import RandomActivation
from mesa.space import *
from orders import *

class WarehouseModel(Model):
	#This is the warehouse model works as the base controller to creat all of the robots

	def __init__(self, robotCount, width, height):
		#Allows the model to continue to run.
		self.running = True
		#Number of robots in the warehouse
		self.num_agents = robotCount
		#The matrix that that is the warehouse floor.
		#This needs to be changed to single grid to not allow multiple robots to enter the same space.
		self.grid = MultiGrid(width, height, False)

		#To be considered later, for now random activation means: "A scheduler which activates each agent once per step, in random order, with the order reshuffled every step."
		self.schedule = RandomActivation(self)

		#Agents that need to be killed off after they crash into the wall, will be removed.
		self.kill_agents = []


		#Adding a starting cell to the grid, concept of robots being lowered on to the grid from above all 1 by 1.
		#Cell 0 0 will always be the starting cell
		startingCell = StartOffPoint('start',self)
		self.grid.place_agent(startingCell,(startingCell.x, startingCell.y))


		#Adding dropoff bins that will each represent 1 order to be filled.
		#Idea to have the far right coloumn on the grid be all dropoff points.
		for i in range(height):
			DropOffCell = DropOffPoint('Drop off point '+str(i),self, x=width-1, y=i, order=generate_order(3))
			self.grid.place_agent(DropOffCell,(DropOffCell.x, DropOffCell.y))


		#Adding a static agent to every cell, they allow mouseover information about what the cell is holding and it's stock level.
		GridContents = allocate_items_to_grid(width*height)
		#Iterates over every cell in the grid
		for Cellx in range(width-1):
			for Celly in range(height):
				if Cellx == 0 and Celly == 0:
					continue
				#The name of the cell it just the coordinates in the grid
				cellReference = (str(Cellx)+str(" ")+str(Celly))
				#Creates a new agent to sit in the cell as a marker
				newCell = Bin(cellReference, self, x = Cellx, y = Celly, contains = GridContents.pop(), stock = 1)
				#Places the cell agent into their place in the grid
				self.grid.place_agent(newCell, (newCell.x,newCell.y))

		# Creating the Robots
		for i in range(self.num_agents):
			#Creates the robots starting at random points on the warehouse floor.
			x, y = startingCell.pos
			newRobot = Robot(i, self, y = y, x = x,gridInfo=[height,width])
			#Adds the new robot to the scheduler
			self.schedule.add(newRobot)

			#Adds the robot to the grid according to its starting coordinates
			self.grid.place_agent(newRobot, (newRobot.x, newRobot.y))

	#Activates the scheduler to move all robots forward 1 step.
	def step(self):
		self.schedule.step()

		#Any agents marked for execution are summimarily killed here.
		#For use in development no robots should be killed when working
		for agent in self.kill_agents:
			#print('removing agent at ',agent.pos)
			self.grid.remove_agent(agent)
			self.schedule.remove(agent)
		#Once all agents are killed clear the to execute list
		self.kill_agents = []