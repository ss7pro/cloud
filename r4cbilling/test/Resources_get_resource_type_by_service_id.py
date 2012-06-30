import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import Resources


if __name__ == "__main__":

    db = db.Db()
    res = Resources.Resources(db)

    r = res.get_resource_type_by_service_id(14)
    print r
    try:
       r = res.get_resource_type_by_service_id(111111111111111)
    except Resources.ResourcesUnknownResourceTypeForServiceId:
        print 'OK Nie ma'
        pass
    print '\n\n\nOK\n\n\n'
