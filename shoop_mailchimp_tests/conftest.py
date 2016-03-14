# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from django.db.models.signals import post_save

from shoop import configuration
from shoop.core.order_creator.signals import order_creator_finished
from shoop.core.models import CompanyContact, Order, PersonContact
from shoop.testing.factories import get_default_shop
from shoop_mailchimp.configuration_keys import (
    MC_API, MC_CONTACT_GROUP_CATEGORY_KEY,
    MC_CONTACT_SIGNAL_DISPATCH_UID, MC_ORDER_SIGNAL_DISPATCH_UID,
    MC_LIST_ID, MC_STORE_ID, MC_USERNAME
)


@pytest.fixture()
@pytest.mark.django_db()
def default_shop():
    return get_default_shop()


@pytest.fixture()
@pytest.mark.django_db()
def valid_test_configuration_without_store():
    configuration.cache.clear()
    shop = get_default_shop()
    configuration.set(shop, MC_API, "some-api-key")
    configuration.set(shop, MC_USERNAME, "some-username")
    configuration.set(shop, MC_LIST_ID, "some-list-id")


@pytest.fixture()
@pytest.mark.django_db()
def valid_test_configuration_with_store():
    configuration.cache.clear()
    shop = get_default_shop()
    configuration.set(shop, MC_API, "some-api-key")
    configuration.set(shop, MC_USERNAME, "some-username")
    configuration.set(shop, MC_LIST_ID, "some-list-id")
    configuration.set(shop, MC_STORE_ID, shop.pk)


def pytest_configure():
    """
    For testing sake let's disconnect integration signals since
    it is quite possible that signal is not yet handled when
    checking if some update functions actually work as supposed
    """
    post_save.disconnect(sender=CompanyContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
    post_save.disconnect(sender=PersonContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
    order_creator_finished.disconnect(sender=Order, dispatch_uid=MC_ORDER_SIGNAL_DISPATCH_UID)
