from flask import flash
from xml.etree import ElementTree
from diagram.DiagramData import DiagramData
from diagram.FencingEntity import FencingEntity
import base64, zlib, urllib.parse, html

class DiagramParser:
	"""Parse fence diagrams"""

	def parse(compressedString):
		"""
		Parse the given compressed XML-SVG fence diagram
		Return the parsed data or None if parse failed
		"""
		try:
			return DiagramParser._parse(compressedString)
		
		except BaseException as e:
			flash("Error saving diagram", "danger")
			print(str(e))
			return None
		
		except:
			flash("Error saving diagram", "danger")
			return None
	
	def _initialDecode(string):
		# Slice to get rid of "data:image/svg+xml;base64,"
		return base64.b64decode(string[26:])

	def _decompress(compressedDiagramString):
		"""Decompress a compressed diagram string"""
		decoded = base64.b64decode(compressedDiagramString)
		decompressed = zlib.decompress(decoded, -8)
		decompressedString = decompressed.decode('utf-8')
		return urllib.parse.unquote(decompressedString)

	def _getShape(style):
		"""
		Given the value of the 'style' tag of an 'mxCell' element, return the
		value of the 'shape' portion or None if it is not found
		"""
		split = style.split(';')

		for item in split:

			if item.startswith('shape='):
				return item[6:]
		
		return None
	
	def _getRoot(compressedString):
		"""
		Given a compressed XML-SVG fence diagram, return the "root" element
		or None if not found
		"""
		string = DiagramParser._initialDecode(compressedString)
		svg = ElementTree.fromstring(string)
		
		content = svg.get('content')

		# If svg has no "content" attribute, return None
		if content is None:
			return None
		
		unescaped = html.unescape(content)
		mxfile = ElementTree.fromstring(unescaped)

		# If mxfile is not actually an 'mxfile' element, return None
		if mxfile.tag != 'mxfile':
			return None

		# If mxfile has no children, return None
		if len(mxfile) < 1:
			return None
		
		diagram = mxfile[0]

		# If diagram is not actually a 'diagram' element, return None
		if diagram.tag != 'diagram':
			return None
		
		graphModelString = DiagramParser._decompress(diagram.text)
		graphModel = ElementTree.fromstring(graphModelString)

		# If graphModel is not actually an 'mxGraphModel' element, return None
		if graphModel.tag != 'mxGraphModel':
			return None
		
		root = graphModel[0]

		# If root is not actually a 'root' element, return None
		if root.tag != 'root':
			return None
		
		return root

	def _parse(compressedString):
		"""
		Parse the given compressed XML-SVG fence diagram
		Return the parsed data or None if parse failed
		"""
		root = DiagramParser._getRoot(compressedString)

		if root is None:
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
			
			shape = DiagramParser._getShape(style)

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