import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import ChargeQueue


if __name__ == "__main__":

    db = db.Db()
    cq = ChargeQueue.ChargeQueue(db)

    t = cq.get_task(time.time())
    print t

    print '\n\n\nOK\n\n\n'
