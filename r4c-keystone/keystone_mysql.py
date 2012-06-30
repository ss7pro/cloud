import MySQLdb
import sys
import exc


class KeystoneMySQL(object):

	def __init__(self):

		self.username = 'keystone'
		self.password = 'wJLMd13cSYCbHt8Hw5ICX8pgfzVOsf1g'
		self.host = '10.76.0.202'
		self.database = 'keystone'

	def connect(self):

		self.db = None

		try:
			self.db = MySQLdb.connect(host=self.host,user=self.username,passwd=self.password,db=self.database,connect_timeout=1)
		except:
			raise exc.KeystoneMySQL('connect')

		return self.db

	def close(self):

		try:
			self.db.close()
		except:
			raise exc.KeystoneMySQL('close')
			

	def get_tenant_id_by_name(self,name):

		try:
			c = self.db.cursor()
			c.execute('SELECT id FROM tenant WHERE name = %(name)s' , dict(name=name))
			if c.rowcount == 1:
				r = c.fetchone()[0]
			else:
				r = None
			c.close()
			return r
		except:
			raise exc.KeystoneMySQL('get_tenant_id_by_name')

	def get_user_id_by_name(self,name):

		try:
			c = self.db.cursor()
			c.execute('SELECT id FROM user WHERE name = %(name)s' , dict(name=name))
			if c.rowcount == 1:
				r = c.fetchone()[0]
			else:
				r = None
			c.close()
			return r
		except:
			raise exc.KeystoneMySQL('get_user_id_by_name')

