import requests
import json
import itertools
import collections
from collections import OrderedDict
class RestAPI:
	def __init__(self):
		self.URI = 'http://LucidN3:8341/sda/v1/client/collections/Test8/documents/retrieval'
		self.Solr_URI = 'http://LucidN4:8888/solr/Test8/select?wt=json'
		self.username = 'administrator'
		self.password = 'foo'
		self.headers = {'content-type': 'application/json'}
		self.SolrParameters = {}		
		self.UIParameters = {}
		self.status = ''
		self.response = ''
		self.data = {}
		self.r = ''

	def addToSolrURI(self):
		for each in self.SolrParameters:
			self.Solr_URI = self.Solr_URI+'&'+each+'='+str(self.SolrParameters[each])

	def addDupSolrURI(self, field, value):
		self.Solr_URI = self.Solr_URI+'&'+field+'='+value

	def pingURI(self):
		self.r = requests.post(self.Solr_URI)
		self.status = self.r.status_code
		self.response = json.loads(self.r.text, object_pairs_hook=OrderedDict)
#		print json.loads(self.r.text, object_pairs_hook=OrderedDict)
	#	print self.response['response']['docs'][0]['warc_WARC-Target-URI']
	#	print self.response['response']['docs'][1]['warc_WARC-Target-URI']
         # 	print self.response['response']['docs'][2]['warc_WARC-Target-URI']

	def assignStaticParameters(self):
		self.SolrParameters['qf'] = 'tika_title^10 text^5.0'
		self.SolrParameters['hl'] = 'true'
		self.SolrParameters['hl.fl'] = 'text'
                self.SolrParameters['hl.simple.pre'] = '<em>'
                self.SolrParameters['hl.simple.post'] = '</em>'
                self.SolrParameters['hl.usePhraseHighlighter'] = 'true'
                self.SolrParameters['hl.fragsize'] = 150
                self.SolrParameters['hl.mergeContinuous'] = 'true'
                self.SolrParameters['facet'] = 'true'
                self.SolrParameters['facet.limit'] = 8 
                self.SolrParameters['facet.mincount'] = 3
#		self.SolrParameters['rows']=7000
#	        self.addDupSolrURI('facet.field','author_display')
#		self.addDupSolrURI('facet.field','tika_category')
#		self.addDupSolrURI('facet.field','tika_content-type')		
		self.addDupSolrURI('facet.field','domain')
		self.addDupSolrURI('facet.field','clusterId')
		self.addDupSolrURI('facet.field','tika_date')
		self.addDupSolrURI('facet.field','tika_dc_creator')
#		self.addDupSolrURI('facet.field','distanceToCentroid')
		self.addDupSolrURI('fq','warc_status:200')
		self.addDupSolrURI('q.alt','*:*')		

	def assignParameters(self, params):
		self.UIParameters['url'] = params['url']+'?'
		if 'query' in params:
			self.UIParameters['originalQuery'] = params['query']
			self.SolrParameters['q'] = 'text:('+params['query']+')'
			self.UIParameters['url'] = self.UIParameters['url']+'&'+'query='+params['query']
		else:
			self.SolrParameters['q']='*:*'
			self.UIParameters['originalQuery']='*:*'
			self.UIParameters['url'] = self.UIParameters['url']+'&'+'query='+'*:*'
		if 'page' in params:
			self.SolrParameters['start'] = int(params['page'])*10
			self.UIParameters['pagenumber'] = int(params['page'])
		else:
			self.UIParameters['pagenumber'] = 0
		for key, value in params.iteritems():
			if key.startswith('fq'):
				self.UIParameters['fq'] = []
				if type(value).__name__=='list':
					for each in value:
						self.addDupSolrURI('fq',each)
						self.UIParameters['url'] = self.UIParameters['url']+'&'+key+'='+each
						self.UIParameters['fq'].append(each)
				else:
					self.addDupSolrURI('fq',value)
					self.UIParameters['url'] = self.UIParameters['url']+'&'+key+'='+value
					self.UIParameters['fq'].append(value)
		self.assignStaticParameters()
		self.addToSolrURI()
#		print self.Solr_URI
		self.pingURI()

#		print self.parameters
#		self.data['query'] = self.parameters
#		self.data = json.dumps(self.data)
	
	def getResults(self):
		self.UIParameters['numFound'] = self.getresponseParams('numFound')
		self.UIParameters['docs'] = self.getresponseParams('docs')
		self.UIParameters['noOfPages'] = self.UIParameters['numFound']/10
		self.UIParameters['highlights'] = self.getHighlights()
		self.UIParameters['facets'] = self.getFacets()
#		print self.response['response']['docs'][0]['warc_WARC-Target-URI'], self.UIParameters['docs'][0]['warc_WARC-Target-URI']
#		print self.response['response']['docs'][1]['warc_WARC-Target-URI'], self.UIParameters['docs'][1]['warc_WARC-Target-URI']
#		print self.response['response']['docs'][2]['warc_WARC-Target-URI'], self.UIParameters['docs'][2]['warc_WARC-Target-URI']
#	        self.UIParameters['docs'] = self.getSimilardocs();	
		return self.UIParameters		

	def getSimilardocs(self):
		for each in self.UIParameters['docs']:
			response = self.requestAPI(each['id'])
#			if response != "":
#				self.UIParameters['docs']['similarDocs'] = json.loads(response)

	def requestAPI(self, id):
		data = {}
		data['DUPLICATES'] = {"id":id}
		print self.URI, json.dumps(data)
		r = requests.post(url=self.URI, data=json.dumps(data) , headers=self.headers, auth=(self.username,self.password))
		print r.text
		if r.status_code == 200:
			print "status code is", r.status_code
			return r.text
		else:
			return ""

	def getStatus(self):
		return self.status

	def getresponseHeaderParams(self, param):
		return self.response['responseHeader']['params'][param]
	
	def getresponseParams(self, param):
		return self.response['response'][param]
	
	def getHighlights(self):
		if self.response['highlighting'] is not None:
			return self.response['highlighting']
		else:
			return ""
	def getFacets(self):
		return self.convertFacets()
	
	def convertFacets(self):
		facets = self.response['facet_counts']
		for eachFacet in facets['facet_fields']:
			facets['facet_fields'][eachFacet] = dict(itertools.izip_longest(*[iter(facets['facet_fields'][eachFacet])]*2, fillvalue=""))
#			facets['facet_fields'][eachFacet] = OrderedDict(sorted(facets['facet_fields'][eachFacet].items(), key = lambda t:t[0]))
			facets['facet_fields'][eachFacet] = OrderedDict(sorted(facets['facet_fields'][eachFacet].items(), key=lambda t:t[1], reverse=True))	
#		print facets
		return facets


		

test=RestAPI()
params = {}
params['url'] = 'ab'
#params['fl'] = 'warc_WARC-Target-URI'
params['query'] = '*:*'
#params['start'] = 0
params['rows'] = 100
test.assignParameters(params)
test.getResults()
#print test.Solr_URI
#print test.response
#print test.getResults()
#print test.getFacets()
#test.requestAPI()
#print test.status
#print test.getFacets()
#print test.getresponseParams('numFound')
