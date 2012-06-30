import sys

sys.path.insert(0,'/home/ubuntu/cloud/r4cgw')
sys.path.insert(0,'/home/ubuntu/cloud')

from r4cgw.gw import manager


if __name__ == '__main__':

    body = {u'_context_roles': [u'admin'], u'_context_request_id': u'req-7ca6de27-8074-4dd1-980d-20bb11ad053c', u'_context_read_deleted': u'no', u'event_type': u'compute.instance.delete.start', u'timestamp': u'2012-06-07 23:54:01.572687', u'payload': {u'state_description': u'deleting', u'display_name': u'test', u'memory_mb': 512, u'disk_gb': 0, u'tenant_id': u'aa8ba720b73e47ffb9d3cc2afa97bb9d', u'created_at': u'2012-06-07 23:17:26', u'instance_type_id': 2, u'instance_id': u'b42d1651-de2c-407f-8d81-ebfb24f02217', u'instance_type': u'm1.tiny', u'state': u'active', u'user_id': u'5d6e2200d7a340cbac17251a94ef1b64', u'launched_at': u'2012-06-07 23:17:45', u'image_ref_url': u'http://10.76.0.119:9292/images/3ee737c2-cece-4f6d-9738-2bcba258ff98'}, u'_context_auth_token': None, u'_context_is_admin': True, u'_context_project_id': None, u'_context_timestamp': u'2012-06-07T23:54:01.572714', u'_context_user_id': None, u'_context_remote_address': None, u'publisher_id': u'compute.vm-dev-1', u'message_id': u'dc32d581-eb9d-4f4f-b3ef-9d622ef4dd7f', u'priority': u'INFO'}
    m = manager.GwManager()
    m.gw_handler(body)
