import math, html, base64
from xml.etree import ElementTree
from diagram.DiagramParser import DiagramParser

class DiagramLabels:
	"""Add length labels to a fence diagram"""

	# TLDR: magic
	# Length labels are added as SVG elements so they show up in SVG renderings
	# of the image. However, they are not added as part of the diagram (which
	# is embedded in the "svg" element as the value of its "content" attribute)
	# so they are ignored when draw.io loads them.
	def addLengthLabels(unparsed, parsed):
		"""
		Add length labels to a fence diagram and return the result or None if
		there was a problem
		"""
		svg = DiagramParser.getSVG(unparsed)
		g = DiagramLabels._getG(svg)
		
		for fencingEntity in parsed:
			rotation = fencingEntity.rotation
			x = fencingEntity.x
			y = fencingEntity.y
			x2 = (x + fencingEntity.rawLength) / 2.0
			x2 = x2 * math.cos(rotation) - y * math.sin(rotation)

			length = html.escape(fencingEntity.lengthString())

			lengthLabel = """<g transform="translate({x},{y})"><switch><foreignObject style="overflow:visible;" pointer-events="all" width="42" height="26" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 42px; white-space: normal; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">{length}</div></div></foreignObject><text x="{x}" y="{y}" fill="#000000" text-anchor="middle" font-size="12px" font-family="Helvetica">{length}</text></switch></g>""".format(
				length=length, x=x, y=y)

			g.append(ElementTree.fromstring(lengthLabel))
		
		ElementTree.register_namespace(
			"", "http://www.w3.org/2000/svg")
		
		xml = ElementTree.tostring(svg, method='xml').decode('utf-8')
		return DiagramLabels._encode(xml)
	
	def _encode(string):
		"""Encode an XML-SVG diagram string"""
		return "data:image/svg+xml;base64," + \
			base64.b64encode(str.encode(string)).decode('utf-8')

	def _getG(svg):
		"""
		Return the "g" element in the given "svg" element or None if not found
		"""
		for element in svg:
			if element.tag == "{http://www.w3.org/2000/svg}g":
				return element
		
		return None