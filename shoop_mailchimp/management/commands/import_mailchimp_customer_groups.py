# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.utils.translation import activate
from django.utils.timezone import now

from shoop import configuration
from shoop.core.models import ContactGroup, Shop
from shoop_mailchimp.configuration_keys import (
    MC_CONTACT_GROUP_CATEGORY_NAME, MC_CONTACT_GROUP_CATEGORY_KEY
)
from shoop_mailchimp.interface.client import ShoopMailchimpClient
from shoop_mailchimp.models import MailchimpContactGroup


class Command(BaseCommand):
    args = '<api_key username shop_id, list_id>'
    help = "Import existing contact groups from Mailchimp for dev purposes"

    @atomic
    def handle(self, api_key, username, shop_id, list_id, **options):
        activate("en")
        shop = Shop.objects.get(id=shop_id)
        client = ShoopMailchimpClient(username, api_key)
        response = client.category.all(list_id)
        if not response.get("categories"):
            print("No customers found for store %s" % list_id)

        for category_data in response.get("categories"):
            if category_data.get("title") == MC_CONTACT_GROUP_CATEGORY_NAME:
                category_id = str(category_data["id"])
                print("Set MC_CONTACT_GROUP_CATEGORY_KEY to %s" % category_id)
                configuration.set(shop, MC_CONTACT_GROUP_CATEGORY_KEY, category_id)

        if not configuration.get(shop, MC_CONTACT_GROUP_CATEGORY_KEY):
            return
        response = client.interest.all(list_id, configuration.get(shop, MC_CONTACT_GROUP_CATEGORY_KEY))
        if not response.get("interests"):
            return

        for interest_data in response.get("interests"):
            group = ContactGroup.objects.filter(translations__name=interest_data["name"]).first()
            if not group:
                continue
            mc_group, created = MailchimpContactGroup.objects.get_or_create(shop=shop, group=group)
            if created:
                print("Created new Mailchimp group for ContactGroup %s" % group)
                mc_group.sent_to_mailchimp = now()
                mc_group.mailchimp_id = interest_data["id"]
                mc_group.save()
