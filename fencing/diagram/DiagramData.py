from diagram.FencingEntity import FencingEntity

class DiagramData:
	"""Data extracted from a fence diagram"""

	def __init__(self):
		self._fences = []
		self._gates = []
	
	def __str__(self):
		fenceStrings = ', '.join([str(fence) for fence in self._fences])
		gateStrings = ', '.join([str(gate) for gate in self._gates])

		if len(self._fences) > 0 and len(self._gates) > 0:
			return '[' + fenceStrings + ', ' + gateStrings + ']'
		
		elif len(self._fences) > 0:
			return '[' + fenceStrings + ']'
		
		elif len(self._gates) > 0:
			return '[' + gateStrings + ']'
		
		else:
			return '[]'
	
	@property
	def empty(self):
		return len(self._fences) == 0 and len(self._gates) == 0

	@property
	def fences(self):
		return self._fences
	
	@property
	def gates(self):
		return self._gates

	def addFence(self, length):
		self._fences.append(FencingEntity('fence', length))
	
	def addGate(self, length):
		self._gates.append(FencingEntity('gate', length))