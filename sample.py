#!/usr/bin/env python
import atexit
import threading

import cherrypy
from jinja2 import Environment, FileSystemLoader
from RESTAPI import RestAPI
from ClusterAPI import ClusterAPI
from os import path
from cherrypy import wsgiserver

current_dir = path.dirname(path.abspath(__file__))
env = Environment(loader=FileSystemLoader(
    path.join(current_dir,'templates'))
)


#config = {
# '/': {},
#}
  

config = {
 '/': {
   'tools.staticdir.root': current_dir,
  },
 '/css': {
   'tools.staticdir.on': True,
   'tools.staticdir.dir': "css",
   },
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
#	if 'query' in params:
	parameters = {}
	for each in params:
		parameters[each] = params[each]	
	parameters['url'] = cherrypy.url()
	test.assignParameters(parameters)
	if test.getStatus() == 200:
		parameters = test.getResults()
		print parameters['numFound'], parameters['noOfPages']
		return tmpl.render(parameters=parameters)	
#	else:
#		return "Error, please enter query";
    @cherrypy.expose
    def default(self, attr='abc'):
	return "Page not Found!"
   
    @cherrypy.expose
    def cluster(self):
	tmpl = env.get_template("root_mod.html")
	tmp = ClusterAPI()
	parameters = tmp.getClusterData()
	return tmpl.render(parameters=parameters)

#server = wsgiserver.CherryPyWSGIServer(('0.0.0.0',8070), Root, server_name='LucidN1')
#server.start()

#application = cherrypy.Application(Root(), script_name=None, config=None)

app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.config.update({'server.socket_host':'0.0.0.0','server.socket_port':9999,})
cherrypy.engine.start()
cherrypy.engine.block()
