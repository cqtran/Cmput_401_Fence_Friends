class JsonDiagramData:
	"""Parsed diagram data as it is passed to the client"""

	def parse(diagramData):
		fences = []
		gates = []
		posts = []

		for fence in diagramData.fences:
			obj = {
				"length": str(fence.length),
				"isRemoval": fence.isRemoval
			}
			
			fences.append(obj)
		
		for gate in diagramData.gates:
			obj = {
				"length": str(gate.length),
				"isDouble": gate.isDouble,
				"isRemoval": gate.isRemoval
			}
			
			gates.append(obj)
		
		for post in diagramData.posts():
			obj = {
				"type": post.postType,
				"isRemoval": post.isRemoval
			}
			
			posts.append(obj)

		return [fences, gates, posts]