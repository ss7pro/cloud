import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import ServiceEvents


if __name__ == "__main__":

    db = db.Db()
    st = ServiceEvents.ServiceEvents(db)

# 2012-01-01 00:00:00
# 2012-01-02 00:00:00
    print st.count_running_hours(63,15,1325376000,1325462400)

    print '\n\n\nOK\n\n\n'
