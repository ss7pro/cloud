import time
import sys

sys.path.insert(0,'/home/ubuntu/cloud')

from r4c import utils

if __name__ == '__main__':
    ct = utils.mktime('2012-03-25 02:00:00 UTC')
    r = time.gmtime(ct)
    print ct
    print r
    ct = utils.mktime('2012-03-25 02:00:00.0111 UTC')
    r = time.gmtime(ct)
    print ct
    print r
