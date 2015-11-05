=====
django-business-time
=====

The django-business-time python package permits to calculate timedelta considering the working hours.

In your `settings.py` file you can specify the flag

.. code-block:: python
    WORK_ON_SATURDAY=False
Because several companies are working also on saturday :(

You can specify also a list of `datetime.date` named `HOLIDAYS` and a list of `datetime.time` named `BUSINESS_DAILY_TIME`

`BUSINESS_DAILY_TIME` must have 4 items:

* The start time (default = 9)
* The start break time (default = 12)
* The stop break time (default = 13)
* The stop time (default = 17)


use as:
.. code-block:: python

  from business_time import business_timedelta

  business_timedelta(dt1,dt2)

where `dt1` and `dt2` are 2 `datetime.datetime` objects and `dt2 >= dt1`

install with

.. code-block:: bash

  pip install git+https://github.com/mariuccio/django-business-time.git

and then in your settings.py:

.. code-block:: python
    INSTALLED_APPS = (
        ...

        'business_time',

    )

an example of settings to put in your settings.py can be:
.. code-block:: python

WORK_ON_SATURDAY = False

BUSINESS_DAILY_TIME = [
    9,
    12,
    13,
    17
]

HOLIDAYS = [
    [2015, 1, 1], # New Year's Day
    [2015, 12, 25], # Christmas Day
]


