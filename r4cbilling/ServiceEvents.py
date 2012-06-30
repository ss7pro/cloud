
class ServiceEventsGenericException(Exception):

    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class ServiceEvents(object):

    def __init__(self,db):
        self.db = db

    @staticmethod
    def count_common_seconds(start,stop,left,right):
        """Return number of seconds in event <start,stop) during
            period <left,right)"""
        if stop is not None and start > stop:
            raise ServiceEventsGenericException('start > stop')
        if left > right:
            raise ServiceEventsGenericException('left > right')
        if start >= right:
            return 0
        if stop is not None and left >= stop:
            return 0
        if start > left:
            b = start
        else:
            b = left
        if stop is None:
            e = right
        elif stop > right:
            e = right
        else:
            e = stop
        return e - b

    def count_running_hours(self,ServiceId,ResourceChargeSchemaId,left,right):
        seconds = 0
        sel = self.db.get_service_status_events(ServiceId,
                                        ResourceChargeSchemaId,left,right)
        last_ts = None
        start_size = None
        for se in sel:
            if se['event'] == 'stop':
                last_ts = se['ts']
            if se['event'] == 'start':
                seconds += (self.count_common_seconds(se['ts'],last_ts,left,
                                                        right)
                                * se['size'])
                last_ts = se['ts']
                if start_size is None:
                    start_size = se['size']
        # we neeed to check if there's no start event which was
        # created before our window.
        sel = self.db.get_service_status_events(ServiceId,
                                        ResourceChargeSchemaId,left,right,
                                        last=True)
        if len(sel):
            se = sel.pop(0)
            if se['event'] == 'start':
                seconds += (self.count_common_seconds(se['ts'],last_ts,left,
                                                        right)
                                * se['size'])
                if start_size is None:
                    start_size = se['size']
        return float(seconds) / 3600.0, start_size

    def addEvent(self, ServiceId, ResourceChargeSchemaId, ts, event, size):
        self.db.add_service_events_record(ServiceId, ResourceChargeSchemaId,
                                            ts, event, size)
