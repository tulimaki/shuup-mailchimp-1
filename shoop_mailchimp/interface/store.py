# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from mailchimp3.baseapi import BaseApi


class Store(BaseApi):
    """
    Extension into mailchimp3 package to handle Mailchimp API v3.0 eCommerce Stores

    http://developer.mailchimp.com/documentation/mailchimp/reference/ecommerce/stores/
    """
    def __init__(self, *args, **kwargs):
        super(Store, self).__init__(*args, **kwargs)
        self.endpoint = 'ecommerce'

    def all(self):
        """
        :return: list of stores for the account.
        :rtype: JSON
        """
        return self._mc_client._get(url=self._build_path('stores'))

    def create(self, data):
        """
        Creates a new store for the account

        :param data: required keys for dict is id, name, list_id and
        currency_code
        :type data: dict
        :return: Mailchimp response
        :rtype: JSON
        """
        return self._mc_client._post(url=self._build_path('stores'), data=data)
