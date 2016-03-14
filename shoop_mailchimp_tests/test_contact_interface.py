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
from shoop.testing.factories import (
    create_random_company, create_random_person, create_empty_order,
    get_default_customer_group
)
from shoop_mailchimp.configuration_keys import MC_ENABLED
from shoop_mailchimp.interface import (
    update_or_create_contact, update_or_create_contact_from_order,
    update_or_create_contacts,
)
from shoop_mailchimp.models import MailchimpContact, MailchimpContactGroup
from shoop_mailchimp_tests.mock_responses import (
    mailchimp_response_failure_with_200, create_or_update_resource_success, raise_on_request
)


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_with_disabled_integration(default_shop, valid_test_configuration_with_store):
    company = create_random_company()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    assert MailchimpContact.objects.count() == 1
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    # Disabled integration should fail silently
    assert mailchimp_contact.log_entries.count() == 0


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_without_marketing_permission(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.marketing_permission = False
    company.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    # Contacts without marketing permission is just skipped
    assert mailchimp_contact.log_entries.count() == 0


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_without_email(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = ""
    company.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    assert mailchimp_contact.log_entries.count() == 1
    assert mailchimp_contact.log_entries.filter(identifier="invalid_email").count() == 1




@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=raise_on_request))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_with_invalid_email(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = "not-valid@"
    company.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    assert mailchimp_contact.log_entries.count() == 1
    assert mailchimp_contact.log_entries.filter(identifier="invalid_email").count() == 1



@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'patch', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_without_orders(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = "valid@example.com"
    company.marketing_permission = True
    company.save()

    # Make sure we have a fresh Mailchimp database for contacts
    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    assert mailchimp_contact.log_entries.count() == 1
    assert mailchimp_contact.log_entries.filter(identifier="no_orders_from_shop").count() == 1
    assert mailchimp_contact.latest_push_failed

    order = create_empty_order(shop=default_shop)
    order.customer = company
    order.save()

    update_or_create_contacts(default_shop)
    mailchimp_contact = MailchimpContact.objects.get(contact=company)
    assert mailchimp_contact.log_entries.count() == 2
    assert mailchimp_contact.log_entries.filter(identifier="sent_successful").count() == 1
    assert not mailchimp_contact.latest_push_failed


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'patch', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = "valid@example.com"
    company.marketing_permission = True
    company.save()

    order = create_empty_order(shop=default_shop)
    order.customer = company
    order.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    assert MailchimpContact.objects.count() == 1
    mailchimp_contact = MailchimpContact.objects.get(shop=default_shop, contact=company)
    assert mailchimp_contact.log_entries.filter(identifier="sent_successful").exists()
    assert not mailchimp_contact.latest_push_failed
    assert mailchimp_contact.sent_to_mailchimp

    assert MailchimpContactGroup.objects.count() == company.groups.count()

    default_group = get_default_customer_group()
    assert default_group not in company.groups.all()
    company.groups.add(default_group)

    update_or_create_contact_from_order(order.__class__, order)
    assert [mc_group for mc_group in MailchimpContactGroup.objects.all() if mc_group.group == default_group]
    assert MailchimpContactGroup.objects.count() == company.groups.count()

    person = create_random_person()
    person.email = "good@example.com"
    person.marketing_permission = True
    person.save()

    second_order = create_empty_order(shop=default_shop)
    second_order.customer = person
    second_order.save()

    update_or_create_contact(person.__class__, person)
    mailchimp_contact = MailchimpContact.objects.get(shop=default_shop, contact=person)
    assert mailchimp_contact.log_entries.filter(identifier="sent_successful").exists()
    assert not mailchimp_contact.latest_push_failed
    assert mailchimp_contact.sent_to_mailchimp


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=mailchimp_response_failure_with_200))
@patch.object(requests, 'patch', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_creating_contact_mailchimp_error(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = "valid@example.com"
    company.marketing_permission = True
    company.save()

    order = create_empty_order(shop=default_shop)
    order.customer = company
    order.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(shop=default_shop, contact=company)
    assert mailchimp_contact.log_entries.filter(identifier="response_error").exists()
    assert mailchimp_contact.latest_push_failed


@pytest.mark.django_db
@patch.object(requests, 'post', Mock(side_effect=create_or_update_resource_success))
@patch.object(requests, 'patch', Mock(side_effect=mailchimp_response_failure_with_200))
@patch.object(requests, 'get', Mock(side_effect=raise_on_request))
def test_updating_interests_mailchimp_error(default_shop, valid_test_configuration_with_store):
    configuration.set(default_shop, MC_ENABLED, True)
    company = create_random_company()
    company.email = "valid@example.com"
    company.marketing_permission = True
    company.save()

    order = create_empty_order(shop=default_shop)
    order.customer = company
    order.save()

    assert MailchimpContact.objects.count() == 0
    update_or_create_contact(company.__class__, company)
    mailchimp_contact = MailchimpContact.objects.get(shop=default_shop, contact=company)
    assert mailchimp_contact.log_entries.filter(identifier="response_error").exists()
    assert mailchimp_contact.latest_push_failed
