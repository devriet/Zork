from abc import ABCMeta, abstractmethod

class Observer(object):
	# Basic observer class to be used
	# by the Player and Monster classes.
	__metaclass__ = ABCMeta

	@abstractmethod
	def update(self):
		pass

