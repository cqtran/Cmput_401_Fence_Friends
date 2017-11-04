class FencingEntity:
	"""A fencing entity (fence segment or gate)"""

	def __init__(self, entityType, length):
		self._entityType = entityType
		self._length = length
	
	def __str__(self):
		return str(self._length) + '" ' + self._entityType
	
	@property
	def entityType():
		return self._entityType

	@property
	def length():
		return self._length