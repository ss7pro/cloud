import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db


if __name__ == "__main__":

    db = db.Db()

    db.begin()
    r = db.get_lock('dupa')
    print ('GET_LOCK: %s' % r)
    r = db.release_lock('dupa')
    print ('RELEASE_LOCK: %s' % r)
    r = db.release_lock('dupa')
    print ('RELEASE_LOCK: %s' % r)
    db.commit()
