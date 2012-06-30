

import keystone_client as client

u = 'dupa12345'

c = client.KeystoneAPIClient()
#r,b = c.keystone_admin_request(url='/tenants',method='GET')
r,b = c.create_tenant(u,'dupa')
i = b['tenant']['id']
r,b = c.create_user(u,'1234dupa1234',i)
i = b['user']['id']
print i
