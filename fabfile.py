from fabric.api import *

env.hosts = ['corpsey.trubbleclub.com']
env.warn_only = True

def deploy():
    with cd('/home/natebeaty/webapps/django14/corpsey/'):
        run('git pull origin master')
        run('python manage.py collectstatic --noinput')
        run('../apache2/bin/restart')
