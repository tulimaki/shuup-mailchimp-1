# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from shoop import configuration
from shoop_mailchimp.configuration_keys import (MC_API, MC_LIST_ID,
                                                MC_STORE_ID, MC_USERNAME)
from shoop_mailchimp.interface.client import ShoopMailchimpClient


class MailchimpResponseError(Exception):
    pass


class ShoopMailchimp(object):
    def __init__(self, shop):
        self.shop = shop
        self.list_id = configuration.get(self.shop, MC_LIST_ID)
        self.store_id = configuration.get(self.shop, MC_STORE_ID)
        self.client = self._get_client()

    def _get_configurations_for_client(self):
        return {
            "api_key": configuration.get(self.shop, MC_API),
            "list_id": self.list_id,
            "username": configuration.get(self.shop, MC_USERNAME)
        }

    def _get_client(self):
        configurations = self._get_configurations_for_client()
        if not all(configurations.itervalues()):
            return
        return ShoopMailchimpClient(configurations["username"], configurations["api_key"])

    def _get_list(self):
        if not (self.list_id and self.client):
            return
        return self.client.list.get(self.list_id)

    def raise_if_no_id_in_data(self, response_data, default_error_msg):
        if not (response_data and response_data.get("id")):
            raise MailchimpResponseError(response_data.get("detail") or default_error_msg)

    def is_configured(self):
        """
        :return: boolean based on whether Mailchimp client is
        available
        :rtype: bool
        """
        return bool(self.client)

    def get_list_id(self):
        """
        :return: configured Mailchimp list id
        :rtype: str
        """
        return self.list_id

    def can_create_store_for_list(self):
        """
        Can create new Mailchimp eCommerce store

        Store can't be created without Mailchimp list id. Also since
        Mailchimp doesn't sync existing list members with store customers
        linked list needs to empty.

        :return: boolean based can the Mailchimp eCommerce store
        be created
        :rtype: bool
        """
        list = self._get_list()
        if not list:
            return False

        list_stats = list.get("stats")
        if not (list_stats and list_stats.get("member_count") == 0):
            return False
        return True

    def save_store_id(self, store_id):
        """
        Saves store id into Shoop configuration

        :param store_id: saved store id
        :return: str
        """
        configuration.set(self.shop, MC_STORE_ID, store_id)  # Save new store id
        return store_id

    def create_store(self, data):
        """
        Creates new Mailchimp eCommerce store

        :param data: store data
        :type data: dict
        :return: store id for created store
        :rtype: str
        """
        store_data = self.client.store.create(data=data)
        self.raise_if_no_id_in_data(store_data, "Error happened while creating store.")
        return self.save_store_id(str(store_data.get("id")))

    def get_store_id(self):
        """
        Get integration store id

        :return: Mailchimp eCommerce store id for integration
        :rtype: str
        """
        return self.store_id
