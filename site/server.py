import sys
import os

import cherrypy
import simplejson as json

import settings
import framework
from models import Effort, Sprint


def html_or_json(handler):
    def wrapper(*args, **kwargs):
        if "json" not in cherrypy.request.headers["Accept"]:
            return open(os.path.join(settings.HTMLDIR, "index.html")).read()
        return handler(*args, **kwargs)
    return wrapper

class Resource(object):
    @cherrypy.expose
    def default(self, *args, **kwargs):
        m = cherrypy.request.method.upper()
        if len(args) > 0 and hasattr(self, "_children"):
            c = self._children(args[0])
            return c.default(*args[1:], **kwargs)
        if hasattr(self, m) and callable(getattr(self, m)):
            return getattr(self, m)(*args, **kwargs)
        raise cherrypy.HTTPError(405)

class SprintResource(Resource):
    exposed = True
    
    def __init__(self, id):
        self.id = id
    
    @html_or_json
    def GET(self):    
        sprint = cherrypy.request.db.query(Sprint).filter_by(id=self.id).first()        
        return json.dumps(sprint.to_dict()) 
    
    def DELETE(self):
        sprint = cherrypy.request.db.query(Sprint).filter_by(id=self.id).first()
        cherrypy.request.db.delete(sprint)
        return ""
        
    def PUT(self):
        data = json.loads(cherrypy.request.body.read())
        sprint = cherrypy.request.db.query(Sprint).filter_by(id=self.id).first()
        sprint.from_dict(data)
        return json.dumps(sprint.to_dict()) 

class Sprints(Resource):
    _children = SprintResource
    
    @html_or_json
    def GET(self):
        qry = cherrypy.request.db.query(Sprint)
        
        cherrypy.response.headers['Content-Type']= 'application/json'
        return json.dumps([sprint.to_dict() for sprint in qry.all()])
        
    def POST(self):
        data = json.loads(cherrypy.request.body.read())
        sprint = Sprint()
        sprint.from_dict(data)
        cherrypy.request.db.add(sprint)
        return json.dumps(sprint.to_dict())
        
class Root(Resource):
    sprints = Sprints()
    
    def GET(self):
        return open(os.path.join(settings.HTMLDIR, "index.html")).read()

def main(argv):
    framework.SAEnginePlugin(cherrypy.engine, settings.DATABASE_URI).subscribe()
    cherrypy.tools.db = framework.SATool()
    
    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': os.path.join(settings.CURRENTDIR, 'static')},
            '/': {'tools.db.on': True}}
    cherrypy.quickstart(Root(), "/", config=conf)
    #, 'request.dispatchs': cherrypy.dispatch.MethodDispatcher()

if __name__=="__main__":
    sys.exit(main(sys.argv))