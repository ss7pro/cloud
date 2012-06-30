
class Tenants(object):

    def __init__(self,db):
        self.db = db

    def add(self,id):
        self.db.tenant_add(id)

    def ensure(self,id):
        r = self.db.tenant_get_by_id(id)
        if r is None:
            self.add(id)
        return r
