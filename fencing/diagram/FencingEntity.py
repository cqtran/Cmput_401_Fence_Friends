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
		return self._x
	
	@property
	def x2(self):
		x = self._x
		y = self._y
		rotation = self._rotation
		return x * math.cos(rotation) - y * sin(rotation)
	
	@property
	def y(self):
		return self._y
	
	@property
	def y2(self):
		x = self._x
		y = self._y
		rotation = self._rotation
		return y * math.cos(rotation) + x * math.sin(rotation)
	
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