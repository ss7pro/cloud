import sys

# temporary work around
#
sys.path.insert(0,'../')

from rescnt import db

if __name__ == "__main__":

    db = db.Db()
    r = db.get_resource_list('interface','r4cz1',None,111)
    print len(r)
    print r
    r = db.get_resource_list('instance','r4cz1','vm-firewall-1',None)
    print len(r)
    print r
