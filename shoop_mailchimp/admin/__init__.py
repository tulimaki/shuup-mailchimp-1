# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from shoop.admin.base import AdminModule
from shoop.admin.utils.urls import admin_url


class MailchimpAdminModule(AdminModule):
    name = _("Mailchimp")

    def get_urls(self):
        return [
            admin_url(
                "^mailchimp/configurations_test/(?P<shop_pk>\d+)/$",
                "shoop_mailchimp.admin.views.configurations_test",
                name="mailchimp.configurations_test"
            ),
        ]
