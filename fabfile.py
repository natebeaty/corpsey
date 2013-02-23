from fabric.api import *

env.hosts = ['corpsey.trubbleclub.com']
env.warn_only = True

def deploy():
    with cd('/home/natebeaty/webapps/django145/corpsey/'):
        run('git pull origin master')
        run('/usr/local/bin/python2.7 manage.py collectstatic --noinput')
        restart()

def syncdb():
    with cd('/home/natebeaty/webapps/django145/corpsey/'):
        run('/usr/local/bin/python2.7 manage.py syncdb')
        # run('../apache2/bin/restart')

def migrate():
    with cd('/home/natebeaty/webapps/django145/corpsey/'):
        run('/usr/local/bin/python2.7 manage.py migrate')

def restart():
    run('/home/natebeaty/webapps/django145/apache2/bin/restart')
