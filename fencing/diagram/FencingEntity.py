class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	_inchesInPoint = 10

	def __init__(self, entityType, length, toRemove=False, double=False):
		self._entityType = entityType
		self._length = length / FencingEntity._inchesInPoint
		self._toRemove = toRemove
		self._isDouble = double
	
	def __str__(self):
		entityType = self._entityType

		if self._isDouble:
			entityType = "double " + entityType
		
		if self._toRemove:
			entityType += " (remove)"

		return str(self._length) + '" ' + entityType
	
	@property
	def toRemove(self, toRemove):
		return self._isDouble
	
	@property
	def isDouble(self):
		return self._isDouble
	
	@property
	def entityType(self):
		return self._entityType

	@property
	def length(self):
		return self._length