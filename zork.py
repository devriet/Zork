from observer_pattern.Observer import Observer
from observer_pattern.Observable import Observable
import random

class Weapon(object):
	# This is the abstract data type for all Weapons.
	# It contains all of the data and performable actions for Weapons.
	def __init__(self, minmult, maxmult, uses, name):
		self.minmult = minmult
		self.maxmult = maxmult
		self.uses = uses
		self.name = name

	def use(self):
		if type(self) != HersheyKiss:
			self.uses -= 1

	def getName(self):
		return self.name

	def __str__(self):
		return self.name
	
	def getMin(self):
		return self.minmult
	
	def getMax(self):
		return self.maxmult

	def getUses(self):
		return self.uses
	
class HersheyKiss(Weapon):
	# A HersheyKiss has infinity uses.
	# It has a 1.0 multiplier.
	def __init__(self):
		super(HersheyKiss, self).__init__(1.0,1.0, 1, "Hershey Kiss")

class SourStraw(Weapon):
	# A SourStraw has 2 uses.
	# It has a 1.0 - 1.75 multiplier.
	def __init__(self):
		super(SourStraw, self).__init__(1.0, 1.75, 2, "Sour Straw")

class ChocolateBar(Weapon):
	# A ChocolateBar has 4 uses.
	# It has a 2.0 - 2.4 multiplier.
	def __init__(self):
		super(ChocolateBar, self).__init__(2.0, 2.4, 4, "Chocolate Bar")

class NerdBomb(Weapon):
	# A NerdBomb has 1 use.
	# It has a 3.5 - 5.0 multiplier.
	def __init__(self):
		super(NerdBomb, self).__init__(3.5, 5.0, 1, "Nerd Bomb")

class Monster(Observable):
	# This is the abstract data type for all creatures.
	# It contains all of the data and performable actions for Monsters.
	def __init__(self, minattack, maxattack, health, name):
		self.minattack = minattack
		self.maxattack = maxattack
		self.health = health
		self.name = name
		super(Monster, self).__init__()
		if type(self) == Ghoul:
			self.toString = "Ghoul"
		elif type(self) == Vampire:
			self.toString = "Vampire"
		elif type(self) == Zombie:
			self.toString = "Zombie"
		elif type(self) == Werewolf:
			self.toString = "Werewolf"
		else:
			self.toString = "Person"

	def getName(self):
		return self.name

	def __str__(self):
		return self.name

	def attack(self, player):
		player.damage(random.randint(self.minattack, self.maxattack), self)

	def getHealth(self):
		return self.health

	def getMin(self):
		return self.minattack

	def getMax(self):
		return self.maxattack

	def damage(self, player, weapon, hitpoints):
		hitpoints = int(hitpoints)
		if type(self) == Ghoul:
			if type(weapon) == NerdBomb:
				hitpoints = 5*hitpoints
			self.health -= hitpoints
		elif type(self) == Zombie:
			if type(weapon) == SourStraw:
				hitpoints = 2*hitpoints
			self.health -= hitpoints
		elif type(self) == Vampire:
			if type(weapon) == ChocolateBar:
				hitpoints = 0
			self.health -= hitpoints
		elif type(self) == Werewolf:
			if type(weapon) == ChocolateBar or type(weapon) == SourStraw:
				hitpoints = 0
			self.health -= hitpoints
		else:
			hitpoints = 0
		print self.toString + " takes " + str(hitpoints) + " damage."
		if self.health > 0:
			self.attack(player)
		else:
			print self.toString + " has died."
			player.addWeapon()
			self.update()

class Ghoul(Monster):
	# A Ghoul takes five times damage from NerdBombs.
	# It has 40 - 80 health and 15 - 30 attack.
	def __init__(self):
		super(Ghoul, self).__init__(15, 30, random.randint(40,80), "Ghoul")

class Zombie(Monster):
	# A Zombie takes double damage from SourStraws.
	# It has 50 - 100 health and 0 - 10 attack.
	def __init__(self):
		super(Zombie, self).__init__(0, 10, random.randint(50,100), "Zombie")

class Vampire(Monster):
	# A Vampire is immune to ChocolateBars.
	# It has 100 - 200 health and 10 - 20 attack.
	def __init__(self):
		super(Vampire, self).__init__(10, 20, random.randint(100,200), "Vampire")

class Werewolf(Monster):
	# This is the strongest of all Monsters
	# A Werewolf is immune to both SourStraws and ChocolateBars.
	# It has 200 health and 0 - 40 attack.
	def __init__(self):
		super(Werewolf, self).__init__(0, 40, 200, "Werewolf")

class Person(Monster):
	# This is an uninfected creature
	# A Person is immune to attacks and
	# heals one health instead of attacking
	def __init__(self):
		super(Person, self).__init__(-20, -10, 100, "Person") #TODO: Change back

def randomMonster():
	# This function generates a random Monster.
	i = random.randint(0,4)
	if i == 0:
		return Werewolf()
	elif i == 1:
		return Vampire()
	elif i == 2:
		return Ghoul()
	elif i == 3:
		return Zombie()
	else:
		return Person()

