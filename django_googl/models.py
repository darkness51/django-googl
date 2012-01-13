import urllib
import urllib2

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.utils import simplejson as json

from .exceptions import GooglException

# Create your models here.
class StringHolder(models.Model):
    """
    A helper model that allows you to create a Bittle with just a URL in a
    string rather than a Django object defining get_absolute_url().
    """
    absolute_url = models.URLField(verify_exists=True)

    def __unicode__(self):
        return u"StringHolder object for %s" % self.absolute_url

    def get_absolute_url(self):
        return self.absolute_url
        
class GooglManager(models.Manager):
    """
    Custom manager for 'Googl' model.
    
    Defines methods to provide shortcuts for creation and management of
    Goo.gl links to local objects
    """
    
    def googlfy(self. obj):
        """
        Creates a new 'Googl' object based on the object pased to it.
        The object must have a 'get_absolute_url' in order for this to 
        work.
        """
        
        if isinstance(obj, basestring):
            obj, created = StringHolder.objects.get_or_create(absolute_url=obj)
            
        # If the object does not have a get_absolute_url() method or the
        # Goo.gl API authentication settings are not in settings.py, fail.