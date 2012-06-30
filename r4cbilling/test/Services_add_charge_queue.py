import sys
import traceback

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import Services


if __name__ == "__main__":

    db = db.Db()
    s = Services.Services(db)

    tenant = dict(name='name',id='test-id')
    resource = dict(id='instance-test',type=dict(id=7,charge_schema_name='instance'))
    sid = s.add(tenant,resource,'2011-01-01','2020-01-01')
    s.add_service_to_charge_queue(sid,resource,'2011-01-01')


    print '\n\n\nOK\n\n\n'
