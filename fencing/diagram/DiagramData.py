from diagram.FencingEntity import FencingEntity, Post
from diagram.PointMath import PointMath

class DiagramData:
	"""Data extracted from a fence diagram"""

	_maxPointDifference = 20.0

	def __init__(self):
		self._fences = []
		self._gates = []
		self.hasBuildings = False
	
	def __str__(self):
		strings = []

		for fence in self._fences:
			strings.append(str(fence))
		
		for gate in self._gates:
			strings.append(str(gate))
		
		for post in self.posts():
			strings.append(str(post))
		
		return str(strings)
	
	def __iter__(self):
		for fence in self._fences:
			yield fence
		
		for gate in self._gates:
			yield gate
		
		for post in self.posts():
			yield post
	
	def displayStrings(self):
		"""Return the items as they would be displayed to the user"""
		counts = {}
		strings = []

		for item in self:
			string = item.displayString()

			if string in counts:
				counts[string] += 1
			
			else:
				counts[string] = 1
		
		for string in counts:
			strings.append(str(counts[string]) + "× " + string)
		
		return strings
	
	@property
	def empty(self):
		if self.hasBuildings:
			return False

		return len(self._fences) == 0 and len(self._gates) == 0

	@property
	def fences(self):
		return self._fences
	
	@property
	def gates(self):
		return self._gates
	
	def _pointsClose(point1, point2):
		"""Return whether the given points are close"""
		return abs(point1[0] - point2[0]) <= DiagramData._maxPointDifference \
			and abs(point1[1] - point2[1]) <= DiagramData._maxPointDifference
	
	def _pointOnFence_(self, point, fence):
		"""Return whether the given point is on the given fence"""
		segmentPoint1 = (fence.x, fence.y)
		segmentPoint2 = (fence.x2, fence.y2)
		intersection = PointMath.perpendicularIntersection(point,
			segmentPoint1, segmentPoint2)

		if PointMath.pointInSegment(intersection, segmentPoint1,
			segmentPoint2):

			return DiagramData._pointsClose(point, intersection)
		
		return False
	
	def _pointOnFence(self, point):
		"""
		Return whether the given point is on a fence, but not at one of its ends
		"""
		for fence in self._fences:
			if DiagramData._pointsClose(point, (fence.x, fence.y)):
				continue
			
			if DiagramData._pointsClose(point, (fence.x2, fence.y2)):
				continue

			if self._pointOnFence_(point, fence):
				return True
		
		return False
	
	def posts(self):
		posts = self._posts()

		# Determine which posts are t posts
		for post in posts:
			if post.postType == "cornerPost":
				continue
			
			if self._pointOnFence(post.point):
				post.postType = "tPost"
		
		return posts
	
	def _posts(self):
		pointCounts = {}
		pointRemovals = set()

		for fence in self._fences:
			foundPoint1 = False
			foundPoint2 = False
			point1 = (fence.x, fence.y)
			point2 = (fence.x2, fence.y2)

			if fence.isRemoval:
				pointRemovals.add(point1)
				pointRemovals.add(point2)

			for p in pointCounts:
				if not foundPoint1 and DiagramData._pointsClose(point1, p):

					pointCounts[p] += 1
					foundPoint1 = True
				
				if not foundPoint2 and DiagramData._pointsClose(point2, p):

					pointCounts[p] += 1
					foundPoint2 = True
				
			if not foundPoint1:
				pointCounts[point1] = 1
				
			if not foundPoint2:
				pointCounts[point2] = 1
		
		posts = []
		
		for p in pointCounts:
			isRemoval = p in pointRemovals

			if pointCounts[p] > 1:
				posts.append(Post("cornerPost", p[0], p[1],
					isRemoval=isRemoval))
			
			else:
				posts.append(Post("endPost", p[0], p[1],
					isRemoval=isRemoval))
		
		return posts

	def addFence(self, length, height, x, y, rotation, isRemoval=False):
		self._fences.append(FencingEntity('fence', length, height, x, y,
			rotation, isRemoval=isRemoval))
	
	def addGate(self, length, height, x, y, rotation, isRemoval=False,
		isDouble=False):

		self._gates.append(FencingEntity('gate', length, height, x, y, rotation,
			isRemoval=isRemoval, isDouble=isDouble))