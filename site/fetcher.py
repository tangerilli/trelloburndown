import sys
import os
import re
import datetime
import time
from optparse import OptionParser

import requests
import simplejson as json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import settings
import framework
from models import Effort

def board_url():
    return os.path.join(settings.TRELLO_API_URL, "boards", settings.BOARD_ID)

def add_params(url):
    params = "?key=%s&token=%s" % (settings.API_KEY, settings.USER_TOKEN)
    return url + params

def cards_url():
    return os.path.join(board_url(), "cards")    

def lists_url():
    return os.path.join(board_url(), "lists")    

def get_totals():
    """Returns a tuple containing the remaining effort, the completed effort and the total effort"""
    remaining = 0
    completed = 0
    total = 0
    
    # TODO: Add some error checking
    response = requests.get(add_params(lists_url()))
    lists = json.loads(response.content)
    for l in lists:
        for card in l["cards"]:
            m = re.search("\((\d+)\)", card["name"])
            if m:
                effort = int(m.groups(1)[0])
                total += effort
                if l["name"] in settings.NOT_DONE_LISTS:
                    remaining += effort
                if l["name"] in settings.DONE_LISTS:
                    completed += effort
    return (remaining, completed, total)

def update(session):
    remaining, completed, total = get_totals()
    print "%s days remaining, %s days total" % (remaining, total)
    effort = Effort(remaining, completed)
    session.add(effort)
    session.commit()
    
def main(args):
    parser = OptionParser()
    parser.add_option("-d", "--daemon", dest="daemon", action="store_true", 
                      help="Script will run forever, periodically updating")
    parser.add_option("-f", "--frequency", dest="frequency", default=60*24, type="int",
                      help="Frequency (in min) to update in daemon mode (default=%s (24 hours))" % (60*24))
    parser.add_option("-t", "--time", dest="time", 
                      help="The time (format: HH:MM) to update in daemon mode (overrides frequency)")
    (options, args) = parser.parse_args()
    
    session = framework.setup_db(settings.DATABASE_URI)
    if options.daemon:
        while True:
            if options.time:
                target_h, target_m = [int(i) for i in options.time.split(":")]
                n = datetime.datetime.now()
                if target_h < n.hour or (target_h == n.hour and target_m <= n.minute):
                    target_time = n + datetime.timedelta(days=1)
                    target_time = target_time.replace(hour=target_h, minute=target_m)
                    diff = target_time - n
                    sleep_time = (diff.days*60*60*24) + diff.seconds
                else:
                    sleep_time = ((target_h - n.hour)*60*60) + ((target_m - n.minute)*60) - n.second
            else:
                sleep_time = options.frequency*60
            print "Sleeping for %s minutes" % (sleep_time/60.0)
            time.sleep(sleep_time)
            update(session)
    else:
        update(session)
    
if __name__=="__main__":
    sys.exit(main(sys.argv))