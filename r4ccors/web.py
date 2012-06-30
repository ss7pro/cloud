from webob import Response
from webob.dec import wsgify
from paste.deploy import loadapp
from eventlet import wsgi
import eventlet
import sys


@wsgify
def application(request):


    resp = Response()
    print request.headers

    if request.headers.get('Access-Control-Request-Headers'):
        resp.headerlist.append(('Access-Control-Allow-Headers', 'origin,content-type,x-auth-token,accept,via,Server,X-Varnish,age'))
    if request.headers.get('Access-Control-Request-Method'):
        resp.headerlist.append(('Access-Control-Allow-Methods', request.headers['Access-Control-Request-Method']))
    resp.headerlist.append(('Content-Length', '0'))
    resp.headerlist.append(('Access-Control-Max-Age', '1728000'))
    resp.headerlist.append(('Access-Control-Allow-Origin', request.headers['Origin']))
    resp.status = 200

    return resp
            

@wsgify.middleware
def auth_filter(request, app):
    return app(request)


def app_factory(global_config, **local_config):
    return application


def filter_factory(global_config, **local_config):
    return auth_filter


wsgi_app = loadapp('config:' +  '/home/ubuntu/cloud/r4ccors/web.ini')

wsgi.server(eventlet.listen(('', 8095)), wsgi_app, keepalive=False)
