from django.core.management.base import BaseCommand, CommandError
from blackrock.portal.models import *

class Command(BaseCommand):
  
  def handle(self, *app_labels, **options):
      people = Person.objects.all()
      
      for person in people:
          parts = person.name.rpartition(' ')
          person.first_name = parts[0]
          person.last_name = parts[2]
          person.save()
     