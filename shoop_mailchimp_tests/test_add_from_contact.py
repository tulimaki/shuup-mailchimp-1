# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
import requests

from django.utils.timezone import now
from mock import Mock, patch

from shoop import configuration
from shoop.testing.factories import create_random_person
from shoop_mailchimp.configuration_keys import MC_ENABLED
from shoop_mailchimp.interface import add_email_to_list, update_or_create_contact
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
def test_add_contact_with_enabled_integration(default_shop, valid_company, valid_test_configuration):
    configuration.set(default_shop, MC_ENABLED, True)

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(valid_company.__class__, valid_company)
    mailchimp_contact = MailchimpContact.objects.get(email=valid_company.email)
    assert mailchimp_contact.sent_to_mailchimp is not None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=success_response))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_add_person_contact_with_name(default_shop, valid_person, valid_test_configuration):
    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(valid_person.__class__, valid_person)
    assert MailchimpContact.objects.count() == 0

    configuration.set(default_shop, MC_ENABLED, True)
    update_or_create_contact(valid_person.__class__, valid_person)
    mailchimp_contact = MailchimpContact.objects.get(email=valid_person.email)
    assert mailchimp_contact.sent_to_mailchimp is not None


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_existing_email_without_contact_update_no_update(default_shop, valid_test_configuration):
    assert MailchimpContact.objects.count() == 0
    configuration.set(default_shop, MC_ENABLED, True)
    valid_email = "noexist@test.com"
    MailchimpContact.objects.create(shop=default_shop, email=valid_email, sent_to_mailchimp=now())
    add_email_to_list(default_shop, valid_email, contact=None)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_edit_contact_matching_existing_email_no_update(default_shop, valid_test_configuration):
    assert MailchimpContact.objects.count() == 0
    configuration.set(default_shop, MC_ENABLED, True)
    valid_email = "noexist@test.com"
    MailchimpContact.objects.create(shop=default_shop, email=valid_email, sent_to_mailchimp=now())
    add_email_to_list(default_shop, valid_email, contact=None)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'put', Mock(side_effect=success_response))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_edit_contact_not_matching_update_related(default_shop, valid_person, valid_test_configuration):
    assert MailchimpContact.objects.count() == 0
    configuration.set(default_shop, MC_ENABLED, True)
    valid_email = "noexist@test.com"
    mailchimp_contact = MailchimpContact.objects.create(
        shop=default_shop,
        email=valid_email,
        contact=valid_person
    )
    new_contact = create_random_person()
    add_email_to_list(default_shop, valid_email, contact=new_contact)
    mailchimp_contact = MailchimpContact.objects.get(email=valid_email)
    assert mailchimp_contact.contact == new_contact
    assert mailchimp_contact.contact != valid_person
