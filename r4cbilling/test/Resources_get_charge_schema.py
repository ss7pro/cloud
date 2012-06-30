import sys
import traceback

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import Resources


if __name__ == "__main__":

    db = db.Db()
    r = Resources.Resources(db)
    for i in r.get_charge_schema('instance'):
        print i

    try:
        for i in r.get_charge_schema('instanceX'):
            print i
    except:
        traceback.print_exc()

    print '\n\n\nOK\n\n\n'
