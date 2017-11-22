class PointMath:
	"""Math with points and lines"""

	# Taken from:
	# https://stackoverflow.com/questions/1811549/perpendicular-on-a-line-from-a-given-point/1811636#1811636
	# Accessed November 21, 2017
	def perpendicularIntersection(point, linePoint1, linePoint2):
		"""
		Return the point of intersection of the line that is perpendicular to
		the given line (defined by "linePoint1" and "linePoint2") and goes
		through "point"
		"""
		x1 = linePoint1[0]
		y1 = linePoint1[1]
		x2 = linePoint2[0]
		y2 = linePoint2[1]
		x3 = point[0]
		y3 = point[1]
		k = ((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2)
		x4 = x3 - k * (y2-y1)
		y4 = y3 + k * (x2-x1)
		return (x4, y4)
	
	def pointInSegment(point, segmentPoint1, segmentPoint2):
		"""
		Return whether the given point is on the given line segment (assuming it
		is on the line that extends from the line segment)
		"""
		x = point[0]
		y = point[1]

		if x < segmentPoint1[0] and x < segmentPoint2[0]:
			return False
		
		if x > segmentPoint1[0] and x > segmentPoint2[0]:
			return False
		
		if y < segmentPoint1[1] and y < segmentPoint2[1]:
			return False
		
		if y > segmentPoint1[1] and y > segmentPoint2[1]:
			return False
		
		return True