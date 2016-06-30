# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup.core.models import Shop

from shuup_mailchimp.interface.base import ShuupMailchimp


def update_or_create_contact(sender, instance, **kwargs):
    """
    Signal handler for Shuup contacts

    Add's contact email to every configured shop list
    """
    if not instance.marketing_permission:
        return

    for shop in Shop.objects.all():
        add_email_to_list(shop, instance.email, contact=instance)


def update_or_create_contact_from_order(sender, order, *args, **kwargs):
    """
    Signal handler for Shuup orders
    """
    if order.email and order.marketing_permission:
        add_email_to_list(order.shop, order.email, contact=order.customer)
        return


def add_email_to_list(shop, email, contact=None):
    """
    Add email and optional contact to Mailchimp list

    :param email: email to add in the list
    :param contact: optional associated Shuup contact
    :return:
    """
    client = ShuupMailchimp(shop)
    client.add_email_to_list(email, contact=contact)
