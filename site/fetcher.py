import sys
import os
import re
import datetime

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
    # remaining, completed, total = get_totals()
    remaining, completed, total = 97, 10, 107
    print "%s days remaining, %s days total" % (remaining, total)
    effort = Effort(remaining, completed, timestamp=datetime.date(2012, 3, 14))
    # session.add(effort)
    # session.commit()
    
def main(args):
    session = framework.setup_db(settings.DATABASE_URI)
    update(session)
    
if __name__=="__main__":
    sys.exit(main(sys.argv))