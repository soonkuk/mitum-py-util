import datetime
import pytz


class Hint(rlp.Serializable):
    fields = (
        ('h_type', text),
        ('h_ver', text),
    )
    
    @property
    def hint(self):
        d = self.as_dict()
        return d['h_type'] + ":" + d['h_ver']


def iso8601TimeStamp():
    return str(datetime.datetime.now(tz=pytz.utc).isoformat())


def getNewToken():
    return iso8601TimeStamp()