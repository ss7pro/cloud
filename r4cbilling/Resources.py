
class ResourcesGenericException(Exception):

    def __init__(self):
        self.msg = 'ResourcesGenericException'

    def __str__(self):
        return self.msg


class ResourcesWrongResourceType(ResourcesGenericException):

    def __init__(self,name,type,zone):
        self.msg = ('Unknown ResourceType: name=%(name)s,type=%(type)s,'
                        'zone=%(zone)s' % dict(name=name,type=type,zone=zone))

class ResourcesUnknownChargeSchemaName(ResourcesGenericException):

    def __init__(self,name):
        self.msg = ('Unknown ResourceChargeSchemaName: name=%(name)s' %
                    dict(name=name))

class ResourcesUnknownResourceTypeForServiceId(ResourcesGenericException):

    def __init__(self,sid):
        self.msg = ('Unknown ResourceType for ServiceId: id=%s' % sid)


class Resources(object):

    def __init__(self,db):
        self.db = db
        self.chargeschema = None

    def get_resource_type(self,name,type,zone):
        rt = self.db.get_resource_type(name,type,zone)
        if rt is None:
            raise ResourcesWrongResourceType(name,type,zone)
        return rt

    def get_resource_type_by_service_id(self,sid):
        r = self.db.get_resource_type_by_service_id(sid)
        if r is None:
            raise ResourcesUnknownResourceTypeForServiceId(sid)
        return r

    def get_charge_schema(self,ChargeSchemaName):
        r = self.db.get_charge_schema_by_name(ChargeSchemaName)
        if len(r) == 0:
            raise ResourcesUnknownChargeSchemaName(ChargeSchemaName)
        return r
