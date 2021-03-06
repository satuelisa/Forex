import datetime

fmt = '%Y-%m-%d-%H'
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

def postpone(t, d):
    original = datetime.datetime.strptime(t, dfmt)
    delay = datetime.timedelta(days = d)
    return (original + delay).strftime(dfmt)

def dt(latter, former):
    dl = datetime.datetime.strptime(latter, fmt)
    df = datetime.datetime.strptime(former, fmt)
    difference = dl - df
    return difference.days * sid + difference.seconds



