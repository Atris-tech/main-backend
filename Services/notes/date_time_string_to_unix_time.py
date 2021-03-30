import datetime as datetime
import dateutil.parser
import time

def convert_dt_to_unixt(date_time_string):
    d = dateutil.parser.parse(date_time_string)
    timestamp = (time.mktime(d.timetuple())*1e3+d.microsecond/1e3)/1e3
    return timestamp
