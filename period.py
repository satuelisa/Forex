import datetime

fmt = '%Y-%m-%d'
dfmt = '%Y-%m-%d'
start = None
end = None

def setStart(y, m, d):
    global start
    start = datetime.datetime(year = y, month = m, day = d)

def setEnd(y, m, d):
    global end
    end = datetime.datetime(year = y, month = m, day = d)  

def getStart():
    return start

def getEnd():
    return end
    
sid = 24 * 60**2

def after(t):
    return datetime.datetime.strptime(t, fmt) >= start

def before(t):
    return datetime.datetime.strptime(t, fmt) <= end

verbose = False
WEEKEND = ['Saturday', 'Sunday']

def postpone(t, d, skipWeekends = False):
    original = datetime.datetime.strptime(t, dfmt)
    if verbose:
        print('in', d, original.strftime('%A'))
    if skipWeekends:
        present = None
        passed = 0
        counter = 0
        while True:
            counter += 1
            present = original + datetime.timedelta(days = counter)
            weekday = present.strftime('%A')
            if not weekday in WEEKEND:
                passed += 1
                if passed == d: # enough days have been skipped
                    if verbose:
                        print('at', weekday, counter)
                    break
        d = counter # we need to skip this many days instead
    final = original + datetime.timedelta(days = d)
    if skipWeekends:
        if verbose:
            print('out', final.strftime('%A'))
        assert final.strftime('%A') not in WEEKEND
    return final.strftime(dfmt)

def dt(latter, former):
    dl = datetime.datetime.strptime(latter, fmt)
    df = datetime.datetime.strptime(former, fmt)
    difference = dl - df
    return difference.days * sid + difference.seconds
