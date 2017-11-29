from decimal import Decimal

def subtotal(prices):
	"""Return the subtotal of the given prices"""
	total = Decimal("0.00")

	for price in prices:
		total += price[1]
		
	return total