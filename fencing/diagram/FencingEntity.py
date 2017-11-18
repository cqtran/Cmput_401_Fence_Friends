import math

class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	_inchesInPoint = 10

	def __init__(self, entityType, length, height, x, y, rotation,
		toRemove=False, double=False):

		self._entityType = entityType
		self._width = length
		self._length = length / FencingEntity._inchesInPoint
		self._height = height
		self._x = x
		self._y = y
		self._toRemove = toRemove
		self._isDouble = double

		if rotation is None:
			rotation = 0
		
		self._rotation = rotation
	
	def __str__(self):
		entityType = self._entityType

		if self._isDouble:
			entityType = "double " + entityType
		
		if self._toRemove:
			entityType += " (remove)"

		return str(self._length) + '" ' + entityType
	
	@property
	def entityType(self):
		return self._entityType
	
	@property
	def width(self):
		return self._width
	
	@property
	def length(self):
		return self._length
	
	@property
	def height(self):
		return self._height
	
	@property
	def x(self):
		x0 = self._x  + self._width / 2.0
		y0 = self._y + self._height / 2.0
		x = self._x
		y = self._y
		angle = math.radians(self._rotation)
		return x0 + math.cos(angle) * (x - x0) - math.sin(angle) * (y - y0)
	
	# Used:
	# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python/34374437#34374437
	# Accessed November 17, 2017
	@property
	def x2(self):
		x0 = self._x  + self._width / 2.0
		y0 = self._y + self._height / 2.0
		x2 = self._x + self._width
		y2 = self._y
		angle = math.radians(self._rotation)
		return x0 + math.cos(angle) * (x2 - x0) - math.sin(angle) * (y2 - y0)
	
	@property
	def y(self):
		x0 = self._x  + self._width / 2.0
		y0 = self._y + self._height / 2.0
		x = self._x
		y = self._y
		angle = math.radians(self._rotation)
		return y0 + math.sin(angle) * (x - x0) + math.cos(angle) * (y - y0)
	
	# Used:
	# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python/34374437#34374437
	# Accessed November 17, 2017
	@property
	def y2(self):
		x0 = self._x  + self._width / 2.0
		y0 = self._y + self._height / 2.0
		x2 = self._x + self._width
		y2 = self._y
		angle = math.radians(self._rotation)
		return y0 + math.sin(angle) * (x2 - x0) + math.cos(angle) * (y2 - y0)
	
	@property
	def rotation(self):
		return self._rotation
	
	@property
	def toRemove(self, toRemove):
		return self._isDouble
	
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