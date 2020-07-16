# MONTHS = {'January': 0,
#           'February': 1,
#           'March': 2,
#           'April': 3,
#           'May': 4,
#           'June': 5,
#           'July': 6,
#           'August': 7,
#           'September': 8,
#           'October': 9,
#           'November': 10,
#           'December': 11
#           }
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
