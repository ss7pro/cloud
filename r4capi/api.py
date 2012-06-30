import uuid
import json

from r4capi import keystone_client

NODE = 0000000000001

class api(object):

    def __init__(self):
        pass

    @classmethod
    def error_bad_request(msg):
        return '400 Bad Request', json.dumps(dict(error=dict(msg=msg)))

    def client_add(self, client):
        def get_tenant_id_from_response(resp, body):
            try:
                body = json.loads(body)
            except:
                return self.error_bad_request(('Unable to deserialize body '
                                                'from keystone.'))
            if resp.get('status') != '200':
                return
            if body.get('tenant') is None:
                return
            if body['tenant'].get('id') is None:
                return
            return body['tenant']['id']
        if client.get('name') is None or client['name'] is None:
            return self.error_bad_request('Unable to find client name.')
        if client.get('password') is None or client['password'] is  None:
            return self.error_bad_request('Unable to find client password.')
        resp, body = self.new_tenant()
        tenant_id = get_tenant_id_from_response(resp, body)
        if tenant_id is None:
            return resp, body
        return self.new_user(client['name'], client['password'], tenant_id)

    def new_tenant(self):
        KeystoneAPI = keystone_client.KeystoneAPIClient()
        name = str(uuid.uuid1(NODE))
        r,b = KeystoneAPI.create_tenant(name,'Created by r4c-api')
        return r,b

    def new_user(self, name, password, tenant_id):
        KeystoneAPI = keystone_client.KeystoneAPIClient()
        return KeystoneAPI.create_user(name, password, tenant_id)

