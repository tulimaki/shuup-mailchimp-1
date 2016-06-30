Shuup Mailchimp Integration
===========================

This package implements Mailchimp integration
for the `Shuup <https://shuup.io/>`_ platform.

Copyright
---------

Copyright (C) 2012-2016 by Shoop Commerce Ltd. <contact@shuup.io>

Shuup is International Registered Trademark & Property of Shoop Commerce Ltd.,
Business ID: FI24815722, Business Address: Aurakatu 12 B, 20100 Turku,
Finland.

Running tests
-------------

You can run tests with `py.test <http://pytest.org/>`_.

Requirements for running tests:

* Your virtualenv needs to have Shuup installed.

* Project root must be in the Python path.  This can be done with:

  .. code:: sh

     pip install -e .

* The packages from ``testing_requirements.txt`` must be installed.

  .. code:: sh

     pip install -r testing_requirements.txt

To run tests, use command:

.. code:: sh

   py.test -v shuup_mailchimp_tests


Documentation
-------------

* See the documentation.rst
