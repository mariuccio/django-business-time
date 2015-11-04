=====
Business Time
=====

The django-business-time python package permits to calculate timedelta considering the working hours.

In your settings.py file you can specify a flag WORK_ON_SATURDAY that is False per default.

You can specify also a list of datetime.date named HOLIDAYS and a list of datetime.time named BUSINESS_DAILY_TIME.


BUSINESS_DAILY_TIME must have 4 items:
- The start time (default = 9)
- The start break time (default = 12)
- The stop break time (default = 13)
- The stop time (default = 17)


use as:
from business-time import business_timedelta



install with
pip install git+https://github.com/mariuccio/django-business-time.git


