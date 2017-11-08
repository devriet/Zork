from observer_pattern.Observer import Observer
from observer_pattern.Observable import Observable
import random

class Weapon(object):
	# This is the abstract data type for all Weapons.
	# It contains all of the data and performable actions for Weapons.
	def __init__(self, minmult, maxmult, uses):
		self.minmult = minmult
		self.maxmult = maxmult
		self.uses = uses

	def use(self):
		if type(self) != HersheyKiss:
			self.uses -= 1			
	
class HersheyKiss(Weapon):
	# A HersheyKiss has infinity uses.
	# It has a 1.0 multiplier.
	def __init__(self):
		super(Weapon, self).__init__(1.0,1.0, 1)

class SourStraw(Weapon):
	# A SourStraw has 2 uses.
	# It has a 1.0 - 1.75 multiplier.
	def __init__(self):
		super(Weapon, self).__init__(1.0, 1.75, 2)

class ChocolateBar(Weapon):
	# A ChocolateBar has 4 uses.
	# It has a 2.0 - 2.4 multiplier.
	def __init__(self):
		super(Weapon, self).__init__(2.0, 2.4, 4)

class NerdBomb(Weapon):
	# A NerdBomb has 1 use.
	# It has a 3.5 - 5.0 multiplier.
	def __init__(self):
		super(Weapon, self).__init__(3.5, 5.0, 1)

class Monster(Observable):
	# This is the abstract data type for all creatures.
	# It contains all of the data and performable actions for Monsters.
	def __init__(self, minattack, maxattack, health):
		self.minattack = minattack
		self.maxattack = maxattack
		self.health = health

	def attack(self, player):
		player.damage(random.randint(minattack, maxattack))

	def damage(self, player, weapon, hitpoints):
		if type(self) == Ghoul:
			if type(weapon) == NerdBomb:
				self.health -= 5*hitpoints
			else:
				self.health -= hitpoints
		else if type(self) == Zombie:
			if type(weapon) == SourStraw:
				self.health -= 2*hitpoints
			else:
				self.health -= hitpoints
		else if type(self) == Vampire:
			if type(weapon) != ChocolateBar:
				self.health -= hitpoints
		else if type(self) == Werewolf:
			if type(weapon) != ChocolateBar and type(weapon) != SourStraw:
				self.health -= hitpoints
		if self.health > 0:
			self.attack(player)
		else:
			self.update()

class Ghoul(Monster):
	# A Ghoul takes five times damage from NerdBombs.
	# It has 40 - 80 health and 15 - 30 attack.
	def __init__(self):
		super(Monster, self).__init__(15, 30, random.randint(40,80))

class Zombie(Monster):
	# A Zombie takes double damage from SourStraws.
	# It has 50 - 100 health and 0 - 10 attack.
	def __init__(self):
		super(Monster, self).__init__(0, 10, random.randint(50,100))

class Vampire(Monster):
	# A Vampire is immune to ChocolateBars.
	# It has 100 - 200 health and 10 - 20 attack.
	def __init__(self):
		super(Monster, self).__init__(10, 20, random.randint(100,200))

class Werewolf(Monster):
	# This is the strongest of all Monsters
	# A Werewolf is immune to both SourStraws and ChocolateBars.
	# It has 200 health and 0 - 40 attack.
	def __init__(self):
		super(Monster, self).__init__(0, 40, 200)

class Person(Monster):
	# This is an uninfected creature
	# A Person is immune to attacks and
	# heals one health instead of attacking
	def __init__(self):
		super(Monster, self).__init__(-1, -1, 100)

def randomMonster():
	# This function generates a random Monster.
	i = random.randint(0,4)
	if i == 0:
		return Werewolf()
	else if i == 1:
		return Vampire()
	else if i == 2:
		return Ghoul()
	else if i == 3:
		return Zombie()
	else
		return Person()

def randomWeapon():
	# This function generates a random Weapon,
	# other than a HersheyKiss.
	i = random.randint(0,2)
	if i == 0:
		return ChocolateBar()
	else if i == 1:
		return SourStraw()
	else:
		return NerdBomb()

class House(Observer):
	# This class contains all information for each house.
	# Each house contains a list of the monsters within,
	# as well as the number of infected and uninfected.
	def __init__(self):
		creatures = []
		humancount = 0
		monstercount = 0
		for i in range(random.randint(0,10)):
			creatures.append(randomMonster())
		for c in creatures:
			c.add_observer(self)
			if type(c) == Person:
				humancount += 1
			else:
				monstercount += 1
	
	def update(self):
		humancount += 1
		monstercount -= 1
		for c in creatures:
			if c.health <= 0:
				creatures.remove(c)
				creatures.append(Person())

class Neighborhood():
	# This is the place where the game story exists.
	# This contains all of the infected houses.
	def __init__(self, w, h):
		houses = []
		monstercount = 0
		humancount = 0
		for i in range(w):
			houses.append([])
			for j in range(h):
				houses[i].append(House())
				monstercount += houses[i][j].monstercount
				humancount += houses[i][j].humancount

class Player(Observable):
	# This class contains all of the playet data,
	# as well as inventory and actions to perform.
	def __init__(self):
		health = 120
		minattack = 10
		maxattack = 12
		candyBag = [HersheyKiss()]
		for i in range(9):
			candyBag.append(randomWeapon())

	def damage(self, hitpoints):
		health -= hitpoints
		if health <= 0:
			update()

	def attack(self, monsters, weapon):
		for m in monsters:
			monster.damage(self, weapon, random.randint(minattack, maxattack)*(random.random()*(weapon.maxmult-weapon.minmult)+weapon.minmult))
		weapon.use()

class Game(object):
	# This class contains all of the game logic required to run,
	# as well as instances of all other necessary classes.
	def __init__(self):
		neigh = Neighborhood(5,5)
		player = Player()
		player.add_observer(self)

	def update(self):
		print "GAME OVER!!!"




