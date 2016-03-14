# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from shoop import configuration
from shoop.admin.form_part import FormPart, TemplatedFormDef
from shoop_mailchimp.configuration_keys import (
    MC_API, MC_ENABLED, MC_LIST_ID,MC_STORE_ID, MC_USERNAME
)
from six import iteritems

from shoop_mailchimp.models import MailchimpContact


FORM_FIELD_TO_CONF_KEY_MAP = {
    "api_key": MC_API,
    "list_id": MC_LIST_ID,
    "is_enabled": MC_ENABLED,
    "store_id": MC_STORE_ID,
    "username": MC_USERNAME
}


class ConfigurationForm(forms.Form):
    api_key = forms.CharField(label=_("Mailchimp API key"), max_length=160, required=False)
    list_id = forms.CharField(
        label=_("Mailchimp list id"),
        max_length=24,
        required=False)
    store_id = forms.CharField(
        label=_("Mailchimp store id"),
        max_length=24,
        required=False)
    is_enabled = forms.BooleanField(label=_("Enabled"), required=False)
    username = forms.CharField(label=_("Mailchimp username"), max_length=160, required=False)

    def __init__(self, **kwargs):
        self.shop = kwargs.pop("shop")
        super(ConfigurationForm, self).__init__(**kwargs)
        for form_field, conf_key in iteritems(FORM_FIELD_TO_CONF_KEY_MAP):
            self.initial[form_field] = configuration.get(self.shop, conf_key)

    def show_instructions(self):
        required_configurations = [MC_API, MC_LIST_ID, MC_USERNAME]
        return not all([configuration.get(self.shop, conf) for conf in required_configurations])

    def can_initialize(self):
        required_configurations = [MC_API, MC_LIST_ID, MC_USERNAME]
        store_id = configuration.get(self.shop, MC_STORE_ID)
        return all([configuration.get(self.shop, conf) for conf in required_configurations]) and not store_id

    def has_store_id(self):
        return bool(configuration.get(self.shop, MC_STORE_ID))

    def can_update_contacts(self):
        return MailchimpContact.objects.filter(shop=self.shop, latest_push_failed=True).exists()

    def save(self):
        if not self.changed_data:
            return
        for form_field, conf_key in iteritems(FORM_FIELD_TO_CONF_KEY_MAP):
            configuration.set(self.shop, conf_key, self.cleaned_data.get(form_field))


class ConfigurationFormPart(FormPart):
    priority = 5
    name = "mailchimp"
    form = ConfigurationForm

    def get_form_defs(self):
        yield TemplatedFormDef(
            name=self.name,
            form_class=self.form,
            template_name="shoop_mailchimp/admin/config_form_part.jinja",
            required=False,
            kwargs={"shop": self.object}
        )

    def form_valid(self, form):
        form["mailchimp"].save()
