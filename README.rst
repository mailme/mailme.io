======
MailMe
======

Installation::

    ~# Create your virtualenv (recommended, use virtualenvwrapper)
    ~# virtualenv env
    ~# # Clone repository
    ~# git clone git@github.com:mailme/mailme.git
    ~# # Activate Environment and install
    ~# source env/bin/activate
    ~# pip install -r requirements.txt
    ~# # run tests
    ~# python manage.py test

Setup the database::

    ~# python manage.py syncdb --migrate --noinput

Create a new superuser and create example data::

    ~# # Create a new super user
    ~# python manage.py createsuperuser
    ~# python import.py


Resources
---------

* `Documentation <yu no url>`_
* `Bug Tracker <http://github.com/mailme/mailme/issues/>`_
* `Code <http://github.com/mailme/mailme>`_
