from mesa import Agent


class Label(Agent):
	# Idea for how to implement letting the user mouseover a grid cell to see what grocery item it is holding.

	def __init__(self, unique_id, model, x, y, item, count):
		super().__init__(unique_id, model)

		# Sets the attributes for the cell object

		self.x = x
		self.y = y

		self.type = "Label"

		self.item = item
		self.itemCount = count

	def getComplete(self):
		return False
