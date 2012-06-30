import sys

class Unauthorized(Exception):
	pass

class AuthorizationFailure(Exception):
	pass

class KeystoneMySQL(Exception):

	def __init__(self,where):
		self.where = where
		self.value = ('%s' % sys.exc_info()[1])
	def __str__(self):
		return 'where:' + self.where + ' msg: ' + self.value
