# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import requests

from django.conf import settings

from shoop import configuration
from shoop_mailchimp.configuration_keys import (
    MC_CONTACT_GROUP_CATEGORY_KEY, MC_CONTACT_GROUP_CATEGORY_NAME
)
from shoop_mailchimp.interface.base import MailchimpResponseError, ShoopMailchimp
from shoop_mailchimp.models import MailchimpContactGroup


class ShoopMailchimpContactGroup(ShoopMailchimp):
    def __init__(self, shop, group):
        super(ShoopMailchimpContactGroup, self).__init__(shop)
        self.group = group
        self.mailchimp_group = None

    def _get_mailchimp_group(self):
        self.mailchimp_group = MailchimpContactGroup.objects.filter(shop=self.shop, group=self.group).first()
        return self.mailchimp_group

    def _get_or_create_contact_group_category_id(self):
        category_id = configuration.get(self.shop, MC_CONTACT_GROUP_CATEGORY_KEY)
        if category_id:
            return category_id

        # Let's create one
        data = {"title": MC_CONTACT_GROUP_CATEGORY_NAME, "type": "hidden"}
        category_data = self.client.category.create(self.get_list_id(), data)
        self.raise_if_no_id_in_data(
            category_data, "Creating Mailchimp category %s failed" % MC_CONTACT_GROUP_CATEGORY_NAME)
        category_id = str(category_data.get("id"))
        configuration.set(self.shop, MC_CONTACT_GROUP_CATEGORY_KEY, category_id)
        return category_id

    def get_or_create_group_interest(self):
        """
        Get or create Mailchimp group interest

        Get or create Mailchimp group interest based on current shop
        and contact group. Create Mailchimp group for contact groups
        if one does not exist.

        New ``MailchimpContactGroup`` is created while creating new
        Mailchimp group interest.

        :return: mailchimp contact group object
        :rtype: shoop_mailchimp.models.MailchimpContactGroup
        """
        if self._get_mailchimp_group():
            return self.mailchimp_group

        mailchimp_category_id = self._get_or_create_contact_group_category_id()
        if not mailchimp_category_id:
            return
        data = {
            "name": self.group.safe_translation_getter("name", language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE)
        }
        interest_data = self.client.interest.create(self.get_list_id(), str(mailchimp_category_id), data)
        self.raise_if_no_id_in_data(interest_data, "Creating Mailchimp interest %s failed" % data.get("name"))

        interest_id = str(interest_data.get("id"))
        self.mailchimp_group = MailchimpContactGroup.objects.create(
            shop=self.shop,
            group=self.group,
            mailchimp_id=interest_id
        )
        return self.mailchimp_group
