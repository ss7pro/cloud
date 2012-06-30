from webob import Response
from webob.dec import wsgify
from webob import exc as excweb
from paste.deploy import loadapp
import json
import keystone_client as client
import keystone_mysql
from eventlet import wsgi
import eventlet
import sys
import exc



def client_request(request,type):

	if not hasattr(request.body_file, 'read'):
		return dict(status='400'),json.dumps(dict(error=dict(msg='Unable to read body')))
	if request.headers['Content-Type'] != 'application/json':
		return dict(status='400'),json.dumps(dict(error=dict(msg='Wrong content type.')))

	try:
		b = json.loads(request.body)
	except:
		return dict(status='400'),json.dumps(dict(error=dict(msg='Unable to serialize JSON data')))

	return _client_request(request,b,type)


def _client_request(request,b,type):

	if type == 'add':
		return client_request_add(b)
	if type == 'check':
		return client_request_check(b)


def client_request_add(b):

	try:
		if (b['client']['name'] and b['client']['password']):
			return _client_add_request(b['client']['name'],b['client']['password'])
	except:
		return dict(status='400'),json.dumps(dict(error=dict(msg='Unable to find name and/or password.')))


def client_request_check(b):

	try:
		if (b['client']['name']):
			return _client_check_request(b['client']['name'])
	except:
		print sys.exc_info()
		return dict(status='400'),json.dumps(dict(error=dict(msg='Unable to check client name.')))

def _client_check_request(name):

	k = keystone_mysql.KeystoneMySQL()
	try:
		k.connect()
		tid = k.get_tenant_id_by_name(name)
		uid = k.get_user_id_by_name(name)
		k.close
		r = {}
		r['status'] = '200'
		b = {}
		if tid:
			b['tenantId'] = tid
		if uid:
			b['userId'] = uid
		b = json.dumps(b)
		del k
		return r,b
	except exc.KeystoneMySQL as err:
		del k
		return dict(status='400'),json.dumps(dict(error=dict(msg='Unable to find client name. error: %s' % err)))



def _client_add_request(name,password):

	r,b = _client_add_tenant(name)
	tenant_id = _get_tenant_id_from_response(r,b)
	if not tenant_id:
		b = json.dumps(b)
		return r,b
	r,b = _client_add_user(name,password,tenant_id)
	b = json.dumps(b)
	
	return r,b

def _client_add_tenant(name):

	c = client.KeystoneAPIClient()
	r,b = c.create_tenant(name,'Created by r4c-api')
	del c
	return r,b

def _client_add_user(name,password,tenant_id):

	c = client.KeystoneAPIClient()
	r,b = c.create_user(name,password,tenant_id)
	del c
	return r,b

def _get_tenant_id_from_response(r,b):

	if r.get('status') == '200':
		try:
			return b['tenant']['id']
		except:
			pass

@wsgify
def application(request):

	resp = Response()
	resp.headerlist = [('Content-type', 'application/json')]
	if request.method == 'POST':
		if request.path == '/client/add':
			r,b = client_request(request,'add')
			resp.status = r['status']
			resp.body =  b
		elif request.path == '/client/mod':
			pass
		elif request.path == '/client/del':
			pass
		elif request.path == '/client/check':
			r,b = client_request(request,'check')
			resp.status = r['status']
			resp.body =  b
		else:
			resp.status = 404
	else:
		resp.status = 404

	return resp
			

@wsgify.middleware
def auth_filter(request, app):

    if request.headers.get('X-Auth-Token') != 'VvpMBCV6x6WL087Q70wi2Lti0wkiNGoX':
        return excweb.HTTPForbidden()
    return app(request)


def app_factory(global_config, **local_config):
    return application


def filter_factory(global_config, **local_config):
    return auth_filter


wsgi_app = loadapp('config:' +  '/home/ubuntu/r4c-keystone/web.ini')

wsgi.server(eventlet.listen(('', 8090)),wsgi_app)
