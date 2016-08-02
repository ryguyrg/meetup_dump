import json
import urllib2
import datetime
import csv
import os
import sys


api_key = os.environ.get('MEETUP_API_KEY', None)

if not api_key:
  print("No MEETUP_API_KEY specified in env")
  exit(-1)

 
data = json.load(urllib2.urlopen('https://api.meetup.com/2/groups?topic=neo4j&key=%s' % (api_key)))
 
field_names = [
  'group_id', 
  'group_name', 
  'event_id', 
  'event_name', 
  'event_rsvps', 
  'event_time'
]
 
#csvfile = open('events.csv', 'w')
csvfile = sys.stdout

writer = csv.DictWriter(csvfile, fieldnames=field_names)
writer.writeheader()
 
for result in data['results']:
  group_name = result['name']
  group_id = result['id']
#  url = "https://api.meetup.com/2/events?group_id=%s&status=past&time=%s&key=%s" % (result['id'], '1420099200000,', api_key)
  url = "https://api.meetup.com/2/events?group_id=%s&status=past&time=%s&key=%s" % (result['id'], '1388534400000,', api_key)
  events = json.load(urllib2.urlopen(url))
  for event in events['results']:
    event_id = event['id']
    event_name = event['name']
    event_rsvps = event['yes_rsvp_count']
    event_time = event['time']
    utc_offset = event['utc_offset']
    event_local_time = (event_time + utc_offset) / 1000
    event_local_time_str = datetime.datetime.utcfromtimestamp(int(event_local_time)).strftime('%Y-%m-%d %H:%M:%S')
    event_row = {
      'group_name': group_name.encode('utf-8'),
      'group_id': group_id,
      'event_id': event_id,
      'event_name': event_name.encode('utf-8'),
      'event_rsvps': event_rsvps,
      'event_time': event_local_time_str
    }
    writer.writerow(event_row)
