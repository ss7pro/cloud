from webob import Response
from webob import Request
from eventlet import wsgi
from paste.request import parse_formvars
import json

from nova import wsgi as base_wsgi

from r4capi import api


class router(base_wsgi.Router):

    @classmethod
    def factory(self,global_config, **local_config):
        return self.application

    @classmethod
    def application(self,environ,start_response):
        app = application(environ)
        app.run(environ)
        start_response(app.status,app.headers)
        return app.body

class application(object):

    status = '404 Not Found'
    headers = [('Content-type', 'application/json')]
    body = [json.dumps(dict(error=dict(msg='Not found.')))]
    tenant_id = None
    request_body = None

    def __init__(self,environ):
        self.api = api.api()
        self.tenant_id = environ['nova.context'].project_id
        pass

    def run(self,environ):
        req = Request(environ)
        self.route(req)

    def route(self,request):
        ctx = request.environ['nova.context']
        routes = self.create_routes(ctx)
        for route in routes:
            if request.path[0:len(route[0])] != route[0]:
                continue
            if request.method != route[1]:
                continue
            if request.content_type == 'application/json' and len(request.body):
                try:
                    self.request_body = json.loads(request.body)
                except:
                    self.status = '400 Bad Request'
                    self.body = json.dumps(dict(error=dict(msg=('Unable to '
                                                                'deserialize '
                                                                'JSON data'))))
                    break
            route[2](request)
            break

    def create_routes(self,ctx):
        if ctx.roles.count('FrontAdmin'):
            return self.create_admin_routes()
        else:
            return self.create_public_routes()

    def create_public_routes(self):
        routes = []
        routes.append(('/period/list', 'GET', self.period_list))
        routes.append(('/charge/list/period', 'GET', self.charge_period_list))
        routes.append(('/period/list', 'GET', self.period_list))
        return routes

    def create_admin_routes(self):
        routes = []
        routes.append(('/client/add', 'POST', self.client_add))
        routes.append(('/client/name/check', 'GET', self.client_name_check))
        return routes

    def call_api_func(self, param_names, func):
        params = self.build_params_from_body(param_names)
        resp, body = func(**params)
        self.status = resp['status']
        self.body = body

    def build_params_from_body(self, param_names):
        params = {}
        for param_name in param_names:
            if self.request_body is None:
                params[param_name] = None
            else:
                params[param_name] = self.request_body.get(param_name)
        return params

    def period_list(self, request):
        pass

    def charge_period_list(self, request):
        pass

    def client_add(self, request):
        param_names = ('client',)
        self.call_api_func(param_names, self.api.client_add)

    def client_name_check(self, request):
        print request.path
