=====
DoIt!
=====

Installation
------------

.. code-block:: bash

    $ Create your virtualenv (recommended, use virtualenvwrapper)
    $ mkvirtualenv doit

    $ # Clone repository
    $ git clone git@github.com:EnTeQuAk/doit.git

    $ # Activate Environment and install
    $ workon doit
    $ make develop

    $ # run tests
    $ make test


Edit settings
-------------

Create a new file ``doit/settings.py`` with the following content:

.. code-block:: python

    from doit.conf.development import *

Edit and adapt this file to your specific environment.


Setup the database
------------------

Create an empty new PostgreSQL database.

.. code-block:: bash

    $ createdb doit_dev

.. note::

    You might need to apply a postgresql user (``createdb -U youruser``) e.g ``postgres``
    for proper permissions.


.. code-block:: bash

    $ python manage.py syncdb --migrate --noinput


Superuser & example data
------------------------

.. code-block:: bash

    $ # Create a new super user
    $ python manage.py createsuperuser
    $ python import.py

Now you can run the webserver and start using the site.

.. code-block:: bash

   $ python manage.py runserver

This starts a local webserver on `localhost:8000 <http://localhost:8000/>`_. To view the administration
interface visit `/admin/ <http://localhost:8000/admin/>`_

Run Celery and other services
-----------------------------

Other services being used:

* Celery, is being used to run [regular] tasks, e.g for feed imports.
* Compass, is being used to compile our scss files and the foundation framework.

.. note::

   To test oauth services we require using a SSL server for local development.
   It's not required for regular development but the default setup is using SSL.

   Please install ``stunnel``.

   $ brew install stunnel


To start all of them (including the runserver):

.. code-block:: bash

   $ foreman start

.. note::

   Please make sure you have the ``foreman`` gem installed.

**You can find the SSL version on `port 8443 <https://localhost:8443/>`_**


Resources
---------

* `Documentation <http://doit.readthedocs.org>`_
* `Bug Tracker <https://github.com/EnTeQuAk/doit>`_
* `Code <https://github.com/EnTeQuAk/doit>`_
