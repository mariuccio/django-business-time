from datetime import timedelta, date, datetime, time
from django.conf import settings

if hasattr(settings, 'WORK_ON_SATURDAY'):
    WORK_ON_SATURDAY = settings.WORK_ON_SATURDAY
else:
    WORK_ON_SATURDAY = False

if hasattr(settings, 'HOLIDAYS'):
    HOLIDAYS = []
    for holiday in settings.HOLIDAYS:
        HOLIDAYS.append(date(holiday[0],holiday[1],holiday[2]))
else:
    HOLIDAYS = [
        date(2015,12,25),
        date(2016,1,1)
    ]

if hasattr(settings, 'BUSINESS_DAILY_TIME'):
    BUSINESS_DAILY_TIME = (
        time(settings.BUSINESS_DAILY_TIME[0]),
        time(settings.BUSINESS_DAILY_TIME[1]),
        time(settings.BUSINESS_DAILY_TIME[2]),
        time(settings.BUSINESS_DAILY_TIME[3])
    )
else:
    BUSINESS_DAILY_TIME = (
        time(9),
        time(12),
        time(12),
        time(17),
    )

MORNING_TIMEDELTA = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[1]) - datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[0])
AFTERNOON_TIMEDELTA = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[3]) - datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[2])

# Working time per day in datetime.timedelta
BUSINESS_DAILY_TIMEDELTA = MORNING_TIMEDELTA + AFTERNOON_TIMEDELTA


def is_holiday(dt):
    if dt.date() in HOLIDAYS: return True
    else: return False


def is_saturday(dt):
    if dt.weekday() == 5: return True
    else: return False


def is_sunday(dt):
    if dt.weekday() == 6: return True
    else: return False


def convert_datetime(dt):

    # HACK: to make math with times we need to convert them in datetimes
    dtbdt = datetime.combine(datetime.min.date(), dt.time())
    dtbdt0 = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[0])
    dtbdt1 = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[1])
    dtbdt2 = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[2])
    dtbdt3 = datetime.combine(datetime.min.date(), BUSINESS_DAILY_TIME[3])
    break_dt = datetime.combine(datetime.min.date(), timedelta_to_time(dtbdt2,dtbdt1))
    workday_dt = datetime.combine(datetime.min.date(), timedelta_to_time(dtbdt3,dtbdt0))
    curr_dt = datetime.combine(datetime.min.date(), timedelta_to_time(dtbdt,dtbdt0))

    # If before work
    if dt.time() < BUSINESS_DAILY_TIME[0]:
        dt = datetime(dt.year,dt.month,dt.day,0,0,0,0)

    # If during morning work time
    elif BUSINESS_DAILY_TIME[0] <= dt.time() < BUSINESS_DAILY_TIME[1]:
        dt = datetime.combine(dt.date(), timedelta_to_time(dtbdt,dtbdt0))

    # If during lunch time
    elif BUSINESS_DAILY_TIME[1] <= dt.time() < BUSINESS_DAILY_TIME[2]:
        dt = datetime.combine(dt.date(), timedelta_to_time(dtbdt1,dtbdt0))

    # If during afternoon work time
    elif BUSINESS_DAILY_TIME[2] <= dt.time() < BUSINESS_DAILY_TIME[3]:
        dt = datetime.combine(dt.date(), timedelta_to_time(curr_dt, break_dt))

    # If after work
    elif dt.time() >= BUSINESS_DAILY_TIME[3]:
        dt = datetime.combine(dt.date(), timedelta_to_time(workday_dt, break_dt))
    return dt


# it calculates the business time difference between 2 datetime entities
def business_timedelta(dt1, dt2):
    if dt2 > dt1:
        dt1 = convert_datetime(dt1)
        dt2 = convert_datetime(dt2)
        if dt1.date() == dt2.date():
            return dt2-dt1
        else:
            return business_time_after(dt1) + business_time_before(dt2) + (BUSINESS_DAILY_TIMEDELTA * business_days_between(dt1,dt2))
    else:
        return timedelta(0,0,0,0,0,0,0)


def business_time_after(dt):
    dt_end = datetime.combine(dt.date(),BUSINESS_DAILY_TIME[3])
    return dt_end - dt


def business_time_before(dt):
    dt_start = datetime.combine(dt.date(),BUSINESS_DAILY_TIME[0])
    return dt - dt_start


def business_days_between(dt1,dt2):

    t = timedelta(days=1)
    dtiterator = dt1 + t
    business_days = 0
    while dtiterator.date() < dt2.date():
        if not is_holiday(datetime.combine(dtiterator.date(), datetime.min.time())) and not (is_saturday(dtiterator) and not WORK_ON_SATURDAY) and not is_sunday(dtiterator):
            business_days += 1
        dtiterator += t

    return business_days


def timedelta_to_time(t1,t2):
    return (datetime.min + (t1 - t2)).time()
