from decimal import Decimal

class QuoteCalculation:
	"""Calculate quote price"""

	def prices(parsed, appearance_value, removal_value, gate_single_value, gate_double_value):
		"""Return a list of pairs with each item's name and price"""
		prices = []

		for item in parsed:
			if item.entityType == "fence":
				prices.append(QuoteCalculation._fencePrice(item, appearance_value, removal_value))

			elif item.entityType == "gate":
				prices.append(QuoteCalculation._gatePrice(item, gate_single_value, gate_double_value, removal_value))

			# Not required?
			#elif item.entityType == "post":
				#prices.append(QuoteCalculation._postPrice(item))

		return prices

	def _fencePrice(fence, appearance_value, removal_value):
		if fence.isRemoval:
			return (fence.displayString(), removal_value * fence.length/12)

		else:
			return (fence.displayString(), appearance_value * fence.length/12)

	def _gatePrice(gate, gate_single_value, gate_double_value, removal_value):
		# ----> Eric: Gates have .isDouble if you need it

		# Not required?
		#if gate.isRemoval:
			#return (gate.displayString(), Decimal("0.25") * gate.length)

		if gate.isDouble:
			return (gate.displayString(), gate_double_value)

		else:
			return (gate.displayString(), gate_single_value)

	# Not currently in use
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
