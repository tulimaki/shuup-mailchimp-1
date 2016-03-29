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
from shoop_mailchimp.configuration_keys import MC_ENABLED
from shoop_mailchimp.interface import update_or_create_contact
from shoop_mailchimp.models import MailchimpContact
from shoop_mailchimp_tests.mock_responses import (
    raise_on_request, success_response
)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=success_response))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_add_contact_with_disabled_integration(default_shop, valid_company, valid_test_configuration):
    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(valid_company.__class__, valid_company)
    assert MailchimpContact.objects.count() == 0

    configuration.set(default_shop, MC_ENABLED, True)
    update_or_create_contact(valid_company.__class__, valid_company)
    mailchimp_contact = MailchimpContact.objects.get(email=valid_company.email)
    assert mailchimp_contact.sent_to_mailchimp is not None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=success_response))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_add_contact_without_marketing_permission(default_shop, valid_company, valid_test_configuration):
    configuration.set(default_shop, MC_ENABLED, True)
    valid_company.marketing_permission = False
    valid_company.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(valid_company.__class__, valid_company)
    assert MailchimpContact.objects.count() == 0


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=success_response))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_add_contact_with_disabled_integration(default_shop, valid_company, valid_test_configuration):
    configuration.set(default_shop, MC_ENABLED, True)

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(valid_company.__class__, valid_company)
    mailchimp_contact = MailchimpContact.objects.get(email=valid_company.email)
    assert mailchimp_contact.sent_to_mailchimp is not None
