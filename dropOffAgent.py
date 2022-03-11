from mesa import Agent

class DropOffPoint(Agent):
	def __init__(self, unique_id, model, x, y, order):
		super().__init__(unique_id, model)

		self.x = x
		self.y = y
		self.type = 'DropOff'
		self.unique_id = unique_id

		self.order = order
		self.contains = {}
		self.complete = False

		self.bookings = {}

	def checkComplete(self):
		if self.contains == self.order:
			return True
		else:
			return False

	def getPercentageDone(self):
		colorOutput = []
		numberTotal = sum(self.order.values())
		numberHolding = sum(self.contains.values())

		for i in range(numberHolding):
			colorOutput.append('#FFFF00')
		for i in range(numberTotal - numberHolding):
			colorOutput.append('#000000')
		return colorOutput

	def recieveItem(self,item):
		# print('Checking if can recieve ',item,'into',self.contains,'with order',self.order)
		if item in self.order:			
			if item in self.contains:
				if self.order[item] > self.contains[item]:
					self.contains.update({item:(self.contains[item]+1)})

				elif self.order[item] <= self.contains[item]:
					None

				else:
					return False
			else:
				self.contains.update({item:1})
			return True
		else:
			return False

	def lookingFor(self):
		itemsNeeded = []

		# print('checking',self.order,self.contains)
		for item in self.order:
			if item in self.contains:
				if self.order[item] > self.contains[item]:
					itemsNeeded.append(item)
			else:
				itemsNeeded.append(item)
		# print('needed',itemsNeeded)
		return itemsNeeded

	def bidOn(self,turn,robot):
		self.bookings.update({turn:robot})

	def getBookings(self):
		return self.bookings

	def advance(self):
		None










