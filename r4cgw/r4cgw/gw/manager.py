
from nova import flags
from nova import manager
from nova import log as logging
from nova import context

from r4c import utils
from r4cgw import rpc

from r4cbilling import db
from r4cbilling import Services

FLAGS = flags.FLAGS
LOG = logging.getLogger('nova.' + __name__)

class GwManager(manager.Manager):

    def __init__(self, *args, **kwargs):
        self.zone = 'r4cz1'
        super(GwManager, self).__init__(*args, **kwargs)

    def init_host(self):
        self.rpc_init()

    def rpc_init(self):
        self.connection = rpc.Connection(flags.FLAGS)
        self.connection.declare_topic_consumer(topic='notifications.info', callback=self.gw_handler)
        self.connection.consume_in_thread()
        print 'gotowe'

    def gw_handler(self,body):
        LOG.debug('NOTIFICATION: %s',str(body))
        if body.get('payload') is None:
            return
        p = body['payload']
        if (p.get('instance_type') is None or p.get('tenant_id') is None
            or p.get('instance_id') is None):
            return
        if body['event_type'] == 'compute.instance.create.end':
            if p.get('launched_at') is None:
                return
            self.compute_instance_create(p['instance_type'], p['instance_id'],
                                            p['tenant_id'], p['launched_at'])
        elif body['event_type'] == 'compute.instance.delete.start':
            if body.get('timestamp') is None:
                return
            self.compute_instance_delete(p['instance_type'], p['instance_id'],
                                            p['tenant_id'], body['timestamp'])

    def compute_instance_create(self, instance_type, instance_id, tenant_id,
                                launched_at):
        LOG.debug(('INSTANCE CREATE: %(instance_type)s, %(instance_id)s, '
                    '%(tenant_id)s, %(launched_at)s' %
                    dict(instance_type=instance_type, instance_id=instance_id,
                            tenant_id=tenant_id,
                            launched_at=launched_at)
                    ))
        self.register_instance(self.zone, instance_type, instance_id, tenant_id,
                                launched_at)

    def compute_instance_delete(self, instance_type, instance_id, tenant_id,
                                timestamp):
        LOG.debug(('INSTANCE TERMINATE: %(instance_type)s, %(instance_id)s, '
                    '%(tenant_id)s, %(timestamp)s' %
                    dict(instance_type=instance_type, instance_id=instance_id,
                            tenant_id=tenant_id,
                            timestamp=timestamp)
                    ))
        self.terminate_instance(self.zone, instance_type, instance_id,
                                tenant_id, timestamp)

    def register_instance(self, zone, instance_type, instance_id, tenant_id,
                            launched_at):
        dbs = db.Db()
        billingServices = Services.Services(dbs)
        resource = dict(name='instance', type=instance_type, id=instance_id, 
                            zone=zone)
        billingServices.register(tenant_id, resource,
                                    utils.mktime(launched_at)) 

    def terminate_instance(self, zone, instance_type, instance_id, tenant_id,
                            timestamp):
        dbs = db.Db()
        billingServices = Services.Services(dbs)
        resource = dict(name='instance', type=instance_type, id=instance_id, 
                            zone=zone)
        billingServices.terminate(tenant_id, resource,
                                    utils.mktime(timestamp)) 
