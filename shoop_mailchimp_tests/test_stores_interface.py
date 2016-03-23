# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
import requests
from mock import Mock, patch

from shoop import configuration
from shoop_mailchimp.configuration_keys import (
    MC_API, MC_LIST_ID, MC_STORE_ID, MC_USERNAME
)
from shoop_mailchimp.admin.views import (
    initialize_store, configurations_test
)
from shoop_mailchimp.interface import (
    get_or_create_store_id_for_shop, get_store_id
)
from shoop_mailchimp_tests.mock_responses import (
    create_store_success, get_empty_list, get_non_empty_list,
    PostIsNotAllowed, raise_on_request
)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_store_with_store_id(default_shop):
    configuration.cache.clear()
    store_id = "some-key"
    configuration.set(default_shop, MC_STORE_ID, store_id)
    assert get_store_id(default_shop) == store_id
    assert get_or_create_store_id_for_shop(default_shop) == store_id


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=get_empty_list))
def test_creating_store_with_invalid_configurations(default_shop):
    configuration.cache.clear()

    assert get_store_id(default_shop) is None
    assert get_or_create_store_id_for_shop(default_shop) is None

    configuration.set(default_shop, MC_API, "some-api-key")
    assert get_store_id(default_shop) is None
    assert get_or_create_store_id_for_shop(default_shop) is None

    configuration.set(default_shop, MC_USERNAME, "some-username")
    assert get_store_id(default_shop) is None
    assert get_or_create_store_id_for_shop(default_shop) is None

    configuration.set(default_shop, MC_LIST_ID, "some-list-id")
    # Now all configurations keys is set
    assert get_store_id(default_shop) is None
    with pytest.raises(PostIsNotAllowed):
        get_or_create_store_id_for_shop(default_shop)

    configuration.set(default_shop, MC_USERNAME, None)
    # Should not send any requests anymore
    assert get_store_id(default_shop) is None
    assert get_or_create_store_id_for_shop(default_shop) is None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=get_non_empty_list))
def test_creating_store_with_non_empty_list(default_shop, valid_test_configuration_without_store):
    assert get_store_id(default_shop) is None
    assert get_or_create_store_id_for_shop(default_shop) is None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=get_empty_list))
def test_creating_store_with_empty_list(default_shop, valid_test_configuration_without_store):
    with pytest.raises(PostIsNotAllowed):
        assert get_store_id(default_shop) is None
        assert get_or_create_store_id_for_shop(default_shop) is None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=create_store_success))
@patch.object(requests, 'get', Mock(side_effect=get_empty_list))
def test_creating_store_success(rf, default_shop, valid_test_configuration_without_store):
    assert get_store_id(default_shop) is None
    request = rf.get("/")
    response = initialize_store(request, default_shop.pk)
    assert response.status_code == 200

    response = configurations_test(request, default_shop.pk)
    assert response.status_code == 200
