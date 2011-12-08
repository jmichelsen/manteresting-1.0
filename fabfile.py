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
        run('env/bin/pip install -r requirements.txt')

        if not file_exists('local_settings.py'):
            run('ln -s configs/local_settings/{0}.py local_settings.py'.format(env.type))

def _manage(command):
    def _command():
        with cd(env.project_dir):
            run('./manage.py ' + command)
    return _command

shell = _manage('shell')
dbshell = _manage('dbshell')
runserver = _manage('runserver 0.0.0.0:8000')
