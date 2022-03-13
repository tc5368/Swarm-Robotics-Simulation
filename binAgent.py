from mesa import Agent


class Bin(Agent):
	# Idea for how to implement letting the user mouseover a grid cell to see what grocery item it is holding.

	def __init__(self, unique_id, model, x, y, contains, stock):
		super().__init__(unique_id, model)

		# Sets the attributes for the cell object
		self.unique_id = unique_id

		self.x = x
		self.y = y

		self.type = "Bin"

		self.contains = contains
		self.stock = stock

		self.bookings = {}

	def giveItem(self):
		# This function hands the an item from the contents of the bin to the robot in the same cell.
		# it will then mark itself as empty if it gives away the last item it was holding.
		# If out of stock gives no item
		if self.stock == 0:
			return []

		# If only 1 item left in stock gives it away and updates it's contents to empty
		elif self.stock == 1:
			self.stock -= 1
			toGive = self.contains[0]
			self.contains = []
			return [toGive]

		# If it has stock left will just give one item away and decremet the stock count
		else:
			self.stock -= 1
			return self.contains

	def recieveItem(self, item):

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

	def bidOn(self, turn, robot):
		self.bookings.update({turn: robot})

	def getBookings(self):
		return self.bookings
