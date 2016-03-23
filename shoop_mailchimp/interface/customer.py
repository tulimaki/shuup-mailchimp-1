# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from mailchimp3.baseapi import BaseApi


class Customer(BaseApi):
    """
    Extension into mailchimp3 package to handle Mailchimp API v3.0 eCommerce Customers

    http://developer.mailchimp.com/documentation/mailchimp/reference/ecommerce/stores/customers/
    """
    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.endpoint = 'ecommerce'

    def all(self, store_id):
        """
        Fetch customers from eCommerce Store

        :param store_id: Mailchimp eCommerce store id to link
        customer
        :type store_id: string
        :return: list of customers in store
        :rtype: JSON
        """
        return self._mc_client._get(url=self._build_path("stores", store_id, 'customers'))

    def create(self, store_id, data):
        """
        Creates a new customer for store

        :param store_id: Mailchimp eCommerce store id to link
        customer
        :type store_id: string
        :param data: required data keys for customer is id,
        email_address and opt_in_status
        :type data: dict
        :return: Mailchimp response
        :rtype: JSON
        """
        return self._mc_client._post(url=self._build_path("stores", store_id, 'customers'), data=data)

    def update(self, store_id, customer_id, data):
        """
        Updates existing customers's data in store

        :param store_id: Mailchimp eCommerce store id to which
        the customer is linked
        :type store_id: string
        :param customer_id: Mailchimp eCommerce customer id
        to update
        :type customer_id: string
        :param data: Data to update for customer. Optional
        keys for data can be found Mailchimp documentation
        :type data: dict
        :return: Mailchimp response
        :rtype: JSON
        """
        return self._mc_client._patch(url=self._build_path("stores", store_id, 'customers', customer_id), data=data)

    def get(self, store_id, customer_id):
        """
        :param store_id: Mailchimp eCommerce store id to which
        the customer is linked
        :type store_id: string
        :param customer_id: Mailchimp eCommerce customer id
        to update
        :type customer_id: string
        :return: information about a specific customer in store
        :rtype: JSON
        """
        return self._mc_client._get(url=self._build_path("stores", store_id, 'customers', customer_id))
