import sys

sys.path.insert(0,'../')

from r4cbilling import db


class sqlsamples(object):
    def __init__(self):
        self.dbc = db.Db()
        self.db = self.dbc.db

    def add_Tenant(self,id,name):
        c = self.db.cursor()
        c.execute("""INSERT INTO Tenants (id,name,balance) VALUES(%(id)s,
                    %(name)s,%(balance)s)""", dict(id=id,name=name,balance=0))
        c.close()

    def add_RateGroup(self,GroupName,description,units,rate,frequency,minunits,
        ValidFrom,ValidTo):
        c = self.db.cursor()
        c.execute("""INSERT INTO RateGroups (GroupName,description,units,rate,
                        frequency,minunits,ValidFrom,ValidTo)
                        VALUES(%(GroupName)s,%(description)s,%(units)s,%(rate)s,
                        %(frequency)s,%(minunits)s,%(ValidFrom)s,
                        %(ValidTo)s)""",dict(GroupName=GroupName,
                        description=description,units=units,rate=rate,frequency=frequency,minunits=minunits,ValidFrom=ValidFrom,ValidTo=ValidTo))
        c.close()

    def add_ResourceChargeSchema(self,name,type,area,RateGroupName):
        c = self.db.cursor()
        c.execute("""INSERT INTO ResourceChargeSchemas (name,type,area,
                    RateGroupName) VALUES(%(name)s,%(type)s,%(area)s,
                    %(RateGroupName)s)""",dict(name=name,type=type,area=area,
                    RateGroupName=RateGroupName))
        c.close()

    def add_ResourceType(self,name,type,zone,ChargeSchemaName):
        c = self.db.cursor()
        c.execute("""INSERT INTO ResourceTypes (name,type,zone,
                    ChargeSchemaName) VALUES(%(name)s,%(type)s,%(zone)s,
                    %(ChargeSchemaName)s)""",dict(name=name,type=type,
                    zone=zone,ChargeSchemaName=ChargeSchemaName))
        c.close()
    def add_ChargePeriod(self,begin,end):
        c = self.db.cursor()
        c.execute("""INSERT INTO ChargePeriods (begin,end) VALUES(%(begin)s,
                    %(end)s)""",dict(begin=begin,end=end))
        c.close()


if __name__ == "__main__":
    s = sqlsamples()
    s.add_Tenant('test-id','test')
    s.add_RateGroup('instance-main','Instance main charges',1,0.05,3600,0,'2012-01-01 00:00:00',None)
    s.add_RateGroup('instance-disk','Instance disk requestes charges',1000,0.05,3600,0,'2012-01-01 00:00:00',None)
    s.add_RateGroup('instance-interface','Instance interface bytes charges',1024 * 1024,5.34,60,0,'2012-01-01 00:00:00',None)
    s.add_ResourceChargeSchema('instance','disk','rrq','instance-disk')
    s.add_ResourceChargeSchema('instance','disk','wrq','instance-disk')
    s.add_ResourceChargeSchema('instance','interface','tx_bytes','instance-interface')
    s.add_ResourceChargeSchema('instance','interface','rx_bytes','instance-interface')
    s.add_ResourceChargeSchema('instance','interface','hours','instance-main')
    s.add_ResourceType('instance','m1.test','r4cz1','instance')
    for j in (2010,2011,2012,2013,2014,2015):
        for i in range(1,12):
            s.add_ChargePeriod(str(j) + '-' + str(i) + '-01 00:00:00',str(j) + '-' + str(i+1) + '-01 00:00:00')
        s.add_ChargePeriod(str(j) + '-' + str(i+1) + '-01 00:00:00',str(j+1) + '-01-01 00:00:00')
    s.db.commit()
