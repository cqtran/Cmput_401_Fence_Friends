class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	_inchesInPoint = 10

	def __init__(self, entityType, length):
		self._entityType = entityType
		self._length = length / FencingEntity._inchesInPoint
	
	def __str__(self):
		return str(self._length) + '" ' + self._entityType
	
	@property
	def entityType():
		return self._entityType

	@property
	def length():
		return self._length