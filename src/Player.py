from trueskill import Rating 

class Player(object):
	name = None
	rating = None

	def __init__(self, name='NULL', rating=None):
		self.name = name
		self.rating = rating

	def toDict(self):
		res = {} 

		res['name'] = self.name
		res['mu'] = self.rating.mu	# MMR
		res['sigma'] = self.rating.sigma	# system certainty

	def __str__(self):
		return "{0} MMR: {1} Certainty: {2}".format(self.name, self.rating.mu, self.rating.sigma)
