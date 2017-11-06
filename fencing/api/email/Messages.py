class Messages:
	"""Generate email messages formatted with HTML"""

	def quote(project, customer):
		"""Generate a quote email"""
		return "<b>This is some bolded HTML text</b>"
	
	def materialList(project):
		"""Generate a material list email"""
		return """<h2>Steel</h2>
7 steel posts<br>
5 steel uchannel<br>
1 L steel<br>
<br>
<h2>Plastic Posts</h2>
1 corner<br>
4 line<br>
2 end<br>
1 blank<br>
<br>
<h2>Plastic</h2>
12 rails<br>
12 u channels<br>
46 T&G<br>
14 collars<br>
8 caps"""