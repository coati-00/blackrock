from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from blackrock.respiration.models import Temperature
import datetime
import os.path
from django.utils import simplejson
from django.core.cache import cache

class ImportTestCases(TestCase):
    #fixtures = ["test_data.json"]
    
    def _login(self, client, uname, pwd):
            # Do a fake login via the handy client login fixture
        self.assert_(client.login(username=uname, password=pwd))
        
        response = client.get('/admin/respiration/')
        self.assertContains(response, 'Respiration', status_code=200)
        
    def setUp(self):
        user = User(username="testuser", is_superuser="t", is_staff="t")
        user.set_password("test")
        user.save()
        
    def tearDown(self):
        User.objects.get(username="testuser").delete()
        Temperature.objects.all().delete()
        
    def test_csv_import(self):
        Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(2008, 6, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(station='Ridgetop', date=datetime.datetime(2008, 7, 1, 1, 00), reading=1.1)
        Temperature.objects.get_or_create(station='Fire Tower', date=datetime.datetime(2008, 8, 1, 1, 00), reading=1.1)

        self._login(self.client, 'testuser', 'test')
        
        response = self.client.get('/admin/respiration/')
        self.assertContains(response, 'Import Respiration Data From CSV', status_code=200)
        
        # test existing data
        qs = Temperature.objects.filter(station='Test Station')
        self.assertEquals(qs.count(), 0)
        
        # Submitting files is a special case. To POST a file, you need only provide the file 
        # field name as a key, and a file handle to the file you wish to upload as a value. 
        # The Test Client will populate the two POST fields (i.e., field and field_file) 
        # required by Django's FileField. For example:
        test_data_file = os.path.join(os.path.dirname(__file__),"test_respiration.csv")
        f = open(test_data_file)
        response = self.client.post('/respiration/loadcsv', {'delete':'on', 'csvfile':f})
        f.close()
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Temperature.objects.filter(station='Test Station').count(), 48)
        self.assertEquals(Temperature.objects.filter(station='Another Station').count(), 24)
        
        # spotcheck
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1996, 12, 31, 00, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -0.72)
        
        # new station with invalid temp, after valid temps, should register as 0 not, the other station's old temp
        qs =Temperature.objects.filter(station='Another Station', date=datetime.datetime(1997, 1, 1, 00, 00))
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, 0)
        
        # Check duplicate handling
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1997, 1, 1, 23, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -0.16)
        
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1997, 1, 1, 22, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -8.0)
        
        # Substituting last valid temp when temp is invalid
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1996, 12, 31, 23, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)
        
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1997, 1, 1, 00, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)
        
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1997, 1, 1, 01, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -2.16)
        
        qs = Temperature.objects.filter(station='Test Station', date=datetime.datetime(1997, 1, 1, 02, 00));
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].reading, -1.06)
        
    def test_solr_fail(self):
      self._login(self.client, 'testuser', 'test')
        
      data = {'base_query': 'http://foo.bar' }
                
      response = self.client.post('/respiration/loadsolr', data)
      
      json = simplejson.loads(response.content)
      self.assertEquals(json['complete'], True)
      self.assertTrue(cache.has_key('solr_complete'))
      self.assertFalse(cache.has_key('solr_deleted'))
      self.assertTrue(cache.has_key('solr_rowcount'))
      self.assertEquals(cache.get('solr_rowcount'), 0)
      self.assertTrue(cache.has_key('solr_error'))
      self.assertEquals(cache.get('solr_error'), '"Key \'station\' not found in <QueryDict: {u\'base_query\': [u\'http://foo.bar\']}>"')
      
      response = self.client.get('/respiration/loadsolrpoll', {})
      json = simplejson.loads(response.content)
      self.assertEquals(json['solr_error'], '"Key \'station\' not found in <QueryDict: {u\'base_query\': [u\'http://foo.bar\']}>"')
      self.assertEquals(json['solr_rowcount'], 0) # "ideal" world count. doesn't include duplicates and such
      
      self.assertFalse(cache.has_key('solr_complete'))
      self.assertFalse(cache.has_key('solr_deleted'))
      self.assertFalse(cache.has_key('solr_rowcount'))
      self.assertFalse(cache.has_key('solr_error'))

        
    def test_solr_import_set(self):
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(2008, 6, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Ridgetop', date=datetime.datetime(2008, 7, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Fire Tower', date=datetime.datetime(2008, 8, 1, 1, 00), reading=1.1)
      
      self.assertEquals(Temperature.objects.filter(station='Open Lowland').count(), 2)
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 1)
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 1)
      self._login(self.client, 'testuser', 'test')
        
      response = self.client.get('/admin/respiration/')
      self.assertContains(response, 'Import Respiration Data from SOLR', status_code=200)
        
      data = {'base_query': 'http://cherrystone.cc.columbia.edu:8181/solr/blackrock/select/?qt=forest-data&collection_id=environmental-monitoring&',
              'import_set': 'OL_2008',
              'delete_data': 'true',
              'station': 'Open Lowland',
              'start_date': '2008-01-01',
              'end_date': '2008-12-31'}
                
      response = self.client.post('/respiration/loadsolr', data)
      
      json = simplejson.loads(response.content)
      self.assertEquals(json['complete'], True)
      
      self.assertTrue(cache.has_key('solr_complete'))
      self.assertFalse(cache.has_key('solr_error'))
      self.assertTrue(cache.has_key('solr_deleted'))
      self.assertEquals(cache.get('solr_deleted'), 1)
      self.assertTrue(cache.has_key('solr_rowcount'))
      self.assertEquals(cache.get('solr_rowcount'), 8784) # "ideal" world count. doesn't include duplicates and such
      
      qs = Temperature.objects.filter(station='Open Lowland').order_by('date')
      self.assertEquals(qs.count(), 8785) # 9151 rows - 365 duplicates 
      self.assertEquals(qs[0].date, datetime.datetime(1997, 1, 1, 1, 0))
      
      self.assertEquals(qs[1].date, datetime.datetime(2008, 1, 1, 0, 0))
      self.assertEquals(qs[1].reading, -2.3799999999999999)
                        
      self.assertEquals(qs[10].date, datetime.datetime(2008, 1, 1, 9, 0))
      self.assertEquals(qs[10].reading, 1.51)
      
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 1)
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 1)
      
      response = self.client.get('/respiration/loadsolrpoll', {})
      json = simplejson.loads(response.content)
      self.assertEquals(json['solr_deleted'], 1)
      self.assertEquals(json['solr_rowcount'], 8784) # "ideal" world count. doesn't include duplicates and such
      
      self.assertFalse(cache.has_key('solr_complete'))
      self.assertFalse(cache.has_key('solr_deleted'))
      self.assertFalse(cache.has_key('solr_rowcount'))
      
      

    # This test takes about 20 minutes to run. I've commented it out for normal testing purposes.
    def x_test_solr_import_all(self):
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(1997, 1, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Open Lowland', date=datetime.datetime(2008, 6, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Ridgetop', date=datetime.datetime(2008, 7, 1, 1, 00), reading=1.1)
      Temperature.objects.get_or_create(station='Fire Tower', date=datetime.datetime(2008, 8, 1, 1, 00), reading=1.1)

      self._login(self.client, 'testuser', 'test')
        
      data = {'base_query': 'http://cherrystone.cc.columbia.edu:8181/solr/blackrock/select/?qt=forest-data&collection_id=environmental-monitoring&',
              'delete_data': 'true',
              'station': 'All',
              'start_date': '2008-01-01',
              'end_date': '2008-12-31'}
                
      response = self.client.post('/respiration/loadsolr', data)
      
      json = simplejson.loads(response.content)
      
      self.assertEquals(json['complete'], True)
      
      self.assertTrue(cache.has_key('solr_complete'))
      self.assertFalse(cache.has_key('solr_error'))
      self.assertTrue(cache.has_key('solr_deleted'))
      self.assertEquals(cache.get('solr_deleted'), 3)
      self.assertTrue(cache.has_key('solr_rowcount'))
      self.assertEquals(cache.get('solr_rowcount'), 43139) # "ideal" world count. doesn't include duplicates and such
      
      query_set = Temperature.objects.extra(select={'count': 'count(1)'}, order_by=['-count', 'station']).values('count', 'station')
      query_set.query.group_by = ['station']
      
      self.assertEquals(Temperature.objects.filter(station='Open Lowland').count(), 16812) # OL_2008 & OL_2009
      self.assertEquals(Temperature.objects.filter(station='Ridgetop').count(), 8784) # RT_
      self.assertEquals(Temperature.objects.filter(station='Fire Tower').count(), 17544)
