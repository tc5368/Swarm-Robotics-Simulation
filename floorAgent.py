from mesa import Agent


class Floor(Agent):
	# Idea for how to implement letting the user mouseover a grid cell to see what grocery item it is holding.

	def __init__(self, unique_id, model, x, y):
		super().__init__(unique_id, model)

		# Sets the attributes for the cell object
		self.unique_id = unique_id
		self.type = "Floor"

		self.x = x
		self.y = y