def randomWeapon():
	# This function generates a random Weapon,
	# other than a HersheyKiss.
	i = random.randint(0,2)
	if i == 0:
		return ChocolateBar()
	elif i == 1:
		return SourStraw()
	else:
		return NerdBomb()

class House(Observer):
	# This class contains all information for each house.
	# Each house contains a list of the monsters within,
	# as well as the number of infected and uninfected.
	def __init__(self, n):
		super(House, self).__init__()
		self.creatures = []
		self.humancount = 0
		self.monstercount = 0
		for i in range(random.randint(0,10)):
			self.creatures.append(randomMonster())
		for c in self.creatures:
			c.add_observer(self)
			c.add_observer(n)
			if type(c) == Person:
				self.humancount += 1
			else:
				self.monstercount += 1
	
	def getHumanCount(self):
		return self.humancount

	def getMonsterCount(self):
		return self.monstercount

	def getMonsters(self):
		return self.creatures

	def update(self):
		self.humancount += 1
		self.monstercount -= 1
		for c in self.creatures:
			if c.health <= 0:
				self.creatures[self.creatures.index(c)] = Person()

class Neighborhood(Observer):
	# This is the place where the game story exists.
	# This contains all of the infected houses.
	def __init__(self, w, h):
		self.houses = []
		self.monstercount = 0
		self.humancount = 0
		for i in range(w):
			self.houses.append([])
			for j in range(h):
				self.houses[i].append(House(self))
				self.monstercount += self.houses[i][j].getMonsterCount()
				self.humancount += self.houses[i][j].getHumanCount()

	def update(self):
		self.humancount += 1
		self.monstercount -= 1

	def getHouses(self):
		return self.houses

	def getHumanCount(self):
		return self.humancount

	def getMonsterCount(self):
		return self.monstercount

class Player(Observable):
	# This class contains all of the player data,
	# as well as inventory and actions to perform.
	def __init__(self):
		super(Player, self).__init__()
		self.xloc = 0
		self.yloc = 0
		self.health = 120
		self.minattack = 15 #TODO: Change back
		self.maxattack = 20 #TODO: Change back
		self.candyBag = [HersheyKiss()]
		for i in range(9):
			self.candyBag.append(randomWeapon())

	def getHealth(self):
		return self.health

	def getMin(self):
		return self.minattack

	def getMax(self):
		return self.maxattack

	def getCandy(self):
		return self.candyBag

	def getX(self):
		return self.xloc

	def getY(self):
		return self.yloc

	def setX(self, val):
		self.xloc = val

	def setY(self, val):
		self.yloc = val

	def addWeapon(self):
		if len(self.candyBag) < 10:
			self.candyBag.append(randomWeapon())
			a = self.candyBag[len(self.candyBag)-1]
			print "You got a " + str(a)

	def damage(self, hitpoints, monster):
		print monster.toString + " deals " + str(hitpoints) + " damage."
		self.health -= hitpoints
		if self.health <= 0:
			print "You have died!"
			self.update()

	def attack(self, monsters, weapon):
		run = False
		if weapon == "sourstraw":
			for c in self.candyBag:
				if type(c) == SourStraw:
					weapon = c
					run = True
		elif weapon == "chocolatebar":
			for c in self.candyBag:
				if type(c) == ChocolateBar:
					weapon = c
					run = True
		elif weapon == "nerdbomb":
			for c in self.candyBag:
				if type(c) == NerdBomb:
					weapon = c
					run = True
		else:
			for c in self.candyBag:
				if type(c) == HersheyKiss:
					weapon = c
					run = True
		if run:
			if len(monsters) >= 1:
				i = 0
				for m in monsters:
					if self.health > 0:
						m.damage(self, weapon,
							random.randint(self.minattack,
								self.maxattack)
							*(random.random()
							*(weapon.getMax()-
								weapon.getMin())
							+weapon.getMin()))
				weapon.use()
				if weapon.getUses == 0:
					self.candyBag.remove(weapon)
			else:
				print "There are no monsters to attack at this location."
		else:
			print "You have no available " + weapon + " to use."

