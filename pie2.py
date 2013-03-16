#!/usr/bin/env python
import cherrypy
 
config = {
 '/': {},
}
 
class Subpage(object):
    @cherrypy.expose
    def index(self):
        return "subpage"
 
    @cherrypy.expose
    def bar(self, p=None, q=None):
        return "Bar: {}, {}".format(p, q)
 
class Root(object):
    subpage = Subpage()
 
    @cherrypy.expose
    def index(self):
        return """
<h2>Root page #2</h2>
<a href='/foo'>/foo</a><br />
<a href='/subpage'>/subpage</a><br />
<a href='/subpage/bar?p=hello&q=there'>/subpage/bar?p=hello&q=there</a><br />
<a href='/subpage/bar/hello/there'>/subpage/bar/hello/there</a><br />
        """
    @cherrypy.expose
    def foo(self):
        return "Foo"
 
app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.engine.start()
cherrypy.engine.block()
