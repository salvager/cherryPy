import sys
sys.stdout = sys.stderr

#from RESTAPI import RestAPI
from os import path
import atexit
import threading
import cherrypy
from jinja2 import Environment, FileSystemLoader
import requests
import json

cherrypy.config.update({'environment': 'embedded'})

current_dir='/srv/www/wsgi'
env = Environment(loader=FileSystemLoader(path.join(current_dir,'templates')))

root = path.join(path.dirname(__file__), '..')
sys.path.insert(0, root)

class RestAPI:
        def __init__(self):
                self.URI = 'http://LucidN3:8341/sda/v1/client/collections/VAQuake/documents/retrieval'
                self.username = 'administrator'
                self.password = 'foo'
                self.headers = {'content-type': 'application/json'}
                self.parameters = {}
                self.status = ''
                self.response = ''
                self.data = {}
                self.r = ''

        def assignParameters(self, params):
                self.parameters['qf'] = 'tika_title^10 text^5.0'
                self.parameters['q'] = params['query']
                if 'start' in params:
                        self.parameters['start'] = params['start']
                self.data['query'] = self.parameters
                self.data = json.dumps(self.data)
                self.requestAPI()

        def requestAPI(self):
                self.r = requests.post(url=self.URI,data=self.data,headers=self.headers,auth=(self.username,self.password))
                print self.data
                self.status = self.r.status_code
                self.response = self.r.text
                self.response = json.loads(self.response)
                print self.response['QUERY']['json']['response']['docs'][0]['warc_WARC-Target-URI']

        def getStatus(self):
                return self.status

        def getresponseHeaderParams(self, param):
                return self.response['QUERY']['json']['responseHeader']['params'][param]

        def getresponseParams(self, param):
                return self.response['QUERY']['json']['response'][param]

        def getdocs(self):
                 return self.getresponseParams('docs')



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
                return tmpl.render(parameters=parameters)

application = cherrypy.Application(Root(), script_name=None, config=None)
