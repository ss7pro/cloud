import time
import decimal

from r4cbilling import ServiceEvents
from r4cbilling import Resources
from rescnt import counter

class ChargeQueueGenericException(Exception):

    def __init__(self):
        self.msg = 'ChargeQueueGenericExeption'

    def __str__(self):
        return self.msg

class ChargeQueueChargePeriodsWrong(ChargeQueueGenericException):

    def __init__(self,ChargeTime):
        self.msg = ('None or multiple ChargePeriods for: %s.' %
                    time.strftime('%a, %d %b %Y %H:%M:%S +0000',
                    time.gmtime(ChargeTime)))

class ChargeQueueNoRateGroupFor(ChargeQueueGenericException):

    def __init__(self,RateGroupName,NextCharge,units):
        self.msg = ('No RateGroup for: RateGroupName=%s,NextCharge=%s,'
                    'units=%s' % (RateGroupName,time.strftime(
                    '%a, %d %b %Y %H:%M:%S +0000', time.gmtime(NextCharge)),
                    units))

class ChargeQueueUnknownResourceType(ChargeQueueGenericException):

    def __init__(self,sid):
        self.msg = ('Unknown resource type for ServiceId:%s' % sid)

class ChargeQueue(object):

    def __init__(self,db):
        self.db = db
        self.counter = counter.Counter()

    def run(self):
        while True:
            ct = time.time()
            t = self.get_task(ct)
            if t is None:
                break
            self.run_task(t,ct)
            self.unlock_task(t)

    def get_task(self,ct):
        while True:
            self.db.begin()
            t = self.db.get_charge_task(ct)
            if t is None:
                break
            if self.lock_task(t) == 0:
            # task is locked chose another one
                continue
            self.update_lastrun_on_task(t,ct)
            self.db.commit()
            break
        return t


    def run_task(self,t,ct):
        """Run ChargeQueue task

        t - task structure
        ct - execution timestamp
        """
        if (t['ServiceDropped'] is not None and
            t['NextCharge'] >= t['ServiceDropped']):
            # task needs to be removed from chargequeue as service is no longer
            # active
            return self.remove_task(t, 'Service Terminated: #1', ct)
        # check if service is eligble to be charged according to
        # current time. If not return
        if self.check_task_timeline(t,ct) == 0:
            return
        self.charge_resource(t,ct)

    def check_task_timeline(self,t,ct):
        # service is not born yet
        if t['ServiceCreated'] > ct:
            return 0
        # charge window for task is not yet
        if t['NextCharge'] > ct:
            return 0
        # NextCharge must be greater or equal than LastCharge
        if t['LastCharge'] is not None and t['NextCharge'] < t['LastCharge']:
            return 0
        return 1

    def charge_resource(self,t,ct):
        self.db.begin()
        # get usage counters
        rcnt = self.get_resource_counters(t)
        # get previous window charges
        wchg = self.get_resource_charges(t,prevWindow=True)
        if rcnt is None:
            # get current period charges
            cpchg = self.get_resource_charges(t)
            # get rate group based on charge period charges
            rg = self.get_rate_group(t,cpchg['units'])
            # we don't have counters for this service yet
            # schedule next check
            self.schedule_next_check(t,rg,ct)
            self.db.commit()
            return
        rcnt['units'] = decimal.Decimal(rcnt['units'])
        if rcnt['units'] > wchg['units']:
            # charges for this window are smaller than usage, charge
            # missing difference
            cunits = self._charge_resource_back(t,rcnt,wchg,ct)
            wchg['units'] += cunits
        # get current period charges
        cpchg = self.get_resource_charges(t)
        # get rate group based on charge period charges
        rg = self.get_rate_group(t,cpchg['units'])
        # all charged resources used, count for next in advance
        if (rcnt['units'] and (rcnt['units'] > wchg['units'] or
            rcnt['units'] == wchg['units'])):
            self._charge_resource_advance(t,rg['frequency'],ct)
            # we also pass rcnt['end'] which is last counter position
            # to start next charge
            self.schedule_next_charge(t,rg,rcnt['units']-wchg['units'],
                                        rcnt['end'],ct)
        else:
            self.schedule_next_check(t,rg,ct)
        self.db.commit()


    def _charge_resource_back(self,t,rcnt,wchg,ct):
        lt = t.copy()
        if lt['LastCharge'] is not None:
            lt['NextCharge'] = lt['LastCharge']
        # get current period charges
        cpchg = self.get_resource_charges(lt)
        # get rate group based on charge period charges
        rg = self.get_rate_group(lt,cpchg['units'])
        if rcnt['units'] <= wchg['units']:
            return 0
        if (rcnt['units'] - wchg['units']) / rg['units'] < 1.0:
            return 0
        um = int((rcnt['units'] - wchg['units']) / rg['units'])
        self.add_resource_charges(lt,rg['units']*um,rg['rate']*um,ct)
        return rg['units']*um

    def _charge_resource_advance(self,t,freq,ct):
        lt = t.copy()
        lt['LastCharge'] = lt['NextCharge']
        lt['NextCharge'] += freq
        # get charge period charges and window charges
        cpchg = self.get_resource_charges(lt)
        # get rate group based on charge period charges
        rg = self.get_rate_group(lt,cpchg['units'])
        if lt['ResourceChargeSchemaType'] == 'main':
            rcnt = self.calculate_resource_hours(lt)
            um = int(rcnt['units'] / rg['units'])
        else:
            um = 1
        self.add_resource_charges(t,rg['units']*um,rg['rate']*um,ct)

    @staticmethod
    def task_lock_string(t):
        return ('billing_ChargeQueue_SId:-%s-RCSId-%s' % (t['ServiceId'],
                t['ResourceChargeSchemaId']))

    def lock_task(self,t):
        return self.db.get_lock(self.task_lock_string(t))

    def unlock_task(self,t):
        return self.db.release_lock(self.task_lock_string(t))

    def update_lastrun_on_task(self,t,ct):
        return self.db.update_lastrun_on_charge_task(t['ServiceId'],
                t['ResourceChargeSchemaId'],ct)

    def get_resource_counters(self,t):
        if (t['ResourceChargeSchemaType'] == 'disk' or
            t['ResourceChargeSchemaType'] == 'interface' or
            t['ResourceChargeSchemaType'] == 'process'):
            return self.get_resource_counters_metered(t)
        elif t['ResourceChargeSchemaType'] == 'main':
            return self.calculate_resource_hours(t)
        else:
            return

    def get_resource_counters_metered(self,t):
        res = Resources.Resources(self.db)
        rt = res.get_resource_type_by_service_id(t['ServiceId'])
        rc = self._get_resource_counters_metered(rt['name'],rt['zone'],
                                    t['ResourceId'],
                                    t['ResourceChargeSchemaType'],
                                    t['ResourceChargeSchemaArea'],
                                    t['LastCounter'],
                                    t['NextCharge'])
        if rc is not None:
            r = {}
            r['begin'] = rc['first_ts']
            r['end'] = rc['last_ts']
            r['units'] = rc['sum']
            return r

    def _get_resource_counters_metered(self,ResourceTypeName,ResourceZone,
                                        ResourceId,ChargeSchemaType,
                                        ChargeSchemaArea,PrevCounter,
                                        MaxCounter):
        return self.counter.get_parent_resource_delta_sum(ResourceTypeName,
                                                    ResourceZone,ResourceId,    
                                                    ChargeSchemaType,
                                                    ChargeSchemaArea,
                                                    PrevCounter,
                                                    MaxCounter)


    def calculate_resource_hours(self,t):
        if (t['LastCharge'] is None) or (t['LastCharge'] == t['NextCharge']):
            r = {}
            r['begin'] = t['NextCharge']
            r['end'] = t['NextCharge']
            r['units'] = 0
            return r
        se = ServiceEvents.ServiceEvents(self.db)
        (h,rsize) = self._calculate_resource_hours(t['ServiceId'],
                                            t['ResourceChargeSchemaId'],
                                            t['LastCharge'],t['NextCharge'])
        r = {}
        r['begin'] = t['LastCharge']
        r['end'] = t['NextCharge']
        r['units'] = h
        r['rsize'] = rsize
        return r

    def _calculate_resource_hours(self,ServiceId,
                                            ResourceChargeSchemaId,
                                            left,right):
        se = ServiceEvents.ServiceEvents(self.db)
        return se.count_running_hours(ServiceId,ResourceChargeSchemaId,left,
                                        right)

    def get_resource_charges(self,t,prevWindow=False):
        """GET charges sum for current Period or if prevWindow is True
            get charges for previous window <LastCharge,NextCharge)."""
        if prevWindow is False:
            # get current charge period based on NextCharge datetime
            cp = self.get_charge_period(t['NextCharge'])
        else:
            # get sum of all  charges in <LastCharge,NextCharge) window
            cp = {}
            cp['begin'] = t['LastCharge']
            cp['end'] = t['NextCharge']
        pc = self.get_resource_charges_sum(t,cp)
        pc['begin'] = cp['begin']
        pc['end'] = cp['end']
        print pc
        return pc

    def get_charge_period(self,ChargeTime):
        r = self.db.get_charge_period(ChargeTime)
        if r is  None:
            raise ChargeQueueChargePeriodsWrong(ChargeTime)
        return r

    def get_resource_charges_sum(self,t,cp):
        return self.db.get_resource_charges_sum(t['ServiceId'],
                                                t['ResourceChargeSchemaId'],
                                                cp['begin'],cp['end'])

    def get_rate_group(self,t,units):
        r = self.db.get_rate_group(t['RateGroupName'],t['NextCharge'],units)
        if r is None:
            raise ChargeQueueNoRateGroupFor(t['RateGroupName'],t['NextCharge'],
                                            units)
        return r

    def add_resource_charges(self,t,units,rate,ct):
        return self.db.add_resource_period_charges(t['ServiceId'],
                                                t['ResourceChargeSchemaId'],
                                                units,rate,t['NextCharge'],ct)

    def schedule_next_charge(self,t,rg,SavedUnits,LastCounter,ct):
        freq = rg['frequency']
        #
        # TODO
        #
        # Implement SavedUnits compensation
        #
        #
        return self.db.update_charge_task_schedule(t['ServiceId'],
                                        t['ResourceChargeSchemaId'],
                                        t['NextCharge'] + freq,
                                        t['NextCharge'] + freq,
                                        ct,LastCharge=t['NextCharge'],
                                        SavedUnits=SavedUnits +
                                        decimal.Decimal(t['SavedUnits']),
                                        LastCounter=LastCounter)

    def schedule_next_check(self,t,rg,ct):
        return self.db.update_charge_task_schedule(t['ServiceId'],
                                        t['ResourceChargeSchemaId'],
                                        t['NextCharge'] + rg['frequency'],
                                        t['NextCharge'] + rg['frequency'],
                                        ct)

    def remove_task(self, t, reason, ct):
        return self.update_status_on_task(t, reason, ct)

    def update_status_on_task(self, t, status, ct):
        return self.db.update_status_on_charge_task(t['ServiceId'],
                t['ResourceChargeSchemaId'], status, ct)
