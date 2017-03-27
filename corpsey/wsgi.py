"""
WSGI config for corpsey project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys, site

# Tell wsgi to add the Python site-packages to its path. 
site.addsitedir('/home/natebeaty/.virtualenvs/corpsey_18/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corpsey.settings")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'corpsey.settings'

activate_this = os.path.expanduser("~/.virtualenvs/corpsey_18/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# Calculate the path based on the location of the WSGI script
project = '/home/natebeaty/webapps/django18/corpsey/'
workspace = os.path.dirname(project)
sys.path.append(workspace)

# sys.path.insert(0, '/home/natebeaty/webapps/django15/corpsey')
# sys.path.insert(0, '/home/natebeaty/.virtualenvs/corpsey')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
