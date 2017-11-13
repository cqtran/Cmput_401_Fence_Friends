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

		if g is None:
			g = svg
		
		for fencingEntity in parsed:
			x = fencingEntity.x
			y = fencingEntity.y + fencingEntity.height - 12

			length = html.escape(fencingEntity.lengthString())

			lengthLabel = """<g transform="translate({x},{y})"><foreignObject style="overflow:visible;" pointer-events="all" width="58" height="12"><div xmlns="http://www.w3.org/1999/xhtml" style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; vertical-align: top; width: 60px; white-space: nowrap; word-wrap: normal; text-align: center;"><div xmlns="http://www.w3.org/1999/xhtml" style="display:inline-block;text-align:inherit;text-decoration:inherit;background-color:#ffffff;">{length}</div></div></foreignObject></g>""".format(
				length=length, x=x, y=y)

			g.append(ElementTree.fromstring(lengthLabel))
		
		# So labels are not cropped off
		DiagramLabels._addPadding(svg, 50)

		ElementTree.register_namespace(
			"", "http://www.w3.org/2000/svg")
		
		xml = ElementTree.tostring(svg, method='xml').decode('utf-8')
		return DiagramLabels._encode(xml)
	
	def _addPadding(svgElement, pixels):
		"""Add padding to the given SVG image"""
		oldWidth = int(svgElement.get("width")[:-2])
		oldHeight = int(svgElement.get("height")[:-2])
		newWidth = oldWidth + pixels
		newHeight = oldHeight + pixels
		svgElement.set("width", str(newWidth) + "px")
		svgElement.set("height", str(newHeight) + "px")
	
	def _getG(svg):
 		"""
 		Return the "g" element in the given "svg" element or None if not found
 		"""
 		for element in svg:
 			if element.tag == "g" or \
			 	element.tag == "{http://www.w3.org/2000/svg}g":

 				return element
 		
 		return None
	
	def _encode(string):
		"""Encode an XML-SVG diagram string"""
		return "data:image/svg+xml;base64," + \
			base64.b64encode(str.encode(string)).decode('utf-8')