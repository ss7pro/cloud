import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db


if __name__ == "__main__":

    db = db.Db()

    db.begin()
    r = db.get_resource_type_by_service_id(12)
    print r
    db.commit()
