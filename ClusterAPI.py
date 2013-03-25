import requests
import json
import itertools
import collections
from collections import OrderedDict

class ClusterAPI:
	def __init__(self):
                self.URI = 'http://LucidN3:8341/sda/v1/client/collections/Test7/documents/retrieval'
                self.Solr_URI = 'http://LucidN4:8888/solr/Test8/select?wt=json'
                self.username = 'administrator'
                self.password = 'foo'
                self.headers = {'content-type': 'application/json'}
                self.SolrParameters = {}
                self.UIParameters = {}
                self.status = ''
                self.response = ''
                self.docs = {}
                self.r = ''
		self.clusterIds = ''
   
        def setClusterId(self):
#		self.clusterIds = ['7914','7970','8024','7909','8027']
		self.clusterIds = ['8061', '7942','8037','8039', '7983']

        def addDupSolrURI(self, field, value):
               self.Solr_URI = self.Solr_URI+'&'+field+'='+str(value)

        def formQuery(self):
		self.SolrParameters['fq'] = 'clusterId:'	
		self.addDupSolrURI('fl','title')
		self.addDupSolrURI('fl','warc_WARC-Target-URI')
		self.addDupSolrURI('fl','tika_description')
		self.addDupSolrURI('fl','tika_title')
		self.addDupSolrURI('fl','warc_hostname')
		self.addDupSolrURI('fl','distanceToCentroid')
#		self.addDupSolrURI('fl','tika_image')
#		self.addDupSolrURI('fl','tika_og:image')
#		self.addDupSolrURI('fl','tika_og_image')
		self.addDupSolrURI('rows',15)
		self.addDupSolrURI('sort','distanceToCentroid+asc')	
		
        def PingURI(self):
		SolrURI = self.Solr_URI

		for eachCluster in self.clusterIds:
			SURI = SolrURI+'&q=clusterId:'+str(eachCluster)
			docs = {}
			r = requests.post(SURI)
			print SURI
			if r.status_code == 200:
				docs = json.loads(r.text, object_pairs_hook=OrderedDict)['response']['docs']
				docs = self.processDuplicates(docs)
				self.docs[eachCluster] = itertools.islice(docs,0,5)
	

        def getClusterData(self):
		self.setClusterId()
		self.formQuery()
		self.PingURI()
		return self.docs

	def processDuplicates(self, docs):
		processed_docs = [] 
		tmp_docs = {}
		for doc in docs:
			if not tmp_docs.has_key(doc['distanceToCentroid']):
				tmp_docs[doc['distanceToCentroid']] = doc
				processed_docs.append(doc)
		return processed_docs
	
#test =  ClusterAPI()
#print test.getClusterData().keys()


