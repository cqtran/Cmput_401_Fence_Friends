from decimal import Decimal

class QuoteCalculation:
	"""Calculate quote price"""

	def prices(parsed, appearance):
		"""Return a list of pairs with each item's name and price"""
		prices = []

		for item in parsed:
			if item.entityType == "fence":
				prices.append(QuoteCalculation._fencePrice(item))
			
			elif item.entityType == "gate":
				prices.append(QuoteCalculation._gatePrice(item))
			
			elif item.entityType == "post":
				prices.append(QuoteCalculation._postPrice(item))

		return prices
	
	def _fencePrice(fence):
		if fence.isRemoval:
			return (fence.displayString(), Decimal("0.50") * fence.length)
		
		else:
			return (fence.displayString(), Decimal("1.00") * fence.length)
	
	def _gatePrice(gate):
		# ----> Eric: Gates have .isDouble if you need it

		if gate.isRemoval:
			return (gate.displayString(), Decimal("0.25") * gate.length)
		
		else:
			return (gate.displayString(), Decimal("0.75") * gate.length)
	
	def _postPrice(post):
		if post.isRemoval:
			if post.postType == "endPost":
				return (post.displayString(), Decimal("1.00"))
			
			elif post.postType == "cornerPost":
				return (post.displayString(), Decimal("2.00"))
			
			elif post.postType == "tPost":
				return (post.displayString(), Decimal("3.00"))
		
		else:
			if post.postType == "endPost":
				return (post.displayString(), Decimal("4.00"))
			
			elif post.postType == "cornerPost":
				return (post.displayString(), Decimal("5.00"))
			
			elif post.postType == "tPost":
				return (post.displayString(), Decimal("6.00"))

		return ("Unknown item", Decimal("0.00"))