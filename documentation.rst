Shuup Mailchimp Documentation
=============================

Introduction
------------

Shuup Mailchimp integration uses Mailchimp v3 API to send emails
into Mailchimp.

More information about the API can be found at `here <http://developer.mailchimp.com/documentation/mailchimp/reference/overview/>`_.

Integration uses a 3rd party Python client to communicate with Mailchimp.
This client can be found `here <https://github.com/charlesthk/python-mailchimp>`_.

Configurations
--------------

Integration configurations is set inside Shop admin.

Making the integration work needs the following configurations which are
set through the admin interface under shop item.

* Mailchimp API key
* Mailchimp list id

All these configurations are per shop values.

Logging
-------

All errors while adding emails to list is logged.

Contacts
--------

For sending contacts into Mailchimp the integration needs to be
enabled.

Only valid emails is sent to Mailchimp

Contact save: if contact marketing permission is on and email is not
already sent to Mailchimp. Contact email and name information is sent
to all configured Shop lists.

Order creation: if order or contact marketing permission is on and
email is not already sent to Mailchimp. Contact email is sent to
only list based on orders Shop.

Plugin: emails can be send to Mailchimp through xtheme plugin

Updating Contacts
-----------------

End customers can unsubscribe through Mailchimp marketing letters.

eCommerce
---------

Some eCommerce functionality can be found on commit d6b6359


