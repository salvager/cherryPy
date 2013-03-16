import requests
import json

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
		self.status = self.r.status_code
		self.response = self.r.text
		self.response = json.loads(self.response)	

	def getStatus(self):
		return self.status

	def getresponseHeaderParams(self, param):
		return self.response['QUERY']['json']['responseHeader']['params'][param]
	
	def getresponseParams(self, param):
		return self.response['QUERY']['json']['response'][param]

	def getdocs(self):
		 return self.getresponseParams('docs')


#test=RestAPI()
#params = {}
#params['query'] = 'text:(virginia +earthquake)'
#params['start'] = 10
#params['rows'] = 20
#test.assignParameters(params)
#test.requestAPI()
#if test.status != 200:
#	print test.response
#else:
#	print test.status
#	print test.response['QUERY']['json']['responseHeader']['params']
