from fabric.api import *

env.hosts = ['corpsey.trubbleclub.com']
env.warn_only = True

def deploy():
    with cd('/home/natebeaty/webapps/django15/corpsey/'):
        # run('/home/natebeaty/.virtualenvs/corpsey_15/bin/activate_this.py')
        run('git pull origin master')
        run('/home/natebeaty/.virtualenvs/corpsey_15/bin/python2.7 manage.py collectstatic --noinput')
        run('/home/natebeaty/.virtualenvs/corpsey_15/bin/python2.7 manage.py clear_cache')
        restart()

def syncdb():
    with cd('/home/natebeaty/webapps/django15/corpsey/'):
        run('/home/natebeaty/.virtualenvs/corpsey_15/bin/python2.7 manage.py syncdb')
        restart()

def migrate():
    with cd('/home/natebeaty/webapps/django15/corpsey/'):
        run('/home/natebeaty/.virtualenvs/corpsey_15/bin/python2.7 manage.py migrate')
        restart()

def restart():
    run('/home/natebeaty/webapps/django15/apache2/bin/restart')
