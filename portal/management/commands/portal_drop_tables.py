from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from optparse import make_option

class Command(BaseCommand):
  
  option_list = BaseCommand.option_list + (
     make_option('--static',
         dest='static',
         default=False,
         help='clear static tables', 
         action='store_const', 
         const=True),
     )
  
  
  def handle(self, *app_labels, **options):
     cursor = connection.cursor()
     
     asset_tables = ['portal_learningactivity_url',
                     'portal_learningactivity_digital_format',
                     'portal_learningactivity_digital_object',
                     'portal_learningactivity_audience',       
                     'portal_learningactivity_author',         
                     'portal_learningactivity_dataset',        
                     'portal_learningactivity_facet',        
                     'portal_learningactivity_location',       
                     'portal_learningactivity_person',
                     'portal_learningactivity_tag',
                     'portal_learningactivity', 
                     
                     'portal_researchproject_audience',        
                     'portal_researchproject_dataset',         
                     'portal_researchproject_digital_object',  
                     'portal_researchproject_facet',         
                     'portal_researchproject_location',        
                     'portal_researchproject_person',          
                     'portal_researchproject_publication',
                     'portal_researchproject_tag',          
                     'portal_researchproject',  
                     
                     'portal_publication_audience',            
                     'portal_publication_dataset',             
                     'portal_publication_facet',             
                     'portal_publication_location',            
                     'portal_publication_person',
                     'portal_publication_publication_type',
                     'portal_publication_rights_type',
                     'portal_publication_tag',              
                     'portal_publication', 
                                         
                     'portal_digitalobject_audience',          
                     'portal_digitalobject_author',  
                     'portal_digitalobject_digital_format',            
                     'portal_digitalobject_facet',           
                     'portal_digitalobject_location',
                     'portal_digitalobject_tag',
                     'portal_digitalobject',                   
                           
                     'portal_dataset_url',    
                     'portal_dataset_audience',                
                     'portal_dataset_facet',                 
                     'portal_dataset_location',                
                     'portal_dataset_person',
                     'portal_dataset_rights_type',
                     'portal_dataset_tag',
                     'portal_dataset',                         
                                       
                     'portal_person_institution',   
                     'portal_person_audience',                 
                     'portal_person_facet',
                     'portal_person_person_type',
                     'portal_person_tag',
                     'portal_person',
                     
                     'portal_station_audience',
                     'portal_station_location',                
                     'portal_station_facet',
                     'portal_station_tag',       
                     'portal_station',    
                     
                     'portal_region_audience',
                     'portal_region_facet',
                     'portal_region_tag',
                     'portal_region_location',
                     'portal_region_region_type',
                     'portal_region',
                                          
                     'portal_location_audience',               
                     'portal_location_facet',
                     'portal_location_tag',
                     'portal_location_location_subtype',
                     'portal_location_location_type',                      
                     'portal_location'
                     
                     ]   
  
     for table in asset_tables:
        cmd = "drop table if exists %s" % table
        print cmd
        cursor.execute(cmd);
                
     if options.get('static'):
        print "Dropping static tables"
     
        static_tables = ['portal_audience',
                        'portal_digitalformat',                   
                        'portal_facet',                         
                        'portal_institution',
                        'portal_locationsubtype',                 
                        'portal_locationtype',
                        'portal_persontype',
                        'portal_publicationtype',                     
                        'portal_rightstype',
                        'portal_regiontype',
                        'portal_tag',
                        'portal_url']
       
        for table in static_tables:
           cmd = "drop table if exists %s" % table
           print cmd
           cursor.execute(cmd);
          
        
     transaction.commit_unless_managed()
   
      
        
        
        
         
  