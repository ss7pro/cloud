import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import ChargeQueue


if __name__ == "__main__":

    db = db.Db()
    cq = ChargeQueue.ChargeQueue(db)

    t = {}
    t['ServiceId'] = 63 
    t['ResourceChargeSchemaId'] = 15
    t['NextCharge'] = 1325376000
    r = cq.add_resource_charges(t,1,0.1,1325376000)
    db.commit()
    print r
    print '\n\n\nOK\n\n\n'
