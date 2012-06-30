
import keystone_mysql
import exc


k = keystone_mysql.KeystoneMySQL()
try:
	k.connect()
	tid = k.get_tenant_id_by_name('admin')
	uid = k.get_user_id_by_name('admin')
	k.close
except exc.KeystoneMySQL as err:
	print err
