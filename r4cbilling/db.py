import sys
import MySQLdb

class Db(object):

    def __init__(self):

        self.username = 'billing'
        self.password = 'HieShoowooj4ohvu0Siz1eechahqueez'
        self.host = '10.76.0.202'
        self.database = 'billing'
        self.connect()
        self.cursor = self.db.cursor()
        # use UTC as time zone
        self.cursor.execute("""SET time_zone = '+00:00'""")

    def connect(self):

        self.db = None
        self.db = MySQLdb.connect(host=self.host,user=self.username,
                                        passwd=self.password,db=self.database,
                                        connect_timeout=1)
        return self.db

    def begin(self):
        self.db.rollback()

    def commit(self):
        self.db.commit()
        
    def get_lock(self,key,timeout=0):
        self.cursor.execute("""SELECT GET_LOCK(%(key)s,%(timeout)s)""",
                                dict(key=key,timeout=timeout))
        row = self.cursor.fetchone()
        return row[0]

    def release_lock(self,key):
        self.cursor.execute("""SELECT RELEASE_LOCK(%(key)s)""",dict(key=key))
        row = self.cursor.fetchone()
        return row[0]
        

    def close(self):

        try:
            self.db.close()
        except AttributeError:
            pass

    def get_last_insert_id(self):
        self.cursor.execute("""SELECT LAST_INSERT_ID()""")
        row = self.cursor.fetchone()
        return row[0]
        

    def get_resource_type(self,name,type,zone):
        self.cursor.execute("""SELECT id,name,type,zone,ChargeSchemaName FROM
                                ResourceTypes WHERE name = %(name)s AND
                                type = %(type)s AND zone = %(zone)s""",
                                dict(name=name,type=type,zone=zone));
        if self.cursor.rowcount >= 1:
            row = self.cursor.fetchone()
            r = {}
            r['id'] = row[0]
            r['name'] = row[1]
            r['type'] = row[2]
            r['zone'] = row[3]
            r['charge_schema_name'] = row[4]
        else:
            r = None
        return r

    def get_resource_type_by_service_id(self,sid):
        self.cursor.execute("""SELECT ResourceName,ResourceType,ResourceZone
                            FROM ServiceTypeView WHERE
                            ServiceId = %(ServiceId)s""",dict(ServiceId=sid))
        if self.cursor.rowcount >= 1:
            row = self.cursor.fetchone()
            r = {}
            r['name'] = row[0]
            r['type'] = row[1]
            r['zone'] = row[2]
        else:
            r = None
        return r

    def service_add(self,TenantId,ResourceTypeId,ResourceId,created,dropped):
        self.cursor.execute("""INSERT INTO Services (tenant,ResourceType,
                                ResourceId,created,dropped) VALUES(%(tenant)s,
                                %(ResourceType)s,%(ResourceId)s,
                                FROM_UNIXTIME(%(created)s),
                                FROM_UNIXTIME(%(dropped)s))""",
                                dict(tenant=TenantId,
                                ResourceType=ResourceTypeId,
                                ResourceId=ResourceId,created=created,
                                dropped=dropped))
        return self.get_last_insert_id()

    def get_charge_schema_by_name(self,ChargeSchemaName):
        self.cursor.execute("""SELECT id,name,type,area,RateGroupName FROM
                                ResourceChargeSchemas WHERE name = %(name)s""",
                            dict(name=ChargeSchemaName))
        r = []
        for i in range(self.cursor.rowcount):
            row = self.cursor.fetchone()
            cs = {}
            cs['id'] = row[0]
            cs['name'] = row[1]
            cs['type'] = row[2]
            cs['area'] = row[3]
            cs['RateGroupName'] = row[4]
            r.append(cs)
            del cs
        return r

    def add_charge_queue(self,ServiceId,ResourceChargeSchema,created,status):
        self.cursor.execute("""INSERT INTO ChargeQueue (service,
                                ResourceChargeSchema,NextCharge,LastCharge,
                                NextRun,LastRun,status) VALUES(%(service)s,
                                %(ResourceChargeSchema)s,
                                FROM_UNIXTIME(%(NextCharge)s),
                                FROM_UNIXTIME(%(LastCharge)s),
                                FROM_UNIXTIME(%(NextRun)s),
                                FROM_UNIXTIME(%(LastRun)s),
                                %(status)s)""",dict(service=ServiceId,
                                ResourceChargeSchema=ResourceChargeSchema,
                                NextCharge=created,LastCharge=None,
                                NextRun=created,
                                LastRun=created,status=status))

    def tenant_add(self,id):
        self.cursor.execute("""INSERT INTO Tenants (id,balance) VALUES(
                                %(id)s,%(balance)s)""",dict(id=id,balance=0))

    def tenant_get_by_id(self,id):
        self.cursor.execute("""SELECT id,balance FROM Tenants WHERE
                                id = %(id)s""",dict(id=id))
        if self.cursor.rowcount == 0:
            return None
        r = {}
        row = self.cursor.fetchone()
        r['id'] = row[0]
        r['balance'] = row[1]
        return r

    def get_charge_task(self,ct):
        self.cursor.execute("""SELECT
                                    ServiceId,
                                    TenantId,
                                    UNIX_TIMESTAMP(ServiceCreated),
                                    UNIX_TIMESTAMP(ServiceDropped),
                                    ResourceId,
                                    UNIX_TIMESTAMP(NextCharge),
                                    UNIX_TIMESTAMP(NextRun),
                                    UNIX_TIMESTAMP(LastCharge),
                                    UNIX_TIMESTAMP(LastCounter),
                                    Status,
                                    SavedUnits,
                                    ResourceChargeSchemaId,
                                    ResourceChargeSchemaName,
                                    ResourceChargeSchemaType,
                                    ResourceChargeSchemaArea,
                                    RateGroupName,
                                    UNIX_TIMESTAMP(NextRun)
                                FROM
                                    ChargeQueueView
                                WHERE
                                    NextRun <= FROM_UNIXTIME(%(ct)s)
                                    AND status IS NULL
                                ORDER BY
                                    LastRun ASC,NextRun ASC,
                                    LastCharge ASC
                                LIMIT 1""",dict(ct=ct))
        r = None
        for i in range(self.cursor.rowcount):
            row = self.cursor.fetchone()
            f = ('ServiceId','TenantId','ServiceCreated','ServiceDropped',
                    'ResourceId','NextCharge','NextRun','LastCharge',
                    'LastCounter','Status','SavedUnits',
                    'ResourceChargeSchemaId','ResourceChargeSchemaName',
                    'ResourceChargeSchemaType','ResourceChargeSchemaArea',
                    'RateGroupName','NextRun')
            r = {}
            j = 0
            for n in f:
                r[n] = row[j]
                j += 1
        return r

    def update_lastrun_on_charge_task(self,ServiceId,ResourceChargeSchemaId,ct):
        self.cursor.execute("""UPDATE ChargeQueue SET
                                LastRun = FROM_UNIXTIME(%(ct)s) WHERE
                                service = %(service)s AND
                                ResourceChargeSchema =
                                %(ResourceChargeSchema)s""",dict(ct=ct,
                                service=ServiceId,
                                ResourceChargeSchema=ResourceChargeSchemaId))

    def update_status_on_charge_task(self, ServiceId, ResourceChargeSchemaId,
                                        status, ct):
        self.cursor.execute("""UPDATE ChargeQueue SET
                                status = %(status)s,
                                LastRun = FROM_UNIXTIME(%(ct)s) WHERE
                                service = %(service)s AND
                                ResourceChargeSchema =
                                %(ResourceChargeSchema)s""",
                                dict(status=status,
                                        ct=ct,
                                        service=ServiceId,
                                        ResourceChargeSchema=
                                        ResourceChargeSchemaId))

    def get_charge_period(self,ChargeTime):
        self.cursor.execute("""SELECT id,UNIX_TIMESTAMP(begin),
                                UNIX_TIMESTAMP(end) FROM ChargePeriods WHERE
                                FROM_UNIXTIME(%(ChargeTime)s) >= begin AND
                                FROM_UNIXTIME(%(ChargeTime)s) < end""",
                                dict(ChargeTime=ChargeTime))
        if self.cursor.rowcount != 1:
            return None
        row = self.cursor.fetchone()
        r = {}
        r['id'] = row[0]
        r['begin'] = row[1]
        r['end'] = row[2]
        return r

    def get_resource_charges_sum(self,ServiceId,ResourceChargeSchemaId,
                                    CpBegin,CpEnd):
        query = """SELECT SUM(amount),SUM(units) FROM ResourcePeriodCharges
                    WHERE service = %(service)s AND ResourceChargeSchema =
                    %(ResourceChargeSchema)s """
        if CpBegin is None:
            query += "AND ChargeTime = FROM_UNIXTIME(%(CpEnd)s)"""
        else:
            query += """AND ChargeTime >= FROM_UNIXTIME(%(CpBegin)s)
                        AND ChargeTime < FROM_UNIXTIME(%(CpEnd)s)"""
        self.cursor.execute(query,dict(service=ServiceId,ResourceChargeSchema=
                                        ResourceChargeSchemaId,CpBegin=CpBegin,
                                        CpEnd=CpEnd))
        row = self.cursor.fetchone()
        r = {}
        if row[0] is None:
            r['amount'] = 0
        else:
            r['amount'] = row[0]
        if row[1] is None:
            r['units'] = 0
        else:
            r['units'] = row[1]
        return r

    def get_rate_group(self,RateGroupName,ChargeTime,units):
        self.cursor.execute("""SELECT GroupName,minunits,units,rate,frequency
                                FROM RateGroups WHERE
                                GroupName = %(GroupName)s AND
                                FROM_UNIXTIME(%(ChargeTime)s) >= ValidFrom AND
                                (ValidTo IS NULL OR
                                    FROM_UNIXTIME(%(ChargeTime)s) < ValidTo) AND
                                (minunits IS NULL OR %(units)s >= minunits)
                                ORDER BY
                                    minunits DESC,
                                    ValidFrom DESC,
                                    rate DESC
                                LIMIT 1""",dict(GroupName=RateGroupName,
                                ChargeTime=ChargeTime,units=units))
        if self.cursor.rowcount != 1:
            return None
        row = self.cursor.fetchone()
        r = {}
        r['GroupName'] = row[0]
        r['minunits'] = row[1]
        r['units'] = row[2]
        r['rate'] = row[3]
        r['frequency'] = row[4]
        return r

    def add_resource_period_charges(self,ServiceId,ResourceChargeSchemaId,units,
                                        amount,ChargeTime,RunTime):
        self.cursor.execute("""INSERT INTO ResourcePeriodCharges
                            (service,ResourceChargeSchema,amount,units,
                            ChargeTime,RunTime) VALUES(%(service)s,
                            %(ResourceChargeSchema)s,%(amount)s,%(units)s,
                            FROM_UNIXTIME(%(ChargeTime)s),
                            FROM_UNIXTIME(%(RunTime)s))""",
                            dict(service=ServiceId,
                            ResourceChargeSchema=ResourceChargeSchemaId,
                            amount=amount,units=units,ChargeTime=ChargeTime,
                            RunTime=RunTime))

    def update_charge_task_schedule(self,ServiceId,ResourceChargeSchemaId,
                                NextCharge,NextRun,LastRun,LastCharge=None,
                                SavedUnits=None,LastCounter=None):
        query = """UPDATE ChargeQueue SET
                    NextCharge = FROM_UNIXTIME(%(NextCharge)s),
                    NextRun = FROM_UNIXTIME(%(NextRun)s),
                    LastRun = FROM_UNIXTIME(%(LastRun)s) """
        if LastCharge is not None:
            query += ",LastCharge = FROM_UNIXTIME(%(LastCharge)s) "
        if LastCounter is not None:
            query += ",LastCounter = FROM_UNIXTIME(%(LastCounter)s) "
        if SavedUnits is not None:
            query += ",SavedUnits = %(SavedUnits)s "
        query += """WHERE service = %(service)s
                    AND ResourceChargeSchema = %(ResourceChargeSchema)s"""
        self.cursor.execute(query,dict(NextCharge=NextCharge,NextRun=NextRun,
                            LastRun=LastRun,LastCharge=LastCharge,
                            LastCounter=LastCounter,SavedUnits=SavedUnits,
                            service=ServiceId,
                            ResourceChargeSchema=ResourceChargeSchemaId))

    def get_service_status_events(self,service,ResourceChargeSchema,left,right,last=False):
        query = """SELECT UNIX_TIMESTAMP(ts),event,size
                    FROM ServiceEvents WHERE service = %(service)s
                    AND (event = 'start' OR event = 'stop') """
        if ResourceChargeSchema is not None:
            query += "AND ResourceChargeSchema = %(ResourceChargeSchema)s "
        else:
            query += "AND ResourceChargeSchema IS NULL "
        if last is True:
            query += """AND ts < FROM_UNIXTIME(%(left)s) ORDER BY ts DESC LIMIT 1"""
        else:
            query += """AND ts >= FROM_UNIXTIME(%(left)s)
            AND ts < FROM_UNIXTIME(%(right)s) ORDER BY ts DESC"""
        self.cursor.execute(query,dict(service=service,
                                ResourceChargeSchema=ResourceChargeSchema,
                                left=left,right=right))
        r = []
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            res = {}
            res['ts'] = row[0]
            res['event'] = row[1]
            res['size'] = row[2]
            r.append(res)
        return r

    def add_service_events_record(self, service, ResourceChargeSchemaId, ts,
                                    event, size):
        self.cursor.execute("""INSERT INTO ServiceEvents (service,
                                ResourceChargeSchema,ts,event,size) VALUES(
                                %(service)s,%(ResourceChargeSchema)s,
                                FROM_UNIXTIME(%(ts)s),%(event)s,%(size)s)""",
                                dict(service=service,
                                        ResourceChargeSchema=
                                        ResourceChargeSchemaId, ts=ts,
                                        event=event, size=size
                                        )
                                )

    def set_dropped_on_service(self, ResourceType, ResourceId, ts):
        self.cursor.execute("""UPDATE Services SET dropped =
                                FROM_UNIXTIME(%(dropped)s) WHERE
                                ResourceType = %(ResourceType)s AND
                                ResourceId = %(ResourceId)s""",
                                dict(dropped=ts, ResourceType=ResourceType,
                                        ResourceId=ResourceId))

    def __del__(self):
        self.close()
