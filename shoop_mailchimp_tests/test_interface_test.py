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

from shoop_mailchimp.configuration_keys import MC_LIST_ID
from shoop_mailchimp.interface import interface_test
from shoop_mailchimp_tests.mock_responses import (
    raise_on_request, success_response
)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=success_response))
def test_with_missing_list_id(default_shop, valid_test_configuration):
    configuration.cache.clear()
    configuration.set(default_shop, MC_LIST_ID, None)

    assert interface_test(default_shop) is False

    configuration.set(default_shop, MC_LIST_ID, "some-list-id")
    assert interface_test(default_shop)