class Game(Observer):
	# This class contains all of the game logic required to run,
	# as well as instances of all other necessary classes.
	def __init__(self):
		super(Game, self).__init__()
		while True:
			self.w = input("Enter the desired neighborhood width: ")
			self.h = input("Enter the desired neighborhood height: ")
			if type(self.w) == int and type(self.h) == int:
				break
			if type(self.w) != int:
				print "Invalid width: " + str(self.w)
			if type(self.h) != int:
				print "Invalid height: " + str(self.h)
		self.running = True
		print "Game beginning..."
		print "The neighborhood is " + str(self.h) + " houses by " + str(self.w) + " houses."
		print "There are " + str(self.h*self.w) + " houses in total."
		self.neigh = Neighborhood(self.h,self.w)
		self.player = Player()
		self.player.add_observer(self)
		print "There are " + str(self.neigh.getMonsterCount()) + " monsters in the neighborhood,"
		print "and " + str(self.neigh.getHumanCount()) + " people in the neighborhood."
		print "Your candy bag contains: "
		print self.showCandyBag()
		while self.running:
			inp = raw_input("What would you like to do? ")
			inputs = inp.split()
			if len(inputs) >=1:
				if len(inputs) == 1:
					inputs.append("")
				if inputs[0] == "quit":
					self.update()
				elif inputs[0] == "move":
					self.move(inputs[1])
				elif inputs[0] == "show":
					self.show(inputs[1])
				elif inputs[0] == "use":
					self.use(inputs[1])
				elif inputs[0] == "help":
					self.showHelp(inputs[1])
				else:
					print "Invalid input: " + str(inp)
			else:
				print "Invalid input."

	def update(self):
		print "GAME OVER!!!"
		self.running = False

	def showHelp(self, toShow):
		toShow = toShow.lower()
		if toShow == "":
			print "The possible commands to use are: {help, use, show, move, quit}."
			print "The help command can be used to show additional information about a command."
			print "Usage:\thelp <command>\n\twhere <command> = {use, show, move}"
		elif toShow == "use":
			print "The use command uses a candy from the candy bag to attack all of the creatures in the house."
			print "Usage:\tuse <candy>\n\twhere <candy> = {hersheykiss, sourstraw, chocolatebar, nerdbomb}"
		elif toShow == "show":
			print "The show command show information about a certain part of the game."
			print "Usage:\tshow <item>\n\twhere <item> = {candybag, house, status, me}"
		elif toShow == "move":
			print "The move function allows you to move throughout the neighborhood (game board)."
			print "Usage:\tmove <direction>\n\twhere <direction> = {left, right, up, down}"
		else:
			print "Invalid help option: " + toShow

	def use(self, toUse):
		if toUse.lower() == "hersheykiss" or toUse.lower() == "sourstraw" or toUse.lower() == "chocolatebar" or toUse.lower() == "nerdbomb":
			self.player.attack(self.neigh.getHouses()[self.player.getX()][self.player.getY()].getMonsters(), toUse.lower())
			if self.neigh.getMonsterCount() == 0:
				self.running = False
				print "You win!!!"
		else:
			print "Invalid candy weapon: " + toUse

	def show(self, toView):
		if toView.lower() == "candybag":
			self.showCandyBag()
		elif toView.lower() == "house":
			self.showHouse(self.neigh.getHouses()[self.player.getX()][self.player.getY()])
		elif toView.lower() == "status":
			self.showStatus()
		elif toView.lower() == "me":
			self.showMe()
		else:
			print "Cannot show: \"" + toView + "\""

	def move(self, direction):
		if direction == "left":
			if self.player.getX() == 0:
				print "There is no room to move left. You are at the edge of the neighborhood."
			else:
				self.player.setX(self.player.getX()-1)
				print "You have moved left to (" + str(self.player.getX()) + ",  " + str(self.player.getY()) + ")."
		elif direction == "right":
			if self.player.getX() == self.w-1:
				print "There is no room to move right. You are at the edge of the neighborhood."
			else:
				self.player.setX(self.player.getX()+1)
				print "You have moved right to (" + str(self.player.getX()) + ", " + str(self.player.getY()) + ")."
		elif direction == "up":
			if self.player.getY() == 0:
				print "There is no room to move up. You are at the edge of the neighborhood."
			else:
				self.player.setY(self.player.getY()-1)
				print "You have moved up to (" + str(self.player.getX()) + ", " + str(self.player.getY()) + ")."
		elif direction == "down":
			if self.player.getY() == self.h-1:
				print "There is no room to move down. You are at the edge of the neighborhood."
			else:
				self.player.setY(self.player.getY()+1)
				print "You have moved down to (" + str(self.player.getX()) + ", " + str(self.player.getY()) + ")."
		else:
			print "Invalid move direction: " + str(direction)

	def showCandyBag(self):
		print "Item    \tUses\tMin multiplier\tMax multiplier"
		for c in self.player.getCandy():
			print c.getName() + "\t" + str( c.getUses() ) + "\t" + str(c.getMin()) + "\t\t" + str(c.getMax())

	def showHouse(self, house):
		print "X\tY\tMonsters\tPersons"
		print str(self.player.getX()) + "\t" + str(self.player.getY()) + "\t" + str(house.getMonsterCount()) + "\t\t" + str(house.getHumanCount()) + "\n"
		print "Monster\t\tHealth\tMin Attack\tMax Attack"
		for m in house.creatures:
			print m.getName() + "   \t" + str(m.getHealth()) + "\t" + str(m.getMin()) + "\t\t" + str(m.getMax())

	def showStatus(self):
		print "Width\tHeight\tTotal Houses\tTotal Monsters\tTotal People"
		print str(self.w) + "\t" + str(self.h) + "\t" + str(self.w*self.h) + "\t\t" + str(self.neigh.getMonsterCount()) + "\t\t" + str(self.neigh.getHumanCount())

	def showMe(self):
		print "Health\tMin Attack\tMax Attack"
		print str(self.player.getHealth()) + "\t" + str(self.player.getMin()) + "\t\t" + str(self.player.getMax())

Game()

