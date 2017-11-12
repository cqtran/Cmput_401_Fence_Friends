from xml.etree import ElementTree
import base64, zlib, urllib.parse

class DiagramCompressor:
	"""Compress a diagram"""

	def compressWithRoot(svgElement, rootElement):
		"""Return a compressed diagram given its "svg" and "root" element"""

		ElementTree.register_namespace(
			"", "http://www.w3.org/2000/svg")

		rootString = ElementTree.tostring(rootElement,
			method='xml').decode('utf-8')
		
		# No whitespace so easier to compress
		diagram = """<mxGraphModel dx="717" dy="559" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" background="#ffffff" math="0" shadow="0">{root}</mxGraphModel>""".format(
			root=rootString)
		
		compressedDiagram = DiagramCompressor._compressDiagram(diagram)
		
		content = """<mxfile userAgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36" version="7.6.7" editor="www.draw.io"><diagram id="{id}" name="Page-1">{diagram}</diagram></mxfile>" style="background-color: rgb(255, 255, 255);""".format(
			id="diagram-1", diagram=compressedDiagram)
		
		DiagramCompressor._setSVGContent(svgElement, content)
		fullXML = ElementTree.tostring(svgElement,
			method='xml').decode('utf-8')
		
		return DiagramCompressor._finalEncode(fullXML)
	
	def _setSVGContent(svgElement, content):
		"""
		Set the value of the "content" attribute of the given "svg" element
		"""
		svgElement.set("content", content)
	
	def _compressDiagram(diagramString):
		"""Compress the "diagram" portion of an XML-SVG diagram string"""
		urlQuoted = urllib.parse.quote(diagramString)
		compressor = zlib.compressobj(level=9, wbits=-9)
		compressed = compressor.compress(str.encode(urlQuoted)) + \
			compressor.flush()
		return base64.b64encode(compressed).decode('utf-8')
	
	def _finalEncode(string):
		"""Encode an XML-SVG diagram string"""
		return "data:image/svg+xml;base64," + \
			base64.b64encode(str.encode(string)).decode('utf-8')