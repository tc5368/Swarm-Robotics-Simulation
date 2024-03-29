from mesa import Agent


class DropOffPoint(Agent):
	def __init__(self, unique_id, model, x, y, order, displayMode):
		super().__init__(unique_id, model)

		self.x = x
		self.y = y
		self.type = 'DropOff'
		self.unique_id = unique_id

		self.order = order
		self.contains = {}
		self.complete = False

		self.bookings = {}

		self.displayMode = displayMode

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

	def recieveItem(self, item):
		# print('Checking if can recieve ',item,'into',self.contains,'with order',self.order)
		if item in self.order:
			if item in self.contains:
				if self.order[item] > self.contains[item]:
					self.contains.update({item: (self.contains[item] + 1)})
					if self.displayMode:
						self.updateLabels()

				elif self.order[item] <= self.contains[item]:
					None

				else:
					return False
			else:
				self.contains.update({item: 1})
				if self.displayMode:
					self.updateLabels()
			self.model.itemsDelivered += 1
			return True
		else:
			return False

	def updateLabels(self):
		for item in self.order:
			if item in self.contains:
				for ix in range(1, len(self.order) + 1):
					labelAgent = self.model.grid.get_cell_list_contents((self.pos[0] + ix, self.pos[1]))
					if len(labelAgent) < 2:
						continue
					else:
						labelAgent = labelAgent[1]

						if labelAgent.item == item:
							labelAgent.itemCount -= 1
				if self.contains[item] == self.order[item]:
					self.clearItem(item)

	def clearItem(self, item):
		for ix in range(1, len(self.order) + 1):
			labelAgent = self.model.grid.get_cell_list_contents((self.pos[0] + ix, self.pos[1]))
			if len(labelAgent) < 2:
				continue
			labelAgent = labelAgent[1]
			if labelAgent.item == item:
				self.model.grid.remove_agent(labelAgent)

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

	def clearBooking(self):
		print(self.bookings)
		print(self.model.getTurnCount())
		self.bookings.pop(self.model.getTurnCount())

	def getOrder(self):
		return self.order.copy()

	def bidOn(self, turn, robot):
		self.bookings.update({turn: robot})

	def getBookings(self):
		return self.bookings

	def bookingUsed(self):
		self.bookings.pop(self.model.turnCount - 1)
