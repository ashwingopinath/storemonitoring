# from celery import task
import datetime
import pytz
from .models import StoreReport

def filter_store_status(working_hours,store_status_list):
    filtered_list = []
    end_time_local = datetime.datetime.strptime(working_hours['end_time_local'], '%H:%M:%S').time()
    start_time_local = datetime.datetime.strptime(working_hours['start_time_local'], '%H:%M:%S').time()
    print("Start time local",start_time_local)
    print("End time local",end_time_local)
    for store_status in store_status_list:
        print("Timestam Local time: ",store_status['timestamp_local'].time())
        if store_status['timestamp_local'].time() <= end_time_local and store_status['timestamp_local'].time() >= start_time_local:
            filtered_list.append(store_status)
    return filtered_list

def localize_timezone(status, timezone_local = 'America/Chicago'):
    timestamp_utc = datetime.datetime.fromisoformat(status['timestamp_utc'][:-1])
    timestamp_utc = pytz.utc.localize(timestamp_utc)
    timezone_local = pytz.timezone(timezone_local)
    timestamp_local = timestamp_utc.astimezone(timezone_local)
    return {
        'store_id':status['store_id'],
        'status':status['status'],
        'timestamp_local':timestamp_local
    }

def calculate_uptime(store_status_dict,store_working_hours_dict,start_time,end_time):
    uptime = 0
    start_day = start_time.weekday()
    end_day = end_time.weekday()
    print(store_status_dict)
    for weekday in range(start_day,end_day+8): #Adding extra 7 in case end_day is less than start_day
        weekday = weekday%7
        print("Weekday: ",weekday)
        if weekday not in store_status_dict:
            continue
        store_status_weekday = store_status_dict[weekday]
        print("Store status weekday: ",store_status_weekday)
        daily_start_time = datetime.time.min
        daily_end_time = datetime.time.max
        if weekday in store_working_hours_dict:
            daily_start_time = datetime.datetime.strptime(store_working_hours_dict[weekday]['start_time_local'],'%H:%M:%S').time()
            daily_end_time = datetime.datetime.strptime(store_working_hours_dict[weekday]['end_time_local'],'%H:%M:%S').time()
        print("Start time: ",type(start_time)," ",start_time)
        print("Daily start time: ",type(daily_start_time)," ",daily_start_time)
        if weekday == start_day:
            daily_start_time = max(daily_start_time,start_time.time())
        print("Start time: ",end_time)
        if weekday == end_day:
            daily_end_time = min(daily_end_time,end_time.time())
        prev_status = None
        prev_timestamp = daily_start_time
        # prev_timestamp = None
        for store_status in store_status_weekday:
            # status = store_status.get('status')
            status_time_local = store_status.get('timestamp_local').time()
            print("Store status",store_status.get('timestamp_local'))
            if status_time_local < daily_start_time:
                prev_status = store_status.get('status')
                continue
            if status_time_local >= daily_end_time:
                if prev_status == None:
                    prev_status = store_status.get('status')
                break
            if prev_status == None:
                prev_status = store_status.get('status')
            if prev_status=='active':
                timedelta = datetime.datetime.combine(datetime.date.min, status_time_local) - datetime.datetime.combine(datetime.date.min, prev_timestamp)
                uptime += timedelta.total_seconds() // 60
            prev_timestamp = status_time_local
            prev_status = store_status.get('status')
        if prev_status=='active':
            timedelta = datetime.datetime.combine(datetime.date.min, daily_end_time) - datetime.datetime.combine(datetime.date.min, prev_timestamp)
            uptime += timedelta.total_seconds() // 60
    return uptime

