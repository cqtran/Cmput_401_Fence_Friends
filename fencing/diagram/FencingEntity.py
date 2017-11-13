class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	_inchesInPoint = 10

	def __init__(self, entityType, length, x, y, rotation, double=False):
		self._entityType = entityType
		self._rawLength = length
		self._length = length / FencingEntity._inchesInPoint
		self._x = x
		self._y = y
		self._isDouble = double

		if rotation is None:
			rotation = 0
		
		self._rotation = rotation
	
	def __str__(self):
		entityType = self._entityType

		if self._isDouble:
			entityType = "double " + entityType

		return str(self._length) + '" ' + entityType
	
	@property
	def entityType(self):
		return self._entityType
	
	@property
	def rawLength(self):
		return self._rawLength
	
	@property
	def length(self):
		return self._length
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def rotation(self):
		return self._rotation
	
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