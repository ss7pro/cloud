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
    t['ResourceChargeSchemaType'] = 'main'
    t['ResourceChargeSchemaId'] = 15
# 2012-01-01 00:00:00
    t['LastCharge'] = 1325376000
    t['NextCharge'] = 1325376000 + 3600
    t['RateGroupName'] = 'instance-main'
    rcnt = {}
    rcnt['units'] = 42
    wchg = {}
# wchg['units'] = 30
# wchg['units'] = 40
# wchg['units'] = 10
    wchg['units'] = 40
    r = cq._charge_resource_back(t,rcnt,wchg,t['NextCharge'])
    db.commit()
    print r
    print '\n\n\nOK\n\n\n'
