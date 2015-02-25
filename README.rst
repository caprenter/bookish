Bookish
=======

.. image:: https://travis-ci.org/Bjwebb/bookish.svg?branch=master
    :target: https://travis-ci.org/Bjwebb/bookish

.. image:: https://requires.io/github/Bjwebb/bookish/requirements.svg?branch=master
     :target: https://requires.io/github/Bjwebb/bookish/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://coveralls.io/repos/Bjwebb/bookish/badge.png?branch=master
    :target: https://coveralls.io/r/Bjwebb/bookish?branch=master

Introduction
------------

This project is a work in progress and does very little at the moment.

Demo
----

    WARNING: All data entered into the demo will be DELETED periodically.

A demo instance is currently available at http://bookish.bjwebb.co.uk/

This has been Deployed using Salt and Docker, see `Deployment`_ for more.

Demo login details
------------------

The demo install is set up with the following accounts:

=============== ===============
username        password
=============== ===============
demo_admin      demo_admin
demo_accountant demo_accountant
demo_client     demo_client
=============== ===============


Local Demo - Using Docker
-------------------------

    WARNING: All data entered into the demo will be DELETED when it stops running.

To run the demo, you must have docker installed: https://docs.docker.com/installation/

However, once you have Docker installed (or if you have it installed already), you only need one command to run the demo:

.. code:: bash

    sudo docker run -p 8000:8000 bjwebb/bookish-demo

This will download the image needed to run the demo, and then end with "Status: Downloaded newer image for bjwebb/bookish-demo:latest".
Once this has happened, the demo site will be available at `http://localhost:8000/ <http://localhost:8000/>`__

If you want, you can choose a port other than 8000 e.g. 1234:

.. code:: bash

    sudo docker run -p 1234:8000 bjwebb/bookish-demo

The demo can then be viewed at `http://localhost:1234/ <http://localhost:1234/>`__

If you've previously run the demo, and want to update it to the latest copy of the code:

.. code:: bash

    sudo docker pull bjwebb/bookish-demo

Local Demo - Without Docker
---------------------------

.. code:: bash

    git clone git@github.com:Bjwebb/bookish.git
    cd bookish
    virtualenv pyenv --python=/usr/bin/python3
    source pyenv/bin/activate
    pip install -r requirements.txt
    cp env.demo .env
    python manage.py migrate
    python manage.py createdemodata
    python manage.py runserver

The demo site should now be available at `http://localhost:8000/ <http://localhost:8000/>`__

Issues encountered with "Local Demo - Without Docker"
-----------------------------------------------------
When you run

.. code:: bash

    virtualenv pyenv --python=/usr/bin/python3

... you get the following error message:

.. code:: bash

	The program 'virtualenv' is currently not installed. You can install it by typing:
	sudo apt-get install python-virtualenv
	
... so, install it:

.. code:: bash
    
	sudo apt-get --yes install python-virtualenv

Then try again:

.. code:: bash

    virtualenv pyenv --python=/usr/bin/python3

If you get an error message:

.. code:: bash

	ERROR: The executable pyenv/bin/python3 could not be run: [Errno 13] Permission denied

This is because the file system it was on an external disk and it doesn't support symlinks properly.

So, create a local directory and try again in there:

.. code:: bash

    virtualenv pyenv --python=/usr/bin/python3


Then:

.. code:: bash

    source pyenv/bin/activate

.. code:: bash

    pip install -r requirements.txt 

If you get a warning and an error:

.. code:: bash

    warning: manifest_maker: standard file '-c' not found

	Error: pg_config executable not found.

	Please add the directory containing pg_config to the PATH
	or specify the full executable path with the option:
	    python setup.py build_ext --pg-config /path/to/pg_config build ...
	or with the pg_config option in 'setup.cfg'.
	
It's because pg_config (a part of PostgreSQL) isn't installed, so install libpq-dev:

.. code:: bash

	sudo apt-get --yes install libpq-dev

Then try again:

.. code:: bash

	pip install -r requirements.txt 


If you get this error:

.. code:: bash

	In file included from psycopg/psycopgmodule.c:27:0:
	
	./psycopg/psycopg.h:30:20: fatal error: Python.h: No such file or directory
	
	 #include <Python.h>
	
	                    ^
	
	compilation terminated.
	
	error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

... it's because it needs python-dev.  So install it.

First, check which version you need to install:

.. code:: bash

	python -V

And install accordingly:

.. code:: bash

	sudo apt-get --yes install python3-dev

...   replacing pyhon-3 with whichever version of python was returned earlier, by:

.. code:: bash

	python -V

Then continue as normal:

.. code:: bash

	pip install -r requirements.txt
	cp env.demo .env
	python manage.py migrate
	python manage.py createdemodata
	python manage.py runserver
	

Installation
------------

* `Install docker <https://docs.docker.com/installation/>`__
* Create a .env file based on https://github.com/Bjwebb/bookish/blob/master/env.example
* ``docker run --rm --env-file=.env bjwebb/bookish python manage.py migrate``
* ``docker run --rm -ti --env-file=.env bjwebb/bookish python manage.py createsuperuser``
* ``docker run --rm -p 8000:8000 --env-file=.env bjwebb/bookish``
* Visit http://localhost:8000/ in your browser.

If you want to build your own docker image (for example if you want to make local changes and then test):

.. code:: bash

    git clone git@github.com:Bjwebb/bookish.git
    cd bookish
    docker build -t bookish .
    cp env.example .env # and edit
    docker run --rm --env-file=.env bookish python manage.py migrate
    docker run --rm -ti --env-file=.env bookish python manage.py createsuperuser
    docker run --rm -p 8000:8000 --env-file=.env bookish

* Visit http://localhost:8000/ in your browser.

If you want to run the code without docker:

.. code:: bash

    git clone git@github.com:Bjwebb/bookish.git
    cd bookish
    virtualenv pyenv --python=/usr/bin/python3
    source pyenv/bin/activate
    pip install -r requirements.txt
    cp env.example .env # and edit
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

* Visit http://localhost:8000/ in your browser.


Setting up a postgres database
------------------------------

.. code:: bash

    sudo -u postgres createuser bookish -P
    sudo -u postgres createdb bookish -O bookish -E utf8

The first command will prompt for a password, it's probably best to use a random one (e.g. generated by ``openssl rand -hex 32``).


Setting up your local system for development
--------------------------------------------

Set up flake8 to run on every git commit:

.. code:: bash

    flake8 --install-hook

Running the tests
-----------------

Ensure you have the requirements for the tests installed:

.. code:: bash

    source pyenv/bin/activate
    pip install -r requirements_test.txt

Then run the tests:

.. code:: bash

    SECRET_KEY=test DATABASE_URL=sqlite:///test.db py.test --ignore=pyenv

Deployment
----------

We will make deployments of Bookish using `Salt <http://docs.saltstack.com/en/latest/>`__. Currently there are no production deployments of Bookish. However, the demo deployment is made using `this salt state <https://github.com/Bjwebb/bookish/blob/master/salt/bookish.sls>`__.
