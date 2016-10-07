# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup_mailchimp"
    provides = {
        "admin_module": ["shuup_mailchimp.admin:MailchimpAdminModule"],
        "admin_shop_form_part": [
            "shuup_mailchimp.admin.forms:ConfigurationFormPart"
        ],
        "xtheme_plugin": ["shuup_mailchimp.plugins:NewsletterPlugin"],
        "front_urls": [
            "shuup_mailchimp.urls:urlpatterns"
        ],
    }

    def ready(self):
        from django.db.models.signals import post_save
        from shuup.core.models import CompanyContact, PersonContact
        from shuup.core.order_creator.signals import order_creator_finished

        from shuup_mailchimp.configuration_keys import (
            MC_CONTACT_SIGNAL_DISPATCH_UID, MC_ORDER_SIGNAL_DISPATCH_UID
        )
        from shuup_mailchimp.interface import (
            update_or_create_contact, update_or_create_contact_from_order
        )
        post_save.connect(update_or_create_contact, sender=CompanyContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
        post_save.connect(update_or_create_contact, sender=PersonContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
        order_creator_finished.connect(update_or_create_contact_from_order, dispatch_uid=MC_ORDER_SIGNAL_DISPATCH_UID)
