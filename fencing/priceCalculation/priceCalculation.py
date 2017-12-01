from decimal import Decimal

gstPercent = Decimal("5.00") / 100

def subtotal(prices):
	"""Return the subtotal of the given prices"""
	total = Decimal("0.00")

	for price in prices:
		total += price[1]

	return total