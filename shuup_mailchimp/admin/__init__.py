# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from shuup.admin.base import AdminModule
from shuup.admin.utils.urls import admin_url


class MailchimpAdminModule(AdminModule):
    name = _("Mailchimp")

    def get_urls(self):
        return [
            admin_url(
                "^mailchimp/configurations_test/(?P<shop_pk>\d+)/$",
                "shuup_mailchimp.admin.views.configurations_test",
                name="mailchimp.configurations_test"
            ),
        ]
