import random

class Area:
	inventory = []
	description = ""

	def __init__(self, name, inventory,description):
		self.name = name
		self.inventory = inventory
		self.description = description

	def describeArea(self):
		print self.description
		if(self.inventory):
			i = 0
			print "Obvious items are:"
			for item in self.inventory:
				print str(i) + ": " + item.name
				i += 1
		else:
			print "No obvious items."

class Consumable:
	def __init__(self, name):
		self.name = name
		
	def consume(self, player):
		player.level += 1

class Potion(Consumable):
	def consume(self, player):
		player.health += 1

class Poison(Consumable):
	def consume(self, player):
		player.health -= 1

class AreaGenerator:
	items = [Potion("Red Potion"), Poison("Black Potion")]
	places = [["dark woods","Dark, mysterious woods surround you."],["hill","You can see for miles atop this hill"],["ravine","Water flows quietly from a nearby ravine"],["house","You've entered an older, abandoned country cottage."],["thing","An interesting thing makes this location different and unique."]]
	

	def generateArea(self): 
		place = random.randint(0,(len(self.places) -1))
		noItems = random.randint(0,4)
		items = []
		
		for i in range(noItems):
			items.append(self.randomItem())
		return Area(self.places[place][0], items,self.places[place][1])
	
	def randomItem(self):
		itemNo = random.randint(0,(len(self.items) -1))
		return self.items[itemNo]

class Map:
	map = []
	areaGenerator = AreaGenerator()
	
	def __init__(self,height,length):
		for i in range(height):
			row = []
			for x in range(length):
				row.append(self.areaGenerator.generateArea())
			self.map.append(row)
	
	def getArea(self,horizontal,vertical):
		return self.map[vertical][horizontal]

class Player:
	level = 1
	health = 10

	map = Map(100,100)
	horizontal = 0;
	vertical = 0;
	
	area = map.getArea(vertical,horizontal)
	inventory = []

	def pickupItem(self, index):
		self.area.inventory[index]
		self.inventory.append(self.area.inventory[index])
		del self.area.inventory[index]
	
	def useItem(self, index):
		self.inventory[index].consume(self)
		del self.inventory[index]
	
	def displayInventory(self):
		i = 0
		print "Your inventory:"
		for item in self.inventory:
			print str(i) + ": " + item.name
			i += 1
	
	def displayStatus(self):
		print "Level: " + str(self.level)
		print "Health: " + str(self.health)
	
	def moveHorizontal(self,movement):
		self.horizontal += movement
		self.area = self.map.getArea(self.vertical,self.horizontal)
		self.area.describeArea()
	
	def moveVertical(self,movement):
		self.vertical += movement
		self.area = self.map.getArea(self.vertical,self.horizontal)
		self.area.describeArea()


class Output:
	def printHelp(self):
		print "Known commands are:"
		print "north,south,east,west [n,s,e,w]"
		print "look [l]"
		print "status [st]"
		print "inventory [i]"
		print "pickup <item> [p]"
		print "use <item> [u]"
		print "quit [q]"
		print "help [h]"

player = Player()
output = Output()

player.area.describeArea()

while(True):
	userInput = raw_input("Please enter a command:")
	userInput = userInput.split()

	if player.health < 1:
		print "Oh dear, you've died."
		quit()

	if userInput[0] == 'inventory' or userInput[0] == 'i':
		player.displayInventory()
	elif userInput[0] == 'status' or userInput[0] == 'st':
		player.displayStatus()
	elif userInput[0] == 'pickup' or userInput[0] == 'p':
		try:
			player.pickupItem(int(userInput[1]))
		except:
			print "That item doesn't exist!"
	elif userInput[0] == 'use' or userInput[0] == 'u':
		try:
			player.useItem(int(userInput[1]))
		except:	
			print "That item doesn't exist!"
	elif userInput[0] == 'look' or userInput[0] == 'l':
		player.area.describeArea()
	elif userInput[0] == 'quit' or userInput[0] == 'q':
		quit()
	elif userInput[0] == 'help' or userInput[0] == 'h':
		output.printHelp()
	elif userInput[0] == 'north' or userInput[0] == 'n':
		player.moveVertical(1)
	elif userInput[0] == 'south' or userInput[0] == 's':
		player.moveVertical(-1)
	elif userInput[0] == 'east' or userInput[0] == 'e':
		player.moveHorizontal(1)
	elif userInput[0] == 'west' or userInput[0] == 'w':
		player.moveHorizontal(-1)
	else:
		print "Uh oh! I can't find the command '" + userInput[0] + "', please enter another command."
