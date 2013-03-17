import sys
sys.stdout = sys.stderr

from os import path
import atexit
import threading
import cherrypy
from jinja2 import Environment, FileSystemLoader

cherrypy.config.update({'environment': 'embedded'})

current_dir='/srv/www/wsgi'
env = Environment(loader=FileSystemLoader(path.join(current_dir,'templates3')))

class Subpage(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template("subpage.html")
        return tmpl.render()
 
    @cherrypy.expose
    def bar(self, p=None, q=None):
        tmpl = env.get_template("bar.html")
        return tmpl.render(p=p, q=q)
 
class Root(object):
    subpage = Subpage()
 
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template("root.html")
        return tmpl.render()
 
    @cherrypy.expose
    def foo(self):
        tmpl = env.get_template("foo.html")
        return tmpl.render()

application = cherrypy.Application(Root(), script_name=None, config=None)
