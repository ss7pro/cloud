import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import Services


if __name__ == "__main__":

    db = db.Db()
    s = Services.Services(db)

    # 2012-01-01
    t = 1325376000
    tenant = 'test-id-add'
    resource = dict(name='instance',type='m1.test',zone='r4cz1',id='instance-test-X')
    s.terminate(tenant,resource,t)


    print '\n\n\nOK\n\n\n'
