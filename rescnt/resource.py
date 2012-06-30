from rescnt import exc

class Resource(object):
    """Resource class.

        Resource is identified by:

            type
            zone
            name
            parent - optionaly parent resource id
    """
    def __init__(self,db):

        self.db = db

    def add(self,type,zone,name,parent=None):
        """Add resource."""

        return self.db.add_resource(type,zone,name,parent)

    def get_id(self,type,zone,name,parent=None):
        """Get resource by id."""

        return self.db.get_resource_id(type,zone,name,parent)

    def get_list(self,type,zone,name,parent=None):
        """Get macthing resource list."""

        return self.db.get_resource_list(type,zone,name,parent)

    def ensure(self,type,zone,name,parent=None):
        """Ensure resource is present in the database."""

        r = self.get_id(type,zone,name,parent=parent)
        if r:
            return r
        self.add(type,zone,name,parent=parent)
        r = self.get_id(type,zone,name,parent=parent)
        if not r:
            raise exc.ResourceExc('Resource.ensure(): Unable to ensure resource.',dict(type,zone,name,parent=parent))
        return r

    def get_parent_counters_delta_sum(self,ParentResourceType,
                                ParentResourceZone,ParentResourceValue,
                                ResourceType,CounterType,PrevCounter,
                                MaxCounter):
        pid =  self.get_id(ParentResourceType,ParentResourceZone,
                            ParentResourceValue)
        if pid is None:
            return

        lr = self.get_list(ResourceType,ParentResourceZone,None,pid)
        return self.db.get_parent_resource_counters_delta_sum(lr,CounterType,
                                                                PrevCounter,
                                                                MaxCounter)
