# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'GridSquare.display_this_square'
        db.add_column('mammals_gridsquare', 'display_this_square', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'GridSquare.display_this_square'
        db.delete_column('mammals_gridsquare', 'display_this_square')


    models = {
        'mammals.gridpoint': {
            'Meta': {'object_name': 'GridPoint'},
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mammals.gridsquare': {
            'Meta': {'object_name': 'GridSquare'},
            'NE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SW'", 'to': "orm['mammals.GridPoint']"}),
            'NW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SE'", 'to': "orm['mammals.GridPoint']"}),
            'SE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NW'", 'to': "orm['mammals.GridPoint']"}),
            'SW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NE'", 'to': "orm['mammals.GridPoint']"}),
            'center': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_i_am_in'", 'to': "orm['mammals.GridPoint']"}),
            'display_this_square': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {}),
            'label_2': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mammals']
