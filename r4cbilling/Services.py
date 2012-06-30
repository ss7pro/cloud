from r4cbilling import Tenants
from r4cbilling import Resources
from r4cbilling import ServiceEvents


class Services(object):

    def __init__(self,db):
        self.db = db

    def register(self,TenantId,resource,created,dropped=None,size=None):
        self.db.begin()
        self.ensure_tenant(TenantId)
        resource['type'] = self.get_resource_type(resource)
        sid = self.add(TenantId,resource,created,dropped)
        self.add_service_to_charge_queue(sid,resource,created,size=size)
        self.db.commit()

    def ensure_tenant(self,TenantId):
        t = Tenants.Tenants(self.db)
        t.ensure(TenantId)

    def get_resource_type(self,resource):
        r = Resources.Resources(self.db)
        rt = r.get_resource_type(resource['name'],resource['type'],
                                        resource['zone'])
        return rt

    def add(self,TenantId,resource,created,dropped):
        return self.db.service_add(TenantId,resource['type']['id'],
                            resource['id'],created,dropped)


    def add_service_to_charge_queue(self,sid,resource,created,size=None):
        r = Resources.Resources(self.db)
        se = ServiceEvents.ServiceEvents(self.db)
        if size is None:
            size = 1
        for rcs in r.get_charge_schema(resource['type']['charge_schema_name']):
            if (rcs['type'] == 'main' and rcs['area'] == 'hours'):
                se.addEvent(sid,rcs['id'],created,'start',size)
            self.db.add_charge_queue(sid,rcs['id'],created,None)

    def terminate(self,TenantId,resource,dropped=None,size=None):
        self.db.begin()
        resource['type'] = self.get_resource_type(resource)
        sid = self.db.set_dropped_on_service(resource['type']['id'],
                                                resource['id'], dropped)
        self.db.commit()
