Bookish
-------

This project is a work in progress and does very little at the moment.

However, if you really want to run it:

* `Install docker <https://docs.docker.com/installation/>`__
* ``docker run --rm -p 8000:8000 bjwebb/bookish``
* Visit http://localhost:8000/ in your browser.

If you want to build your own docker image (for example if you want to make local changes and then test):

.. code:: bash

    git clone git@github.com:Bjwebb/bookish.git
    cd bookish
    docker build -t bookish .
    docker run --rm -p 8000:8000 bookish

* Visit http://localhost:8000/ in your browser.

If you want to run the code without docker:

.. code:: bash

    git clone git@github.com:Bjwebb/bookish.git
    cd bookish
    virtualenv pyenv
    source pyenv/bin/activate
    pip install -r requirements.txt
    python manage.py runserver

* Visit http://localhost:8000/ in your browser.
