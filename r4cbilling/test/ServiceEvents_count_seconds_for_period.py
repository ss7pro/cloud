import sys
import traceback
import time

sys.path.insert(0,'../')

from r4cbilling import db
from r4cbilling import ServiceEvents


if __name__ == "__main__":

    db = db.Db()
    st = ServiceEvents.ServiceEvents(db)

    print st.count_common_seconds(47,48,51,101)
    print st.count_common_seconds(50,60,50,61)
    print st.count_common_seconds(0,None,0,1)

    print '\n\n\nOK\n\n\n'
