import random

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

class Enemy: 
	item = ""
	name = ""
	LVL = 0
	HP = 0
	STR = 0
	DEF = 0
	MAG = 0
	SPD = 0
	alive = 1
	attack = ""
	
	def __init__(self,name,LVL,HP,STR,DEF,MAG,SPD,item,attack):
		self.item = item
		self.LVL = LVL
		self.name = name
		self.HP = HP
		self.STR = STR
		self.DEF = DEF
		self.MAG = MAG
		self.SPD = SPD
		self.attack = attack

class EnemyGenerator:
	namesets = [["Dragon","he Dragon biteth thy (ugly) face!"],["Troll","The Troll hits thy head with his big stick!"],["Mage","The Mage casts Magic Missile!"],["Rabbit","The Rabbit bites your foot with great prejudice!"],["Vampire","The Vapire suuucks your blooood!"]]
	items = [Potion("Red Potion"), Poison("Black Potion")]
	
	
	def generateEnemy(self,lvl):
		HP = 0
		STR = 0
		DEF = 0
		MAG = 0
		SPD = 0
		
		SP = lvl * 4 + lvl
		for i in range(SP):
			assign = random.randint(1,5)
			if assign == 1:
				HP += 1
			elif assign == 2:
				STR += 1
			elif assign == 3:
				DEF += 1
			elif assign == 4:
				MAG += 1
			elif assign == 5:
				SPD += 1
		
		setNo = random.randint(0,4)
		#name,LVL,HP,STR,DEF,MAG,SPD,item,attack
		return Enemy(self.namesets[setNo][0],lvl,HP,STR,DEF,MAG,SPD,self.items[0],self.namesets[setNo][1])
		

class Area:
	inventory = []
	description = ""
	enemy = Enemy("Dragon",1,7,1,1,0,1,0,"The Dragon biteth thy (ugly) face!")

	def __init__(self, name, inventory,description,enemy):
		self.name = name
		self.inventory = inventory
		self.description = description
		self.enemy = enemy

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
		if self.enemy != 0:
			print "A " + self.enemy.name + " lurks nearby."



