from fabric.api import *

env.hosts = ['corpsey.trubbleclub.com']
env.warn_only = True

def deploy():
    with cd('/home/natebeaty/webapps/django14/corpsey/'):
        run('git pull origin master')
        run('python manage.py collectstatic --noinput')
        restart()

def syncdb():
    with cd('/home/natebeaty/webapps/django14/corpsey/'):
        run('python manage.py syncdb')
        # run('../apache2/bin/restart')

def migrate():
    with cd('/home/natebeaty/webapps/django14/corpsey/'):
        run('python manage.py migrate')

def restart():
    run('/home/natebeaty/webapps/django14/apache2/bin/restart')
