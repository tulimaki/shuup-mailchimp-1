# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shoop.core.models import CompanyContact, PersonContact, Shop
from shoop_mailchimp.interface.base import ShoopMailchimp
from shoop_mailchimp.interface.contacts import ShoopMailchimpContact
from shoop_mailchimp.models import MailchimpContact


def _update_or_create_contact(shop, contact):
    client = ShoopMailchimpContact(shop, contact)
    return client.update_or_create_contact()


def _get_contacts_ordered_from_shop(cls, shop):
    failed_contact_pks = MailchimpContact.objects.filter(
        latest_push_failed=True
    ).values_list("contact_id", flat=True)
    return cls.objects.filter(
        id__in=failed_contact_pks,
        customer_orders__shop=shop,marketing_permission=True
    ).distinct()


def _update_or_create_contacts(shop, cls):
    for contact in _get_contacts_ordered_from_shop(cls, shop):
        _update_or_create_contact(shop, contact)


def update_or_create_contacts(shop):
    """
    Update or create Shoop contacts into Mailchimp

    Update all failed ``MailchimpContact`` resources
    """
    client = ShoopMailchimp(shop)
    if not (client.is_configured() and client.get_store_id()):
        return

    _update_or_create_contacts(shop, CompanyContact)
    _update_or_create_contacts(shop, PersonContact)


def update_or_create_contact(sender, instance, **kwargs):
    """
    Signal handler for Shoop contacts

    Updates or creates contact into Mailchimp if possible
    """
    for shop in Shop.objects.all():
        _update_or_create_contact(shop, instance)


def update_or_create_contact_from_order(sender, instance, **kwargs):
    """
    Signal handler for Shoop orders

    Updates or creates order customer into Mailchimp if possible
    """
    _update_or_create_contact(instance.shop, instance.customer)
