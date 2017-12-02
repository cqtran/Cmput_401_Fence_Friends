from decimal import Decimal
import os

_path = os.path.dirname(os.path.abspath(__file__)) + "/gst.txt"
_defaultGstPercent = Decimal("5.00") / 100

def updateGst(gst):
	with open(_path, "w") as gstFile:
		gstFile.write(str(Decimal(gst) / Decimal("100")))

def priceString(price):
	if isinstance(price, int):
		price = Decimal(price)

	return str(price.quantize(Decimal("0.01")))

def subtotal(prices):
	"""Return the subtotal of the given prices"""
	total = Decimal("0.00")

	for price in prices:
		total += price[1]

	return total

def gstPercent():
	try:
		with open(_path, "r") as gstFile:
			line = gstFile.readline()
		
		return Decimal(line.strip())
	
	except:
		return _defaultGstPercent
