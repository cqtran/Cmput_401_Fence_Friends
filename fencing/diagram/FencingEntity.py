import math
from decimal import Decimal

# Used for rotations:
# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python/34374437#34374437
# Accessed November 17, 2017

class Post:
	"""A post"""

	def __init__(self, postType, x, y):
		self.postType = postType
		self._point = (x, y)
	
	def __str__(self):
		return self.postType
	
	def displayString(self):
		"""Return this item as it would be displayed to the user"""
		if self.postType == "cornerPost":
			return "Corner Post"

		if self.postType == "endPost":
			return "End Post"
		
		if self.postType == "tPost":
			return "T Post"
		
		print("Warning: unknown post type")
		return str(self)
	
	@property
	def point(self):
		return self._point

class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	_inchesInPoint = Decimal(10)

	def __init__(self, entityType, length, height, x, y, rotation,
		toRemove=False, double=False):

		if rotation is None:
			rotation = 0

		self._entityType = entityType
		self._length = length / FencingEntity._inchesInPoint
		length = float(length)
		self._x = FencingEntity._getX(x, y, length, height, rotation)
		self._y = FencingEntity._getY(x, y, length, height, rotation)
		self._x2 = FencingEntity._getX2(x, y, length, height, rotation)
		self._y2 = FencingEntity._getY2(x, y, length, height, rotation)
		self._toRemove = toRemove
		self._isDouble = double
	
	def __str__(self):
		entityType = self._entityType

		if self._isDouble:
			entityType = "double " + entityType
		
		if self._toRemove:
			entityType += " (remove)"

		return str(self._length) + '" ' + entityType
	
	def displayString(self):
		"""Return this item as it would be displayed to the user"""
		if self._entityType == "fence":
			string = "Fence"
		
		elif self._entityType == "gate":
			string = "Gate"
		
		else:
			print("Warning: unknown fencing attribute type")
			return str(self)
		
		if self._isDouble:
			string = "Double " + string
		
		string = self.lengthString() + " " + string
		
		if self._toRemove:
			string += " (To Remove)"
		
		return string
	
	@property
	def entityType(self):
		return self._entityType
	
	@property
	def length(self):
		return self._length
	
	def _getX(x, y, width, height, rotation):
		x0 = x + width / 2.0
		y0 = y + height / 2.0
		angle = math.radians(rotation)
		return x0 + math.cos(angle) * (x - x0) - math.sin(angle) * (y - y0)
	
	@property
	def x(self):
		return self._x
	
	def _getX2(x, y, width, height, rotation):
		x0 = x + width / 2.0
		y0 = y + height / 2.0
		x2 = x + width
		y2 = y + height
		angle = math.radians(rotation)
		return x0 + math.cos(angle) * (x2 - x0) - math.sin(angle) * (y2 - y0)

	@property
	def x2(self):
		return self._x2
	
	def _getY(x, y, width, height, rotation):
		x0 = x + width / 2.0
		y0 = y + height / 2.0
		angle = math.radians(rotation)
		return y0 + math.sin(angle) * (x - x0) + math.cos(angle) * (y - y0)
	
	@property
	def y(self):
		return self._y
	
	def _getY2(x, y, width, height, rotation):
		x0 = x + width / 2.0
		y0 = y + height / 2.0
		x2 = x + width
		y2 = y + height
		angle = math.radians(rotation)
		return y0 + math.sin(angle) * (x2 - x0) + math.cos(angle) * (y2 - y0)

	@property
	def y2(self):
		return self._y2
	
	@property
	def toRemove(self):
		return self._toRemove
	
	@property
	def isDouble(self):
		return self._isDouble
	
	def _inchesString(self):
		return str(int(self._length)) + '"'
	
	def _feetString(self):
		feet = self._length // 12
		inchesLeft = self._length % 12
		return str(int(feet)) + "'" + str(int(inchesLeft)) + '"'
	
	def lengthString(self):
		if self._entityType == "fence":
			return self._feetString()
		
		return self._inchesString()