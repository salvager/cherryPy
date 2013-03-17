#!/usr/bin/env python
import atexit
import threading

import cherrypy
from jinja2 import Environment, FileSystemLoader
from RESTAPI import RestAPI
from os import path
from cherrypy import wsgiserver

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
			parameters['start'] = int(params['page'])*10
			parameters['pagenumber'] = int(params['page'])
		else:
			parameters['pagenumber'] = 0
		test.assignParameters(parameters)
		parameters['numFound'] = test.getresponseParams('numFound')
		parameters['docs'] = test.getresponseParams('docs')
		parameters['noOfPages'] = parameters['numFound']/10
		parameters['highlights'] = test.getHighlights()
		parameters['facets'] = test.getFacets()
		return tmpl.render(parameters=parameters)	

    @cherrypy.expose
    def default(self, attr='abc'):
	return "Page not Found!"


#server = wsgiserver.CherryPyWSGIServer(('0.0.0.0',8070), Root, server_name='LucidN1')
#server.start()

#application = cherrypy.Application(Root(), script_name=None, config=None)

app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':9999,})
cherrypy.engine.start()
cherrypy.engine.block()
