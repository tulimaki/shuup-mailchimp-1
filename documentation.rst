Shoop Mailchimp Documentation
=============================

Introduction
------------

Shoop Mailchimp integration uses Mailchimp v3 API to send
Shoop Contacts and ContactGroups into Mailchimp.

More information about the API can be found at `here <http://developer.mailchimp.com/documentation/mailchimp/reference/overview/>`_.

Integration uses a 3rd party Python client to communicate with Mailchimp.
This client can be found `here <https://github.com/charlesthk/python-mailchimp>`_.

Configurations
--------------

Making the integration work needs the following configurations which are
set through the admin interface under shop item.

* Mailchimp API key
* Mailchimp list id
* Mailchimp eCommerce store id

All these configurations are per shop values.

Initialization
--------------

Initialization creates new eCommerce store for the given Mailchimp list.
Initialization can be activated from Shoop admin.

Contacts in database while starting integration are not synced to
Mailchimp. As a customer you can manually add these to your store list
after the integration is initialized in Mailchimp admin panel.

Logging
-------

All Mailchimp commands and processes are logged to MailchimpLogEntry
which is stored in the database.

Contacts
--------

For sending contacts into Mailchimp the integration needs to be
enabled.

Contacts are sent to Mailchimp as eCommerce customers.
These Mailchimp customers are automatically synced to the list linked to
Mailchimp eCommerce store as members.

If sending contact to Mailchimp fails it is marked to database and
can be sent again from shop admin.

Updating Contacts
-----------------

End customers can unsubscribe through Mailchimp marketing letters.

Mailchimp interests are update while new orders are created.

ContactGroups
-------------

ContactGroups are sent to Mailchimp as a list of group interests.
Mailchimp group "Contact Group" is created for these interests.
This enables the option to create different segments in Mailchimp admin.

ContactGroups is sent while updating contact interests.

Updating ContactGroups
----------------------

ContactGroup is sent to Mailchimp when Contact's groups are updated.
