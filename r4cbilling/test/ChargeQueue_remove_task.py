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
    t['ServiceId'] = 58
    t['ResourceChargeSchemaId'] = 11
    db.begin()
    cq.remove_task(t, 'Task removal test', time.time())
    db.commit()

    print '\n\n\nOK\n\n\n'
