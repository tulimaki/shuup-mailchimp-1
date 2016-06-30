# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import hashlib

import requests
import six
from django.utils.timezone import now
from shuup import configuration
from shuup.core.models import CompanyContact, PersonContact
from shuup.utils.analog import LogEntryKind

from shuup_mailchimp.configuration_keys import (
    MC_API, MC_ENABLED, MC_LIST_ID, MC_USERNAME
)
from shuup_mailchimp.interface.client import ShuupMailchimpClient
from shuup_mailchimp.models import MailchimpContact


class ShuupMailchimp(object):
    def __init__(self, shop):
        self.shop = shop
        self.list_id = configuration.get(self.shop, MC_LIST_ID)
        self.client = self._get_client()

    def _get_configurations_for_client(self):
        return {
            "api_key": configuration.get(self.shop, MC_API),
            "list_id": self.list_id,
            "username": configuration.get(self.shop, MC_USERNAME)
        }

    def _get_client(self):
        configurations = self._get_configurations_for_client()
        if not all(six.itervalues(configurations)):
            return
        return ShuupMailchimpClient(configurations["username"], configurations["api_key"])

    def _get_subscriber_hash(self, email):
        """
        Get hash for subscriber email for updating list member

        From Mailchimp API documentation: subscriber_hash is MD5
        hash of the lowercase version of the list member's email
        address
        """
        return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    def get_list(self):
        if not (self.list_id and self.client):
            return
        return self.client.list.get(self.list_id)

    def _is_enabled(self):
        return bool(self.list_id and self.client and configuration.get(self.shop, MC_ENABLED))

    def add_email_to_list(self, email, contact=None):
        """
        Add given email to configured Mailchimp list

        :param email: email to add list
        :param contact: optional associated Shuup contact
        """
        if not self._is_enabled():
            return

        mailchimp_contact, created = MailchimpContact.objects.get_or_create(
            shop=self.shop, email=email
        )
        if not contact and mailchimp_contact.sent_to_mailchimp:
            return

        if contact and mailchimp_contact.contact == contact:
            return

        if contact != mailchimp_contact.contact:
            mailchimp_contact.contact = contact
            mailchimp_contact.save()

        try:

            merge_fields = {}
            if isinstance(contact, PersonContact):
                merge_fields = {"FNAME": contact.first_name, "LNAME": contact.last_name}
            elif isinstance(contact, CompanyContact):
                # Mailchimp has no default merge tag for company name, so using first name tag
                merge_fields = {"FNAME": contact.full_name}

            resp = self.client.shuup_member.update_or_create(
                self.list_id,
                self._get_subscriber_hash(email),
                {"status": "subscribed", "email_address": email, "merge_fields": merge_fields}
            )
            if not (resp and resp.get("id")):
                mailchimp_contact.add_log_entry(resp.get("title"), "client_error", LogEntryKind.ERROR)
                return
            mailchimp_contact.sent_to_mailchimp = now()
            mailchimp_contact.save()
            return mailchimp_contact
        except requests.HTTPError:
            mailchimp_contact.add_log_entry(
                "Unexpected error: Couldn't send email to list.", "client_error", LogEntryKind.ERROR)
