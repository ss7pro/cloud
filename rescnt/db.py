import sys
import exc
import MySQLdb

class Db(object):

    def __init__(self):

        self.username = 'resourcecounters'
        self.password = 'u07Kq0MTZPgamlwbnUJGBnl80bFbfjT0'
        self.host = '10.76.0.202'
        self.database = 'resourcecounters'
        self.connect()
        self.cursor = self.db.cursor()
        self.cursor.execute("""SET time_zone = '+00:00'""")


    def connect(self):

        self.db = None
        self.db = MySQLdb.connect(host=self.host,user=self.username,
                                        passwd=self.password,db=self.database,
                                        connect_timeout=1)
        self.db.autocommit(True)
        return self.db

    def close(self):

        try:
            self.db.close()
        except AttributeError:
            pass

    def get_resource_id(self,type,zone,name,parent=None):

        r = None
        c = self.cursor
        if parent:
            c.execute("""SELECT id FROM resources WHERE type = %(type)s
                        AND zone = %(zone)s AND value = %(value)s
                        AND parent = %(parent)s""",
                        dict(type=type,zone=zone,value=name,parent=parent))
        else:
            c.execute("""SELECT id FROM resources WHERE type = %(type)s
                        AND zone = %(zone)s AND value = %(value)s""",
                        dict(type=type,zone=zone,value=name))
        if c.rowcount == 1:
            r = c.fetchone()[0]
        elif c.rowcount > 1:
            c.close()
            raise exc.ResourceDbExc('Db.get_resource_id(): More than one '
                                    'result.', dict(type=type,zone=zone,
                                    value=name,parent=parent))
        return r

    def add_resource(self,type,zone,name,parent=None):
        c = self.cursor
        if parent:
            c.execute("""INSERT INTO resources (type,zone,value,parent,
                        added) VALUES(%(type)s,%(zone)s,%(value)s
                        ,%(parent)s,NOW())""",
                        dict(type=type,zone=zone,value=name,parent=parent))
        else:
            c.execute("""INSERT INTO resources (type,zone,value,added)
                         VALUES(%(type)s,%(zone)s,%(value)s,NOW())""",
                         dict(type=type,zone=zone,value=name))

    def get_last_counter_entry(self,resource_id,type):
        r = None
        c = self.cursor
        c.execute("""SELECT value,UNIX_TIMESTAMP(added) FROM counters WHERE
                    resource = %(resource)s AND type = %(type)s
                    ORDER BY added DESC LIMIT 1""", dict(
                    resource=resource_id,type=type))
        if c.rowcount == 1:
            cr = c.fetchone()
            r = {}
            r['value'] = cr[0]
            r['added'] = cr[1]
        return r

    def add_counter_entry(self,resource_id,type,value,delta,added,prevadded):
        c = self.cursor
        c.execute("""INSERT INTO counters (resource,type,value,delta,added,
                        prev) VALUES(%(resource)s,%(type)s,%(value)s,%(delta)s,FROM_UNIXTIME(%(added)s),FROM_UNIXTIME(%(prev)s))""", dict(
                        resource=resource_id,type=type,value=value,
                        delta=delta,added=added,prev=prevadded))

    def get_resource_list(self,type,zone,name,parent):
        q = """SELECT id,parent,type,value FROM resources WHERE
                type = %(type)s  AND zone = %(zone)s"""
        if parent is not None:
            q += " AND parent = %(parent)s"
        if name is not None:
            q += " AND value = %(value)s"
        self.cursor.execute(q,dict(type=type,zone=zone,value=name,
                            parent=parent))
        r = []
        for i in range(self.cursor.rowcount):
            row = self.cursor.fetchone()
            f = ('id','parent','type','value')
            res = {}
            j = 0
            for n in f:
                res[n] = row[j]
                j += 1
            r.append(res)
            del res
        return r

    def get_parent_resource_counters_delta_sum_sql(self,ResourceList,
                                                    CounterType,PrevCounter,
                                                    MaxCounter):
        # build sql resource list
        rl = ""
        for i in ResourceList:
            if len(rl):
                rl += ", "
            rl += str(i['id'])
        q = """SELECT resource,SUM(delta),UNIX_TIMESTAMP(MAX(added)),
                UNIX_TIMESTAMP(MIN(added)) FROM counters FORCE INDEX (resource) WHERE resource IN ("""
        q += rl
        q+= """) AND type = %(CounterType)s AND
                added > FROM_UNIXTIME(%(PrevCounter)s) AND
                added < FROM_UNIXTIME(%(MaxCounter)s) GROUP BY resource,type"""
        self.cursor.execute(q,dict(CounterType=CounterType,
                            PrevCounter=PrevCounter,MaxCounter=MaxCounter))

    def get_parent_resource_counters_delta_sum(self,ResourceList,CounterType,
                                                PrevCounter,MaxCounter):
        if PrevCounter is None:
        # if there's no prev counter we start from the begining
            PrevCounter = 0
        self.get_parent_resource_counters_delta_sum_sql(ResourceList,
                                                        CounterType,
                                                        PrevCounter,MaxCounter)
        sum = 0
        ts_max = PrevCounter
        ts_min = MaxCounter
        for i in range(self.cursor.rowcount):
            row = self.cursor.fetchone()
            sum += row[1]
            if row[2] > ts_max:
                ts_max = row[2]
            if ts_min > row[3]:
                ts_min = row[3]
        if ts_max != PrevCounter:
            r = {}
            r['sum'] = long(sum)
            r['first_ts'] = ts_min
            r['last_ts'] = ts_max
            return r
        return


    def __del__(self):
        self.close()
