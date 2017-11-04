from xml.etree import ElementTree
from diagram.DiagramData import DiagramData
from diagram.FencingEntity import FencingEntity

class DiagramParser:
	"""Parse fence diagrams"""

	def getShape(style):
		"""
		Given the value of the 'style' tag of an 'mxCell' element, return the
		value of the 'shape' portion or None if it is not found
		"""

		split = style.split(';')

		for item in split:

			if item.startswith('shape='):
				return item[6:]
		
		return None

	def parse(fileName):
		"""
		Parse the given XML fence diagram file
		Return the parsed data or None if parse failed
		"""
		tree = ElementTree.parse(fileName)
		graphModel = tree.getroot()

		# If graphModel is not actually an 'mxGraphModel' element, return false
		if graphModel.tag != 'mxGraphModel':
			return None

		# If graphModel has no children, return false
		if len(graphModel) < 1:
			return None
		
		root = graphModel[0]

		# If root is not actually a 'root' element, return false
		if root.tag != 'root':
			return None

		data = DiagramData()

		for cell in root:

			# We are only dealing with 'mxCell' elements and their children
			if cell.tag != 'mxCell':
				continue
			
			style = cell.get('style')

			# We are only dealing with 'mxCell' elements that have styles
			if style is None:
				continue
			
			shape = DiagramParser.getShape(style)

			# We are only dealing with 'mxCell' elements that have shapes
			if shape is None:
				continue
			
			# We are only dealing with fencing shapes
			if not shape.startswith('mxgraph.fencing.'):
				continue
			
			shape = shape[16:]

			# We are only dealing with fence and gate shapes
			if shape != 'fence' and shape != 'gate':
				continue
			
			for geometry in cell:

				# We are only dealing with 'mxGeometry' child elements
				if geometry.tag != 'mxGeometry':
					continue
				
				widthString = geometry.get('width')

				# This element should have a width
				if widthString is None:
					return None
				
				width = int(widthString)
				
				if shape == 'fence':
					data.addFence(width)
				
				elif shape == 'gate':
					data.addGate(width)
		
		return data