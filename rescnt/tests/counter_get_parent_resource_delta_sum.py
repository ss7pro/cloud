import sys

# temporary work around
#
sys.path.insert(0,'../')

from rescnt import counter

if __name__ == "__main__":

    c = counter.Counter()
    t = 1338230007
    print 'vm-misc-1'
    r = c.get_parent_resource_delta_sum('instance','r4cz1','vm-misc-1','disk','wr_kreq',t-60*60,t)
    print 'wr_kreq'
    print r
    r = c.get_parent_resource_delta_sum('instance','r4cz1','vm-misc-1','disk','rd_kreq',t-60*60,t)
    print 'rd_kreq'
    print r

