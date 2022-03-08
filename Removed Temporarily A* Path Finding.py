
	# def pathFind(self):
	# 	print('Starting path finding, going from %s to %s, while avoiding booked cells' %(self.pos,self.goal))
			
	# 	parents = {}
	# 	openList = {self.pos:0}
	# 	closedList = []
	# 	g = 0
	# 	h = self.getManhattenDistance(self.pos)
	# 	f = g + h

	# 	# maybe change this to a for loop for gridsize^2 so it checks every cell and if it cant find the path then just wait.
	# 	# for nonInfiniteCount in range(500):
		
	# 	while len(openList) > 0:
	# 		node = self.getLowestCell(openList)
	# 		cost = openList[node]

	# 		if node == self.goal:
	# 			print('Done')
	# 			parents.update({self.goal:node})
	# 			self.getRouteFromParents(parents)
	# 			break


	# 		openList.pop(node)
	# 		closedList.append(node)

	# 		childNodesRaw = self.model.grid.get_neighbors(pos=node, moore=False)
	# 		childNodes = self.cleanGetNeighbors(childNodesRaw)

	# 		print()
	# 		print(node)

	# 		for childNode in childNodes:

	# 			if childNode in closedList:
	# 				continue
				
	# 			newCost = cost + 1

	# 			if (childNode in openList) and (cost < openList[childNode]):
	# 				openList.pop(childNode)

	# 			elif (childNode in closedList) and (cost < openlist[childNode]):
	# 				closedList.pop(childNode)

	# 			elif (childNode not in openList) and (childNode not in closedList):
	# 				openList.update({childNode:(cost+self.getManhattenDistance(childNode))})
	# 				print('---->',childNode,node)
	# 				print(parents)
	# 				parents.update({childNode:node})

	# 	print(parents)











   # make an openlist containing only the starting node
   # make an empty closed list
   # while (the destination node has not been reached):
   #     consider the node with the lowest f score in the open list
   #     if (this node is our destination node) :
   #         we are finished 
   #     if not:
   #         put the current node in the closed list and look at all of its neighbors
   #         for (each neighbor of the current node):
   #             if (neighbor has lower g value than current and is in the closed list) :
   #                 replace the neighbor with the new, lower, g value 
   #                 current node is now the neighbor's parent            
   #             else if (current g value is lower and this neighbor is in the open list ) :
   #                 replace the neighbor with the new, lower, g value 
   #                 change the neighbor's parent to our current node

   #             else if this neighbor is not in both lists:
   #                 add it to the open list and set its g






# '''
# 	def pathFind(self):
# 		self.openList = {}
# 		self.closedList = []

# 		startingCell = self.getCell(self.pos)
# 		self.openList.update({startingCell:0})

# 		while len(self.openList) != 0:
# 			print()
# 			print(self.unique_id)
# 			nextCell = self.getLowestCell()
# 			cellCost = self.openList.pop(nextCell)

# 			print('At cell',nextCell.pos,'with a cost of',cellCost,'trying to go to',self.goal)
# 			self.closedList.append(nextCell.pos)

# 			childCells = self.removeBots(self.model.grid.get_neighbors(pos=nextCell.pos, moore=False))

# 			# Add here need to remove the childCells that have bookings on the turn it's needed.
			
# 			childCells = self.checkBookings(childCells,(self.model.getTurnCount()+len(self.closedList)))

# 			if self.checkGoalFound(childCells):
# 				self.closedList.append(self.goal)
# 				print('Goal Found')
# 				break

# 			else:
# 				for cell in childCells:
# 					g = 1
# 					h = self.getManhattenDistance(cell)
# 					print('From ',cell.pos,'manhatten distance to goal:',h)
# 					f = g+h
# 					print('Estimate cost to goal:',f)

# 					self.openList.update({cell:f})
# 		self.bookRoute(self.closedList)
# 		self.route = self.closedList


# 	def checkBookings(self,childCells,turn):
# 		print('checking if and of these cells:',childCells,'are busy on turn',turn)
# 		validCells = []
# 		for cell in childCells:
# 			if cell.bookings.get(turn) == None:
# 				print(cell,cell.unique_id,'avaliable to be booked')
# 				validCells.append(cell)
# 			else:
# 				print(cell,cell.unique_id,'Is busy with: ',cell.bookings.get(turn),'that turn')

# 		return validCells

# 	def bookRoute(self,cellList):
# 		print('booking route:',cellList)
# 		for cellIndex in range(len(cellList)):
# 			cell = self.getCell(cellList[cellIndex])
# 			turnNumber = self.model.getTurnCount() + cellIndex

# 			print('booking cell ',cell.pos,'for turn number',turnNumber)
# 			cell.bidOn(turnNumber,self.unique_id)


# 	def getManhattenDistance(self,cell):
# 		return abs(cell.pos[0] - self.goal[0]) + abs(cell.pos[1] - self.goal[1])


# 	def checkGoalFound(self,neighbors):
# 		for cell in neighbors:
# 			if cell.pos == self.goal:
# 				return True
# 		return False

# 	def getLowestCell(self):
# 		return min(self.openList, key=self.openList.get)

# 	def removeBots(self,neighbors):
# 		botLocations = []
# 		returning = []
# 		for agent in neighbors:
# 			if agent.type == "Robot":
# 				botLocations.append(agent.pos)
# 		for agent in neighbors:
# 			if agent.type in ['Bin','DropOff'] and agent.pos not in botLocations:
# 				returning.append(agent)
# 		return returning


# 	def getCell(self,posistion):
# 		agentsInCell = self.model.grid.get_cell_list_contents(posistion)
# 		for agent in agentsInCell:
# 			if agent.type in ['Bin','DropOff']:
# 				return agent
# '''