class AreaGenerator:
	enemyGen = EnemyGenerator()
	items = [Potion("Red Potion"), Poison("Black Potion")]
	places = [["dark woods","Dark, mysterious woods surround you."],["hill","You can see for miles atop this hill"],["ravine","Water flows quietly from a nearby ravine"],["house","You've entered an older, abandoned country cottage."],["thing","An interesting thing makes this location different and unique."]]
	

	def generateArea(self): 
		place = random.randint(0,(len(self.places) -1))
		noItems = random.randint(0,4)
		items = []
		
		for i in range(noItems):
			items.append(self.randomItem())
		return Area(self.places[place][0], items,self.places[place][1],self.enemyGen.generateEnemy(1))
	
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
	STR = 1
	DEF = 1
	SPD = 1
	MAG = 0
	XP = 0
	SP = 0

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
		print "EXP: " + str(self.XP)
		print "Health: " + str(self.health)
		print "Strength: " + str(self.STR)
		print "Defense: " + str(self.DEF)
		print "Speed: " + str(self.SPD)
		print "Magicness: " + str(self.MAG)
	
	def moveHorizontal(self,movement):
		self.horizontal += movement
		self.area = self.map.getArea(self.vertical,self.horizontal)
		self.area.describeArea()
	
	def moveVertical(self,movement):
		self.vertical += movement
		self.area = self.map.getArea(self.vertical,self.horizontal)
		self.area.describeArea()
	
	def fight(self,enemy):
		print "A wild " + enemy.name + " appears!"
		run = True
		while(run):
			userInput = raw_input("What will you do?:")
			userInput = userInput.lower()
			userInput = userInput.split()	
			
			if userInput[0] == "h" or userInput[0] == "help":
				print "You need help? Oh geez. Look you're fighting a " + enemy.name + "and it's winning. You can ATTACK, DEFEND or RUN. Ye can also use STATUS to check ye health an' the like."
			elif userInput[0] == "attack" or userInput[0] == "a":
				initiative = random.randint(0,20) + self.SPD
				enemyInitiative = random.randint(0,20) + enemy.SPD
				if initiative > enemyInitiative:
					self.attack(enemy)
					self.beAttacked(enemy)
				else:
					self.beAttacked(enemy)
					self.attack(enemy)
			elif userInput[0] == "status" or userInput[0] == "st" or userInput[0] == "s":
				print "Ye hath " + str(self.health) + " health points left."
				if enemy.HP < 3:
					print "The beastly " + enemy.name + " looks injured!"
				else:
					print "The damned " + enemy.name + " isn't showing any signs of fatigue!"
			elif userInput[0] == "run" or userInput[0] == "r":
				if self.SPD + random.randint(0,20) > enemy.SPD + random.randint(0,20):
					print "Ye escapeth! Thou art a pussy."
					return 1
				else:
					print "Thou art too slow this time!"
					self.beAttacked()
			if enemy.HP < 1:
				print "Ye bested the foul beast!"
				self.XP += enemy.LVL * (10 + random.randint(0,3))
				return 
			elif self.health < 1:
				print "Ye were bested by the foul beast.."
				return False

	def attack(self,enemy):
		print "Ye swing with ye mighty EQUIPPED WEAPON!"
		dmg = self.STR - enemy.DEF + random.randint(0,self.STR)
		if dmg < 1:
			dmg = 0
		print "Ye does a masive " + str(dmg) + " points of damage!"
		enemy.HP -= dmg
	def beAttacked(self,enemy): 
		print enemy.attack
		dmg = enemy.STR - self.DEF + random.randint(0,enemy.STR)
		if dmg < 1:
			dmg = 0
		print "The " + enemy.name + " does a massive " + str(dmg) + " points of damage!"

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
	userInput = userInput.lower()
	userInput = userInput.split()

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
	elif userInput[0] == 'fight' or userInput[0] == 'f':
		if player.area.enemy != 0:
			win = player.fight(player.area.enemy)
			if win == False:
				print "Thou art dead, thy corpse's anus ist being ransacked by a " + enemy.name + ". Ye hath made it's day."
				quit()
	elif userInput[0] == 'skillpoints' or userInput[0] == 'sp':
		if player.SP < 1:
			print "But player, ye have not the skill points to spare!"
		else:
			userInput = raw_input("Ye adventurer hath " + str(player.SP) + " skill points! Do ye wish to spend one on STR, DEF, SPD or MAG?\n")
			userInput = userInput.lower()
			if userInput == "str":
				player.STR += 1
				player.SP -= 1
				print "Arr, 'tis spent on STRENGTH!" 
			elif userInput == "def":
				player.DEF += 1
				player.SP -= 1
				print "Arr, 'tis spent on DEFENSE!" 
			elif userInput == "spd":
				player.SPD += 1
				player.SP -= 1
				print "Arr, 'tis spent on SPEED!" 
			elif userInput == "mag":
				player.MAG += 1
				player.SP -= 1
				print "Arr, 'tis spent on MAGICNESS!" 
			else:
				print "Urr, " + userInput + " is not a skill that ye can spend skill points on, Cap'n!"
			print "Ye scruvy dawg has but " + str(player.SP) + " skill point(s) left!"
			
	else:
		print "Uh oh! I can't find the command '" + userInput[0] + "', please enter another command."
	
	if player.health < 1:
		print "Oh dear, you've died."
		quit()
	elif player.XP > player.level * (50 + (player.level * 2)):
		print "Congratulations, thy adventurer hath leveled the fuck up- bitch!"
		player.level += 1
		player.SP += player.level
		print "Use 'SkillPoints' or 'SP' command to use your new skill points."
