import sys
import traceback

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import Resources


if __name__ == "__main__":

    db = db.Db()
    r = Resources.Resources(db)
    ret = r.get_resource_type('instance','m1.test','r4cz1')
    print ret
    try:
        ret = r.get_resource_type('instance','m1.testa','r4cz1')
    except:
        traceback.print_exc()

    print '\n\n\nOK\n\n\n'
