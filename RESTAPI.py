import requests
import json
import itertools

class RestAPI:
	def __init__(self):
		self.URI = 'http://LucidN3:8341/sda/v1/client/collections/VAQuake/documents/retrieval'
		self.Solr_URI = 'http://LucidN4:8888/solr/VAQuake/select?wt=json'
		self.username = 'administrator'
		self.password = 'foo'
		self.headers = {'content-type': 'application/json'}
		self.parameters = {}		
		self.status = ''
		self.response = ''
		self.data = {}
		self.r = ''

	def addToSolrURI(self):
		for each in self.parameters:
			self.Solr_URI = self.Solr_URI+'&'+each+'='+str(self.parameters[each])
		self.Solr_URI = self.Solr_URI+'&facet.field=tika_keywords'+'&facet.field=tika_Content-Type'

	def pingURI(self):
		self.r = requests.post(self.Solr_URI)
		self.status = self.r.status_code
		self.response = json.loads(self.r.text)
		print self.Solr_URI	

	def assignParameters(self, params):
		self.parameters['qf'] = 'tika_title^10 text^5.0'
		self.parameters['hl'] = 'true'
		self.parameters['hl.fl'] = 'text'
		self.parameters['hl.simple.pre']='<em>'
		self.parameters['hl.simple.post']='</em>'
		self.parameters['hl.usePhraseHighlighter']='true'
		self.parameters['hl.fragsize']=300
		self.parameters['hl.mergeContinuous']='true'
		self.parameters['q'] = params['query']
		self.parameters['facet']='true'
		self.parameters['facet.field']='tika_author'
		self.parameters['facet.limit']=6
		self.parameters['facet.mincount']=6
		if 'start' in params:
			self.parameters['start'] = params['start']
#		print self.parameters
		self.data['query'] = self.parameters
		self.data = json.dumps(self.data)
		self.addToSolrURI()
		self.pingURI()		
#		self.requestAPI()
	
	def requestAPI(self):
		self.r = requests.post(url=self.URI,data=self.data,headers=self.headers,auth=(self.username,self.password))
		self.status = self.r.status_code
		self.response = self.r.text
		self.response = json.loads(self.response)

	def getStatus(self):
		return self.status

	def getresponseHeaderParams(self, param):
		return self.response['responseHeader']['params'][param]
	
	def getresponseParams(self, param):
		return self.response['response'][param]
	
	def getHighlights(self):
		return self.response['highlighting']

	def getFacets(self):
		return self.convertFacets()
	
	def convertFacets(self):
		facets = self.response['facet_counts']
		for eachFacet in facets['facet_fields']:
			facets['facet_fields'][eachFacet] = dict(itertools.izip_longest(*[iter(facets['facet_fields'][eachFacet])]*2, fillvalue=""))
		return facets


		

test=RestAPI()
params = {}
params['query'] = 'text:(virginia +earthquake)'
params['start'] = 10
params['rows'] = 20
test.assignParameters(params)
print test.getFacets()
#test.requestAPI()
#print test.status
#print test.getFacets()
#print test.getresponseParams('numFound')
