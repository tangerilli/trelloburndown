import simplejson as json
import datetime
import math

import cherrypy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, DateTime

from framework import Base

class Effort(Base):
    __tablename__ = 'effort'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    remaining = Column(Integer)
    completed = Column(Integer)
    
    def __init__(self, remaining, completed, timestamp=None):
        Base.__init__(self)
        self.remaining = remaining
        self.completed = completed
        if timestamp:
            self.timestamp = timestamp
            
    def to_dict(self):
        return {"timestamp":self.timestamp.strftime("%Y-%m-%d"),
                "remaining":self.remaining,
                "completed":self.completed}
            
class Sprint(Base):
    __tablename__ = 'sprints'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    def __init__(self, name="", start_date=None, end_date=None):
        self.name = name
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
            
    def date_to_json(self, date):
        if date:
            return date.strftime("%Y-%m-%d")
        else:
            return ""
    
    def json_to_date(self, data):        
        if data:
            return datetime.datetime(*[int(n) for n in data.split("-")])
        return None
            
    def to_dict(self):        
        data = {"id":self.id,
                "name":self.name,
                "start_date":self.date_to_json(self.start_date),
                "end_date":self.date_to_json(self.end_date)}
        if self.start_date and self.end_date:
            # TODO: Refactor this to be less horrible
            effort_qry = cherrypy.request.db.query(Effort).filter(Effort.timestamp >= self.start_date).filter(Effort.timestamp <= self.end_date)
            actual_efforts = {}
            for effort in effort_qry:
                actual_efforts[effort.timestamp.date()] = effort
            ideal_remaining = effort_qry.first().remaining
            per_day = float(ideal_remaining) / ((self.end_date - self.start_date).days)
            date = self.start_date.date()
            efforts = []
            one_day = datetime.timedelta(days=1)
            while date <= self.end_date.date():
                effort = {"ideal":math.floor(ideal_remaining), "timestamp":self.date_to_json(date)}
                ideal_remaining = max(ideal_remaining-per_day, 0)
                if date in actual_efforts:
                    effort["remaining"] = actual_efforts[date].remaining
                else:
                    effort["remaining"] = None
                efforts.append(effort)
                date += one_day
            data["efforts"] = efforts
        return data
                
    def from_dict(self, data):
        self.name = data.get("name", self.name)
        self.start_date = self.json_to_date(data.get("start_date", self.start_date))
        self.end_date = self.json_to_date(data.get("end_date", self.end_date))
    