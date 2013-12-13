======
MailMe
======

Installation
------------

.. code-block:: bash

    $ Create your virtualenv (recommended, use virtualenvwrapper)
    $ virtualenv env

    $ # Clone repository
    $ git clone git@bitbucket.org:mailme/mailme.git

    $ # Activate Environment and install
    $ source env/bin/activate
    $ make devinstall

    $ # run tests
    $ python setup.py test


Edit settings
-------------

Ignore development settings.

.. code-block:: bash

    $ git update-index --assume-unchanged mailme/settings/development.py

This ignores all future changes to your local development settings.

Edit ``mailme/settings/development.py`` and adapt to your environment.


Setup the database
------------------

.. code-block:: bash

    $ python manage.py syncdb --migrate --noinput


Superuser & example data
------------------------

.. code-block:: bash

    $ # Create a new super user
    $ python manage.py createsuperuser
    $ python import.py

Now you can run the webserver and start using the site.

.. code-block::

   $ python manage.py runserver

This starts a local webserver on `localhost:8000 <http://localhost:8000/`_. To view the administration
interface visit `/admin/ <http://localhost:8000/admin/`_

Resources
---------

* `Documentation <yu no url>`_
* `Bug Tracker <https://trello.com/b/yQfpDGPx/task-board>`_
* `Code <https://bitbucket.org/fruitywinter/mailme.io>`_
