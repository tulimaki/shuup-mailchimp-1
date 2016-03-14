# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.utils.timezone import now

from shoop.core.models import CompanyContact, PersonContact, Shop
from shoop_mailchimp.interface.client import ShoopMailchimpClient
from shoop_mailchimp.models import MailchimpContact


def handle_customer(cls, shop, customer_data):
    contact_for_email = cls.objects.filter(email=customer_data["email_address"]).first()
    if not contact_for_email:
        return

    mc_contact, created = MailchimpContact.objects.get_or_create(shop=shop, contact=contact_for_email)
    if created:
        print("Created new MailchimpContact for Contact %s" % contact_for_email)
        mc_contact.mailchimp_id = customer_data["id"]
        mc_contact.sent_to_mailchimp = now()
        mc_contact.save()



class Command(BaseCommand):
    args = '<api_key username shop_id, store_id>'
    help = "Import existing store customers from Mailchimp for dev purposes"

    @atomic
    def handle(self, api_key, username, shop_id, store_id, **options):
        shop = Shop.objects.get(id=shop_id)
        client = ShoopMailchimpClient(username, api_key)
        response = client.customer.all(store_id)
        if not response.get("customers"):
            print("No customers found for store %s" % store_id)

        for customer_data in response.get("customers"):
            handle_customer(CompanyContact, shop, customer_data)
            handle_customer(PersonContact, shop, customer_data)
