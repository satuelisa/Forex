import datetime

fmt = '%Y-%m-%d-%H'
start = datetime.datetime(year = 2017, month = 2, day = 20)
end = datetime.datetime(year = 2017, month = 2, day = 24)
sid = 24 * 60**2

def after(t):
    return datetime.datetime.strptime(t, fmt) >= start

def before(t):
    return datetime.datetime.strptime(t, fmt) <= end

def dt(latter, former):
    dl = datetime.datetime.strptime(latter, fmt)
    df = datetime.datetime.strptime(former, fmt)
    difference = dl - df
    return difference.days * sid + difference.seconds



