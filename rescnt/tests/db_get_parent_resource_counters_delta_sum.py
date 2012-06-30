import sys

# temporary work around
#
sys.path.insert(0,'../')

from rescnt import db

if __name__ == "__main__":

    db = db.Db()
    t = 1338230007
    rl = [{'id':100},{'id':101}]
    r = db.get_parent_resource_counters_delta_sum(rl,'rx_kbytes',t-60*60,t)
    print r
    r = db.get_parent_resource_counters_delta_sum(rl,'tx_kbytes',t-60*60,t)
    print r
    rl = [{'id':105},{'id':104}]
    r = db.get_parent_resource_counters_delta_sum(rl,'rx_kbytes',t-60*60,t)
    print r
    r = db.get_parent_resource_counters_delta_sum(rl,'tx_kbytes',t-60*60,t)
    print r
    rl = [{'id':108}]
    r = db.get_parent_resource_counters_delta_sum(rl,'rx_kbytes',t-60*60,t)
    print r
    r = db.get_parent_resource_counters_delta_sum(rl,'tx_kbytes',t-60*60,t)
    print r
    rl = [{'id':112},{'id':113}]
    r = db.get_parent_resource_counters_delta_sum(rl,'rx_kbytes',t-60*60,t)
    print r
    r = db.get_parent_resource_counters_delta_sum(rl,'tx_kbytes',t-60*60,t)
    print r
