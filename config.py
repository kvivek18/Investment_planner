import datetime

JAN = 'January'
FEB = 'February'
MAR = 'March'
APR = 'April'
MAY = 'May'
JUN = 'June'
JUL = 'July'
AUG = 'August'
SEP = 'September'
OCT = 'October'
NOV = 'November'
DEC = 'December'

MONTHS = [JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC]

RECUR = 'Recurring'
ADH = 'Adhoc'
INFLOW = 'Inflow'
OUTFLOW = 'Outflow'

MON_MAP = {
    'January': 0,
    'February': 1,
    'March': 2,
    'April': 3,
    'May': 4,
    'June': 5,
    'July': 6,
    'August': 7,
    'September': 8,
    'October': 9,
    'November': 10,
    'December': 11
}

COLUMNS = ['DATA TYPE', 'FREQUENCY', 'START MONTH', 'START YEAR', 'TIME DURATION', 'VALUE']

REPORT_COLUMNS = ['MONTH', 'TOTAL INFLOW', 'TOTAL OUTFLOW', 'FIXED DEPOSITS']


def end_date(pres_mon, pres_year, time):
    pres_year = int(pres_year + (pres_mon + time) / 12)
    pres_mon = (pres_mon + time) % 12
    return pres_mon, pres_year


def year_check(pres_mon, pres_year, start_mon_glob, start_year_glob, time_dur=0):
    end_mon, end_year = end_date(pres_mon, pres_year, time_dur)
    start_entry_date = datetime.datetime(pres_year, pres_mon + 1, 1)
    end_entry_date = datetime.datetime(end_year, end_mon + 1, 28)
    end_year_date = datetime.datetime(start_year_glob + 1, start_mon_glob + 1, 1)
    if end_entry_date < end_year_date:
        return -1
    if start_entry_date >= end_year_date:
        return 1
    return 0
