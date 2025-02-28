from datetime import datetime, timedelta

print(datetime.now(),timedelta(minutes=30))
dt = datetime.now() - timedelta(minutes=30)
print(dt)
