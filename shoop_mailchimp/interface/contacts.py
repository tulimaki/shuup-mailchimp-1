# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import hashlib
import requests

from django.core.validators import ValidationError, validate_email
from django.utils.timezone import now
from django.utils.text import force_text

from shoop import configuration
from shoop.core.models import CompanyContact, Order
from shoop.utils.analog import LogEntryKind
from shoop_mailchimp.configuration_keys import MC_ENABLED
from shoop_mailchimp.interface.base import (MailchimpResponseError,
                                            ShoopMailchimp)
from shoop_mailchimp.interface.contact_groups import ShoopMailchimpContactGroup
from shoop_mailchimp.models import MailchimpContact


class ShoopMailchimpContact(ShoopMailchimp):
    def __init__(self, shop, contact):
        super(ShoopMailchimpContact, self).__init__(shop)
        self.contact = contact
        self.mailchimp_contact = self._get_or_create_mailchimp_contact()
        self.errors = []

    def _add_error(self, msg, identifier, kind):
        self.errors.append((msg, identifier, kind))

    def _finalize(self):
        if self.errors:
            for message, identifier, kind in self.errors:
                self.mailchimp_contact.add_log_entry(message, identifier, kind)
                self.mailchimp_contact.latest_push_failed = True
        else:
            # Created or update new contact
            self.mailchimp_contact.latest_push_failed = False
            if not self.mailchimp_contact.sent_to_mailchimp:
                self.mailchimp_contact.sent_to_mailchimp = now()
                self.mailchimp_contact.add_log_entry(
                    "Contact added to Mailchimp", "sent_successful", kind=LogEntryKind.NOTE)
            self.mailchimp_contact.save()
        self.mailchimp_contact.save()
        return self.mailchimp_contact

    def _get_or_create_mailchimp_contact(self):
        self.mailchimp_contact, created = MailchimpContact.objects.get_or_create(
            shop=self.shop, contact=self.contact)
        if created:
            self.mailchimp_contact.mailchimp_id = self.contact.pk
            self.mailchimp_contact.save()
        return self.mailchimp_contact

    def _has_valid_email(self):
        if not self.contact.email:
            return False
        try:
            validate_email(self.contact.email)
        except ValidationError:
            return False
        return True

    def _can_send_contact(self):
        if not self._has_valid_email():
            self._add_error("Invalid email", "invalid_email", LogEntryKind.ERROR)
            return False
        if not Order.objects.filter(shop=self.shop, customer=self.contact).exists():
            self._add_error("Contact has no orders from this shop", "no_orders_from_shop", LogEntryKind.ERROR)
            return False
        return True

    def _get_contact_hash(self):
        """
        Get hash for contact for updating list member

        From Mailchimp API documentation: subscriber_hash is MD5
        hash of the lowercase version of the list member's email
        address
        """
        return hashlib.md5(self.contact.email.lower()).hexdigest() if self.contact.email else None

    def _update_list_member_interests(self):
        interests_data = {}
        for contact_group in self.contact.groups.all():
            try:
                contact_group_client = ShoopMailchimpContactGroup(self.shop, contact_group)
                contact_group_mc_id = contact_group_client.get_or_create_group_interest()
            except (MailchimpResponseError, requests.HTTPError) as e:
                self._add_error(force_text(e), "contact_group_error", LogEntryKind.ERROR)
                return
            if contact_group_mc_id:
                interests_data[contact_group_mc_id.mailchimp_id] = True

        if not interests_data:
            return

        data = {
            "interests": interests_data
        }

        try:
            interests_data = self.client.member.update(self.list_id, self._get_contact_hash(), data)
            self.raise_if_no_id_in_data(
                interests_data, "Error happened while updating customer %s interests" % self.contact.name)
        except (MailchimpResponseError, requests.HTTPError) as e:
            self._add_error(force_text(e), "response_error", LogEntryKind.ERROR)

    def _create_contact(self):
        contact_data = {
            "id": self.mailchimp_contact.mailchimp_id,
            "email_address": self.contact.email,
            "opt_in_status": bool(self.contact.marketing_permission),
        }

        if isinstance(self.contact, CompanyContact):
            contact_data.update({
                "company": self.contact.name or ""
            })

        # TODO: Implement first and last name for PersonContact after SHOOP-832
        try:
            mailchimp_customer_data = self.client.customer.create(str(self.store_id), contact_data)
            self.raise_if_no_id_in_data(
                mailchimp_customer_data, "Error happened while creating customer.")
        except (MailchimpResponseError, requests.HTTPError) as e:
            self._add_error(force_text(e), "response_error", LogEntryKind.ERROR)

    def update_or_create_contact(self):
        """
        Update or create Shoop contact into Mailchimp

        To be able to update or create contacts Mailchimp integration
        needs to be enabled and contact needs to have at least one
        order in current shop. Also integration needs to be fully
        configured.

        Only contacts with valid email is handled.

        Due the update or create ``MailchimpContact`` is created or updated.

        :return: mailchimp contact
        :rtype: shoop_mailchimp.models.MailchimpContact
        """
        if not self.mailchimp_contact:
            return

        if not (configuration.get(self.shop, MC_ENABLED) and self.client):
            # Do not log if integration is not enabled or configured
            return

        if not self.contact.marketing_permission:
            # Do not log if contact does not have marketing permission on
            return

        self._can_send_contact()

        if not self.errors and not self.mailchimp_contact.sent_to_mailchimp:
            # New Mailchimp contact added so let's send it to Mailchimp also
            self._create_contact()

        if not self.errors:
            self._update_list_member_interests()  # Always update contact's list member interests

        return self._finalize()
