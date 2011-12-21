# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('core_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding model 'Workbench'
        db.create_table('core_workbench', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Category'], unique=True)),
        ))
        db.send_create_signal('core', ['Workbench'])

        # Adding model 'Nail'
        db.create_table('core_nail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workbench', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nails', to=orm['core.Workbench'])),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('core', ['Nail'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Workbench'
        db.delete_table('core_workbench')

        # Deleting model 'Nail'
        db.delete_table('core_nail')


    models = {
        'core.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.nail': {
            'Meta': {'object_name': 'Nail'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'workbench': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nails'", 'to': "orm['core.Workbench']"})
        },
        'core.workbench': {
            'Meta': {'object_name': 'Workbench'},
            'category': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Category']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']
