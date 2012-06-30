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
    t['ServiceId'] = 14
    t['ResourceId'] = 'vm-misc-1'
    t['ResourceChargeSchemaType'] = 'disk'
    t['ResourceChargeSchemaArea' ] = 'wr_kreq'
    # UNIX_TIMESTAMP('2012-05-29 13:58:58')
    t['LastCounter'] = 1338299938
    # UNIX_TIMESTAMP('2012-05-29 15:00:00')
    t['NextCharge'] = 1338303600
    r = cq.get_resource_counters_metered(t)
    print r
    t['ResourceChargeSchemaArea'] = 'rd_kreq'
    r = cq.get_resource_counters_metered(t)
    print r
    t['ResourceChargeSchemaType'] = 'interface'
    t['ResourceChargeSchemaArea'] = 'tx_kbytes'
    r = cq.get_resource_counters_metered(t)
    print r
    t['ResourceChargeSchemaArea'] = 'tx_kpackets'
    t['LastCounter'] = None
    r = cq.get_resource_counters_metered(t)
    print r
    print '\n\n\nOK\n\n\n'
