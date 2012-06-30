import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db


if __name__ == "__main__":

    db = db.Db()

    db.begin()
    db.update_status_on_charge_task(58,11,'test',1)
    db.commit()
