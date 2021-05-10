import datetime
import pytz

def iso8601TimeStamp():
    return datetime.datetime.now(tz=pytz.utc).isoformat()

def getNewToken():
    return str(iso8601TimeStamp())