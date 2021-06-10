from fabric import task
from invoke import run as local

remote_path = "/home/natebeaty/apps/corpsey/corpsey/"
remote_hosts = ["natebeaty@natebeaty.opalstacked.com"]
git_branch = "master"

# deploy
@task(hosts=remote_hosts)
def deploy(c,assets="no"):
    update(c)
    # `fab deploy --assets=y` to compile new assets
    if assets != "no":
        compile_assets(c)
    clear_cache(c)
    restart(c)

def update(c):
    c.run("cd {} && git pull origin {}".format(remote_path, git_branch))

def compile_assets(c):
    c.run("cd {} && /home/natebeaty/apps/corpsey/env/bin/python manage.py collectstatic --noinput".format(remote_path))

def clear_cache(c):
    c.run("cd {} /home/natebeaty/apps/corpsey/env/bin/python manage.py clearcache".format(remote_path))

def pip(c):
    c.run("cd {} /home/natebeaty/apps/corpsey/env/bin/python -m pip install -r requirements.txt".format(remote_path))

def syncdb(c):
    c.run("cd {} /home/natebeaty/apps/corpsey/env/bin/python manage.py syncdb".format(remote_path))

def migrate(c):
    c.run("cd {} /home/natebeaty/apps/corpsey/env/bin/python manage.py migrate".format(remote_path))

def restart(c):
    c.run("/home/natebeaty/apps/corpsey/stop")
    c.run("/home/natebeaty/apps/corpsey/start")

# local commands
# @task
# def assets(c):
#     local("npx gulp --production")
