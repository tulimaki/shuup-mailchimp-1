# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shoop.core.models import Shop

from shoop_mailchimp.interface.base import ShoopMailchimp


def update_or_create_contact(sender, instance, **kwargs):
    """
    Signal handler for Shoop contacts

    Add's contact email to every configured shop list
    """
    if not instance.marketing_permission:
        return

    for shop in Shop.objects.all():
        add_email_to_list(shop, instance.email, contact=instance)


def update_or_create_contact_from_order(sender, order, *args, **kwargs):
    """
    Signal handler for Shoop orders
    """
    if order.email and order.marketing_permission:
        add_email_to_list(order.shop, order.email, contact=order.customer)
        return


def add_email_to_list(shop, email, contact=None):
    """
    Add email and optional contact to Mailchimp list

    :param email: email to add in the list
    :param contact: optional associated Shoop contact
    :return:
    """
    client = ShoopMailchimp(shop)
    client.add_email_to_list(email, contact=contact)
