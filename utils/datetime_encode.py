import json
import datetime
from dateutil.tz import tzutc

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    data = {"name": "Tom", "birthday": datetime.datetime(2019, 11, 20, 7, 34, 15, tzinfo = tzutc())}
    print(type(data))
    print(json.dumps(data, cls=DateEncoder))