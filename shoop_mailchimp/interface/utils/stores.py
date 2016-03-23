# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf import settings

from shoop_mailchimp.interface.base import ShoopMailchimp


def get_or_create_store_id_for_shop(shop):
    """
    Get or create Mailchimp store id for Shoop shop

    :param shop: shop instance to get or crete store id for
    :type shop: shoop.core.models.Shop
    :return: Mailchimp store id for given shop. None if
    store id is not configured and new on can't be created
    :rtype: str|None
    """
    client = ShoopMailchimp(shop)
    store_id = client.get_store_id()
    if store_id:
        return store_id

    if not client.can_create_store_for_list():
        return

    data = {
        "id": str(shop.pk),
        "name": shop.safe_translation_getter("name", language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE),
        "list_id": client.get_list_id(),
        "currency_code": shop.currency
    }
    return client.create_store(data)


def get_store_id(shop):
    """
    Get Mailchimp store id for Shoop shop

    :param shop: shop instance to get store id for
    :type shop: shoop.core.models.Shop
    :return: Mailchimp store id for given shop
    :rtype: str
    """
    client = ShoopMailchimp(shop)
    return client.get_store_id()
