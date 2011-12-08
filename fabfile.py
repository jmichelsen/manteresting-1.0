from fabric.api import *
from cuisine import *

def dev():
    env.hosts = ['vbox']
    env.type = 'development'
    env.project_dir = '/vagrant/Manticore'
    use_ssh_config(env)

def create_env():
    with cd(env.project_dir):
        if not dir_exists('env'):
            run('virtualenv env')

        fabfile = 'requirements/{0}.txt'.format(env.type)
        if file_exists(fabfile):
            run('env/bin/pip install -r ' + fabfile)

        if not file_exists('local_settings.py') \
                and file_exists('configs/local_settings/{0}.py'.format(env.type)):
            run('ln -s configs/local_settings/{0}.py local_settings.py'.format(env.type))

def _manage(command):
    def _command():
        with cd(env.project_dir):
            run('./manage.py ' + command)
    return _command

shell = _manage('shell')
dbshell = _manage('dbshell')
runserver = _manage('runserver 0.0.0.0:8000')
syncdb = _manage('syncdb')
