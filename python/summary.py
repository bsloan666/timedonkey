#!/usr/bin/env python
import os
import sys
import re
import time
import datetime


def parse_record(in_str):
    """
    Read an event from the activity log
    """
    fields = re.split(',', in_str)
    timestamp = int(time.mktime(datetime.datetime.strptime(fields[0], "%Y-%m-%d %H:%M:%S").timetuple()))
    app = fields[1]
    action = fields[2]
    arg = fields[3].strip()
    date = datetime.datetime.fromtimestamp(timestamp)
    day = ' '.join(re.split(' ', date.ctime())[0:3])
   

    return {
        'timestamp':timestamp,
        'app':app,
        'action':action,
        'arg':arg,
        'day': day
    }


def parse_slice(index, records):
    """
    For an open event as position index in the table, find the duration of the
    activity and associated args. 
    """
    start = parse_record(records[index])
    arg = None
    result = {'app': start['app'], 'arg': start['arg'], 'day':start['day'], 'elapsed':0}
    for line in records[index+1:]:
        tmp = parse_record(line)
        if tmp['app'] == start['app']:
            if tmp['action'] == 'save':
                result['arg'] = tmp['arg']
            elif tmp['action'] == 'close':
                result['elapsed'] = tmp['timestamp'] - start['timestamp']
                return result
    return result            


def tally_hours(lines):
    """
    Sum the slices dedicated to a particular task
    """
    tasks = {} 
    for i,line in enumerate(lines):
        record = parse_record(line)
        if record['action'] == 'open':
            if record['day'] not in tasks.keys():
                tasks[record['day']] = {}
            if record['app'] not in tasks[record['day']].keys():
                tasks[record['day']][record['app']] = {}
            task = parse_slice(i, lines)
            if task['arg'] in tasks[record['day']][record['app']].keys():
                tasks[record['day']][record['app']][task['arg']] += task['elapsed']
            else:
                tasks[record['day']][record['app']][task['arg']] = task['elapsed']
    return tasks


if __name__ == "__main__":
    with open(os.path.join(os.getenv('HOME'), '.activitylog'), 'r') as handle:
        lines = handle.readlines()
        totals = tally_hours(lines)
        for day, times in totals.items():
            print("{0}:".format(day))
            for app, detail in times.items():
                print("    {0}:".format(app))
                for target, diff in detail.items():
                    hrs = diff//3600
                    mins =  (diff-(diff//3600 * 3600))//60
                    if 15 < mins < 45:
                        hrs += 0.5
                    elif mins >= 45:
                        hrs += 1
                    if hrs:
                        print("        {0:2.1g}h {1}".format(hrs, target)) 
                            
