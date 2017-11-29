from decimal import Decimal

class MaterialListCalculation:
	"""Calculate material list price"""

	def prices(parsed, appearance):
		"""Return a list of pairs with each item's name and price"""
		prices = []

		for item in parsed:
			if item.entityType == "fence":
				prices.append(MaterialListCalculation._fencePrice(item))
			
			elif item.entityType == "gate":
				prices.append(MaterialListCalculation._gatePrice(item))
			
			elif item.entityType == "post":
				prices.append(MaterialListCalculation._postPrice(item))

		return prices
	
	def _fencePrice(fence):
		if fence.isRemoval:
			return (fence.displayString(), Decimal("0.50") * fence.length,
				"Plastic")
		
		else:
			return (fence.displayString(), Decimal("1.00") * fence.length,
				"Steel")
	
	def _gatePrice(gate):
		if gate.isRemoval:
			return (gate.displayString(), Decimal("0.25") * gate.length,
				"Plastic")
		
		else:
			return (gate.displayString(), Decimal("0.75") * gate.length,
				"Steel")
	
	def _postPrice(post):
		if post.isRemoval:
			if post.postType == "endPost":
				return (post.displayString(), Decimal("1.00"),
					"Plastic")
			
			elif post.postType == "cornerPost":
				return (post.displayString(), Decimal("2.00"),
					"Steel")
			
			elif post.postType == "tPost":
				return (post.displayString(), Decimal("3.00"),
					"Plastic")
		
		else:
			if post.postType == "endPost":
				return (post.displayString(), Decimal("4.00"),
					"Steel")
			
			elif post.postType == "cornerPost":
				return (post.displayString(), Decimal("5.00"),
					"Plastic")
			
			elif post.postType == "tPost":
				return (post.displayString(), Decimal("6.00"),
					"Steel")

		return ("Unknown item", Decimal("0.00"), "Other")