Manticore
=========

How to setup
------------

* First, create a MySQL database:
    mysql> create database manteresting charset utf8;
    mysql> grant all on manteresting.* to `manteresting`@`localhost` identified by 'manteresting';
* Run `./manage.py syncdb --migrate`, answer 'no' when it'll ask if you want to create a superuser;
* Run `./manage.py runserver 0.0.0.0:8000`
* Add `127.0.0.1  dev.manteresting.com` into the `/etc/hosts` on your desktop;
* Open `dev.manteresting.com:8000` in the browser.

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
