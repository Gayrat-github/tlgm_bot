import datetime as dt
import json

def get_delta(start, delta):
    if delta == "month":
        m = start.month
        y = start.year
        if m == 12:
            m = 1
            y += 1
            return start.replace(year=y, month=m) - start
        else:
            return start.replace(month=m+1) - start
    elif delta == "day":
        return dt.timedelta(days=1)
    elif delta == "hour":
        return dt.timedelta(hours=1)

def get_data(db, req_data):
    begin_dt = req_data.dt_from
    end_dt = req_data.dt_upto
    deviation = req_data.group_type
    cur_dt = begin_dt
    dataset = []
    labels = []

    while cur_dt <= end_dt:
        total_payments = 0
        next_dt = cur_dt + get_delta(cur_dt, deviation)
        if next_dt > end_dt:
            next_dt = end_dt

        for x in db.find({}):
            if cur_dt <= x["dt"] < next_dt:
                total_payments += x["value"]

        dataset.append(total_payments)
        labels.append(cur_dt.isoformat())

        cur_dt +=  get_delta(cur_dt, deviation)
    result = {"dataset":dataset, "labels":labels}
    return json.dumps(result)
