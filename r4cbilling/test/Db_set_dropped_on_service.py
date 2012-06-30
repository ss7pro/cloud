import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db


if __name__ == "__main__":

    db = db.Db()

    db.begin()
    db.set_dropped_on_service(4,'b42d1651-de2c-407f-8d81-ebfb24f02217',1)
    db.commit()
