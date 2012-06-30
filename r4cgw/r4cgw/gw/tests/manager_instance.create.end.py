import sys

sys.path.insert(0,'/home/ubuntu/cloud/r4cgw')
sys.path.insert(0,'/home/ubuntu/cloud')

from r4cgw.gw import manager


if __name__ == '__main__':

    body = {'_context_roles': ['admin'], '_context_request_id': 'req-f349193b-fecf-4144-90b8-d46725366f76', '_context_read_deleted': 'no', 'event_type': 'compute.instance.create.end', 'timestamp': '2012-06-07 23:17:45.429355', 'payload': {u'state_description': '', 'display_name': 'test', 'memory_mb': 512, 'disk_gb': 0, 'tenant_id': 'aa8ba720b73e47ffb9d3cc2afa97bb9d', 'created_at': '2012-06-07 23:17:26', 'instance_type_id': 2, 'instance_id': 'b42d1651-de2c-407f-8d81-ebfb24f02217', 'instance_type': 'm1.tiny', 'state': 'active', 'user_id': '5d6e2200d7a340cbac17251a94ef1b64', 'fixed_ips': [{'floating_ips': [], 'meta': {}, 'type': 'fixed', u'version': 4, 'address': '10.122.122.2'}], 'launched_at': '2012-06-07 23:17:45.283891', 'image_ref_url': 'http://10.76.0.119:9292/images/3ee737c2-cece-4f6d-9738-2bcba258ff98'}, '_context_auth_token': None, '_context_is_admin': True, '_context_project_id': None, '_context_timestamp': '2012-06-07T23:17:45.429386', '_context_user_id': None, '_context_remote_address': None, 'publisher_id': 'compute.vm-dev-1', 'message_id': '8547a107-5f68-4e70-ba04-9b4ff4bb70bb', 'priority': 'INFO'}
    m = manager.GwManager()
    m.gw_handler(body)