def calculate_downtime(store_status_dict,store_working_hours_dict,start_time,end_time):
    downtime = 0
    start_day = start_time.weekday()
    end_day = end_time.weekday()
    print(store_status_dict)
    for weekday in range(start_day,end_day+8): #Adding extra 7 in case end_day is less than start_day
        weekday = weekday%7
        print("Weekday: ",weekday)
        if weekday not in store_status_dict:
            continue
        store_status_weekday = store_status_dict[weekday]
        print("Store status weekday: ",store_status_weekday)
        daily_start_time = datetime.time.min
        daily_end_time = datetime.time.max
        if weekday in store_working_hours_dict:
            daily_start_time = datetime.datetime.strptime(store_working_hours_dict[weekday]['start_time_local'],'%H:%M:%S').time()
            daily_end_time = datetime.datetime.strptime(store_working_hours_dict[weekday]['end_time_local'],'%H:%M:%S').time()
        print("Start time: ",type(start_time)," ",start_time)
        print("Daily start time: ",type(daily_start_time)," ",daily_start_time)
        if weekday == start_day:
            daily_start_time = max(daily_start_time,start_time.time())
        print("Start time: ",end_time)
        if weekday == end_day:
            daily_end_time = min(daily_end_time,end_time.time())
        prev_status = None
        prev_timestamp = daily_start_time
        # prev_timestamp = None
        for store_status in store_status_weekday:
            # status = store_status.get('status')
            status_time_local = store_status.get('timestamp_local').time()
            print("Store status",store_status.get('timestamp_local'))
            if status_time_local < daily_start_time:
                prev_status = store_status.get('status')
                continue
            if status_time_local >= daily_end_time:
                if prev_status == None:
                    prev_status = store_status.get('status')
                break
            if prev_status == None:
                prev_status = store_status.get('status')
            if prev_status=='inactive':
                timedelta = datetime.datetime.combine(datetime.date.min, status_time_local) - datetime.datetime.combine(datetime.date.min, prev_timestamp)
                downtime += timedelta.total_seconds() // 60
            prev_timestamp = status_time_local
            prev_status = store_status.get('status')
        if prev_status=='inactive':
            timedelta = datetime.datetime.combine(datetime.date.min, daily_end_time) - datetime.datetime.combine(datetime.date.min, prev_timestamp)
            downtime += timedelta.total_seconds() // 60
    return downtime

# @task
def create_report(report_id,current_time_utc,store_status,store_working_hours,store_timezone):
    store_status_dict = {}
    timezone_local = 'America/Chicago'
    if store_timezone is not None:
        timezone_local = store_timezone[0].get('timezone_str','America/Chicago')
    # print('Store status: ',store_status)
    for status in store_status:
        status = localize_timezone(status,timezone_local)
        weekday = status['timestamp_local'].weekday()
        # print("Localised status: ",status)
        # print("Weekday: ",weekday)
        if weekday not in store_status_dict:
            print("Weekday inside store_status_dict: ",weekday)
            store_status_dict[weekday] = []
        store_status_dict[weekday].append(status)
        # print(f"Store status after appending for weekday {weekday}: ",store_status_dict[weekday])
    store_working_hours_dict = {}
    if store_working_hours is not None:
        for working_hours in store_working_hours:
            weekday = working_hours['day']
            store_working_hours_dict[weekday] = {'start_time_local':working_hours['start_time_local'], 'end_time_local':working_hours['end_time_local']}
            if weekday in store_status_dict:
                print("Weekday: ",weekday)
                store_status_dict[weekday] = filter_store_status(working_hours,store_status_dict[weekday])
    current_time_local = current_time_utc.astimezone(pytz.timezone(timezone_local))
    print(store_status_dict)
    uptime_last_week = calculate_uptime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(weeks=1))
    downtime_last_week = calculate_downtime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(weeks=1))
    uptime_last_day = calculate_uptime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(days=1))
    downtime_last_day = calculate_downtime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(days=1))
    uptime_last_hour = calculate_uptime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(hours=1))
    downtime_last_hour = calculate_downtime(store_status_dict,store_working_hours_dict,current_time_local,current_time_local - datetime.timedelta(hours=1))

    store_report = StoreReport.objects.get(id=report_id)
    store_report.status = 'Complete'
    store_report.uptime_last_hour = uptime_last_hour
    store_report.downtime_last_hour = downtime_last_hour
    store_report.uptime_last_day = uptime_last_day // 60
    store_report.downtime_last_day = downtime_last_day // 60
    store_report.uptime_last_week = uptime_last_week // 60
    store_report.downtime_last_week = downtime_last_week // 60
    store_report.save()

