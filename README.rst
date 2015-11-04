=====
django-business-time
=====

The django-business-time python package permits to calculate timedelta considering the working hours.

In your `settings.py` file you can specify the flag
```
WORK_ON_SATURDAY=False #by default
```

You can specify also a list of `datetime.date` named `HOLIDAYS` and a list of `datetime.time` named `BUSINESS_DAILY_TIME`

`BUSINESS_DAILY_TIME` must have 4 items:
* The start time (default = 9)
* The start break time (default = 12)
* The stop break time (default = 13)
* The stop time (default = 17)


use as:
```
from business_time import business_time

business_time.business_timedelta(dt1,dt2)
```
where `dt1` and `dt2` are 2 `datetime.datetime` objects

install with
```
pip install git+https://github.com/mariuccio/django-business-time.git
```

