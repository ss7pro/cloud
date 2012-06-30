import time
import calendar

def mktime(datetime):
    if datetime.count('.'):
       time_format = "%Y-%m-%d %H:%M:%S.%f %Z"
    else:
       time_format = "%Y-%m-%d %H:%M:%S %Z"
    ts = time.strptime(datetime + ' UTC', time_format)
    return calendar.timegm(ts)

