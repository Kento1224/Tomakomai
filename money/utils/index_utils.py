def calc_month_pay(money):
    total = 0
    for m in money:
        total += m.cost
    return total
    
def format_date(money):
    for m in money:
        date = str(m.use_date).split(' ')[0]
        m.use_date = '/'.join(date.split('-')[1:3])
    return None

def get_next(year, month):
    year = int(year)
    month = int(month)
    
    if month == 12:
        return str(year + 1), '1'
    else:
        return str(year), str(month + 1)

def get_prev(year, month):
    year = int(year)
    month = int(month)
    if month == 1:
        return str(year - 1), '12'
    else:
        return str(year), str(month - 1)