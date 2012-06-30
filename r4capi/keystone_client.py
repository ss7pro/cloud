import httplib2
import json
import sys

class KeystoneAPIClient(httplib2.Http):

    def __init__(self,timeout=1):

        self.username = 'admin'
        self.password = 'uBeiLaiw4aro'
        self.tenant = 'admin'
        self.admin_token = 'eev2Thie1imahn7fe1Onua7xohru0Oo6'
        self.auth_url = 'http://127.0.0.1:5000/v2.0'
        self.admin_auth_url = 'http://127.0.0.1:35357/v2.0'
        self.default_zone = 'r4cz1'
        self.keystone_headers = {}

        super(KeystoneAPIClient, self).__init__(timeout=timeout)
        self.force_exception_to_status_code = False
        self.disable_ssl_certificate_validation = True
        httplib2.debuglevel = 0


    def request(self,*args,**kwargs):

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = 'r4c-api'
        kwargs['headers']['Accept'] = 'application/json'
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'

# probujemy polaczy sie dwa razy
        for i in range(2): 
            try:
                resp, body = super(KeystoneAPIClient, self).request(*args, **kwargs)
            except:
                body = json.dumps(dict(error=dict(where='request',type='request error',msg=('%s' %sys.exc_info()[1]))))
                # sprobuj polaczyc sie jeszcze raz
                continue
            # udalo sie polaczyc
            i = 0
            break
        # jezeli i == 1 to nie udalo sie polaczyc do endpointa
        # dlatego ustawiamt status na 408 (request timeout)
        if i == 1:
            resp = dict(status='408')
        return resp, body

    def authenticate(self,username=None,password=None,tenant=None,
        auth_url=None):

        if not username:
            username = self.username
        if not password:
            password = self.password
        if not tenant:
            tenant = self.tenant
        if not auth_url:
            auth_url = self.auth_url

        return self._authenticate(username,password,tenant,auth_url)

    def _authenticate(self,username,password,tenant,auth_url):

        body = dict(auth=dict(passwordCredentials=dict(
            username=username,password=password),tenantName=tenant))
        return self.auth_request(auth_url,body)

    def auth_request(self,auth_url,auth_body):

        resp, resp_body = self._auth_request(auth_url,auth_body)
#
# jezeli 401 Not Authorized oddaj dalej bez zmian
#
        if resp.get('status') == '401':
            return resp, resp_body
        self.token = self.get_token(resp,resp_body)
#
# jezeli nie ma tokena, przekopiuj odpowiedz z keystone do
# keystone_resp,keystone_body i oddaj dalej
#
        if not self.token:
            return self.encapsulate_resp(resp,resp_body,where='auth_request',msg='Unable to find token.',status='502')

        return resp,resp_body
            

    def _auth_request(self,auth_url,auth_body):

        auth_body = json.dumps(auth_body)

        resp,resp_body = self.request(auth_url + '/tokens','POST',body=auth_body)
        # jezeli udalo sie nam polaczyc, deserializujemy jsona
        if resp.get('status') == '401':
            try:
                resp_body = json.loads(resp_body)
            except:
                # deserializacja nie udala sie, przekazujemy
                #  dalej do analizy
                resp_body = dict(resp_body=resp_body)

        return resp, resp_body


    def get_token(self,resp,body):

        try:

            r = body['access']['token']['id']

        except KeyError:
            return

        return r

    def encapsulate_resp(self,resp,body,where=None,msg=None,
        status=None):

        b = dict(error=dict(where=where,msg=msg,enc_resp=resp,
            enc_body=body))
        r = dict(status=status)
        return r,b


    def _keystone_admin_request(self,url=None,method=None,body=None):
        if not self.keystone_headers:
            self.keystone_headers['X-Auth-Token'] = self.admin_token
        return self.request(self.admin_auth_url + url,method,headers=self.keystone_headers,body=body)

    def keystone_admin_request(self,url=None,body=None,method=None):
        if body:
            try:
                body = json.dumps(body)
            except:
                return dict(status='400'),dict(error=dict(where='keystone_create_admin_request at: ' + url,msg='JSON serialization error',body=body))

        r,b = self._keystone_admin_request(url=url,method=method,body=body)

        return r,b


    def create_tenant(self,name,description):
        body = dict(tenant=dict(name=name,description=description,enabled=True))
        return self.keystone_admin_request(url='/tenants',body=body,method='POST')

    def create_user(self,name,password,tenant_id):
        body = dict(user=dict(name=name,password=password,tenantId=tenant_id,enabled=True))
        return self.keystone_admin_request(url='/users',body=body,method='POST')
