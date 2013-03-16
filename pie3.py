#!/usr/bin/env python
import cherrypy
from os import path
from jinja2 import Environment, FileSystemLoader
 
current_dir = path.dirname(path.abspath(__file__))
env = Environment(loader=FileSystemLoader(
    path.join(current_dir,'templates3'))
)
 
config = {
 '/': {},
}
 
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
 
app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.engine.start()
cherrypy.engine.block()
