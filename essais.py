import datetime

ladate = datetime.datetime(year=1960, month=4, day=29)

aujourdhui = datetime.datetime.now()

delta = aujourdhui - ladate

print(delta)

minutessince = int(delta.total_seconds() / 60)
print(minutessince)
