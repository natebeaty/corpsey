from fabric.api import *

env.hosts = ['natebeaty.opalstacked.com']
env.user = 'natebeaty'
env.warn_only = True

def deploy(assets='n'):
    with cd('/home/natebeaty/apps/corpsey/corpsey/'):
        # run('/home/natebeaty/.virtualenvs/corpsey_110/bin/activate_this.py')
        run('git pull origin master')
        if assets != 'n':
            run('/home/natebeaty/apps/corpsey/env/bin/python manage.py collectstatic --noinput')
        # run('/home/natebeaty/apps/corpsey/env/bin/python manage.py clear_cache')
        restart()

def syncdb():
    with cd('/home/natebeaty/apps/corpsey/corpsey/'):
        run('/home/natebeaty/apps/corpsey/env/bin/python manage.py syncdb')
        restart()

def migrate():
    with cd('/home/natebeaty/apps/corpsey/corpsey/'):
        run('/home/natebeaty/apps/corpsey/env/bin/python manage.py migrate')
        restart()

def restart():
    run('/home/natebeaty/apps/corpsey/stop')
    run('/home/natebeaty/apps/corpsey/start')
