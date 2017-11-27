from flask import flash
from xml.etree import ElementTree
from decimal import Decimal
from diagram.DiagramData import DiagramData
from diagram.FencingEntity import FencingEntity
import base64, zlib, urllib.parse, html, traceback

class DiagramParser:
	"""Parse fence diagrams"""

	def parse(compressedString):
		"""
		Parse the given compressed XML-SVG fence diagram
		Return the parsed data or None if parse failed
		"""
		try:
			return DiagramParser._parse(compressedString)
		
		except:
			flash("Error saving diagram", "danger")
			traceback.print_exc()
			return None
	
	def _initialDecode(string):
		# Slice to get rid of "data:image/svg+xml;base64,"
		return base64.b64decode(string[26:]).decode('utf-8')

	def _decompressDiagram(compressedDiagramString):
		"""Decompress a compressed diagram string"""
		decoded = base64.b64decode(compressedDiagramString)
		decompressed = zlib.decompress(decoded, -8)
		decompressedString = decompressed.decode('utf-8')
		return urllib.parse.unquote(decompressedString)

	def _getStyleValue(style, key):
		"""
		Given the value of the 'style' attribute of an 'mxCell' element, return
		the value of the given key in that attribute or None if it is not found
		"""
		split = style.split(';')

		for item in split:

			subSplit = item.split("=")

			if (len(subSplit) < 2):
				continue

			if subSplit[0].strip() == key:
				return subSplit[1].strip()
		
		return None
	
	def getSVG(compressedString):
		"""
		Given a compressed XML-SVG fence diagram, return the "svg" element
		"""
		string = DiagramParser._initialDecode(compressedString)
		return ElementTree.fromstring(string)
	
	def _getRoot(svgElement):
		"""
		Given the "svg" element of an XML-SVG fence diagram, return the "root"
		element or None if not found
		"""
		content = svgElement.get('content')

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
		
		graphModelString = DiagramParser._decompressDiagram(diagram.text)
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
		svg = DiagramParser.getSVG(compressedString)
		root = DiagramParser._getRoot(svg)

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
			
			shape = DiagramParser._getStyleValue(style, 'shape')
			isRemoval = DiagramParser._getStyleValue(style, 'dashed') == "1"

			# We are only dealing with 'mxCell' elements that have shapes
			if shape is None:
				continue
			
			# We are only dealing with fencing shapes
			if not shape.startswith('mxgraph.fencing.'):
				continue
			
			shape = shape[16:]

			if shape == 'building':
				data.hasBuildings = True
				continue
			
			rotationString = DiagramParser._getStyleValue(style, 'rotation')
			rotation = None

			if rotationString is not None:
				rotation = float(rotationString)
			
			for geometry in cell:

				# We are only dealing with 'mxGeometry' child elements
				if geometry.tag != 'mxGeometry':
					continue
				
				widthString = geometry.get('width')
				heightString = geometry.get('height')
				xString = geometry.get('x')
				yString = geometry.get('y')

				# This element should have these attributes
				if widthString is None or xString is None or yString is None:
					return None
				
				width = Decimal(widthString)
				height = float(heightString)
				x = float(xString)
				y = float(yString)
				
				if shape == 'fence':
					data.addFence(width, height, x, y, rotation,
						isRemoval=isRemoval)
				
				elif shape == 'gate':
					data.addGate(width, height, x, y, rotation,
						isRemoval=isRemoval)
				
				elif shape == 'double_gate':
					data.addGate(width, height, x, y, rotation,
						isRemoval=isRemoval, isDouble=True)
		
		return data