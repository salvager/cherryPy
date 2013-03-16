#!/usr/bin/env python
import cherrypy
from os import path
from jinja2 import Environment, FileSystemLoader
from RESTAPI import RestAPI

 
current_dir = path.dirname(path.abspath(__file__))
env = Environment(loader=FileSystemLoader(
    path.join(current_dir,'templates'))
)
 
config = {
 '/': {},
}
 

class Root(object):  

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template("root.html")
      	return tmpl.render()

    @cherrypy.expose
    def search(self, **params):
	test = RestAPI()
	tmpl = env.get_template("search.html")
	if 'query' in params:
		parameters = {}
		parameters['originalQuery'] = params['query']
		query = 'text:('+params['query']+')'
		parameters['query'] = query
		if 'page' in params:
			parameters['start'] = int(params['page'])*10;
		test.assignParameters(parameters)
		parameters['numFound'] = test.getresponseParams('numFound')
		parameters['docs'] = test.getresponseParams('docs')
		parameters['noOfPages'] = parameters['numFound']/10
		return tmpl.render(parameters=parameters)	

 
app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.engine.start()
cherrypy.engine.block()
