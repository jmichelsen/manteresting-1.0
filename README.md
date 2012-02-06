Manticore
=========

How to setup
------------

* Install additional requirements: `mysql-python, PIL`

  To install these packages on Fedora, run:

    sudo yum install python26 python26-devel python26-imaging MySQL-devel

  On Ubuntu:

    sudo apt-get install python-mysqldb python-imaging

* Then create a virtual environment:

    python2.6 virtualenv.py env
    . env/bin/activate
    pip install -r requirements/development.txt

* Now, create a MySQL database:

    mysql> create database manteresting charset utf8;
    mysql> grant all on manteresting.* to `manteresting`@`localhost` identified by 'manteresting';

* Run `./manage.py syncdb --migrate`, answer 'no' when it'll ask if you want to create a superuser;
* Run `./manage.py runserver 0.0.0.0:8000 --settings=manticore.settings.development`
* Add `127.0.0.1  dev.manteresting.com` into the `/etc/hosts` on your desktop;
* Open `dev.manteresting.com:8000` in the browser.
* Login using Twitter.
* Make this user a superuser. For example:

    echo 'from django.contrib.auth.models import User;u=User.objects.get(username="svetlyak40wt");u.is_staff=True;u.is_superuser=True;u.save()'

* sudo ln -s `pwd`/configs/nginx.testing.conf /etc/nginx/conf.d/manteresting.com.conf

Updating code on the server
---------------------------

* git pull
* env/bin/pip install -r requirements/testing.txt
* ./manage.py syncdb --migrate
* ./start-daemon.sh

Testing
-------

* First, create a MySQL database for unittests:
    mysql> create database test_manteresting charset utf8;
    mysql> grant all on test_manteresting.* to `manteresting`@`localhost` identified by 'manteresting';
* Next, run `nosetests`;
* or start `tdaemon`, to run unittests automatically after each file saving.


Architecture
------------

This prototype was built using Django and Pinax.

It should store images on Amazon S3 in production. This app could be useful:
[django-storages](http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html).

Design
------

Project uses [Twitter Bootstrap](http://twitter.github.com/bootstrap/) framework for layout and basic design.
Actually, this Pinax's theme https://github.com/pinax/pinax-theme-bootstrap/
does all job.
