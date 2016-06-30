# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_mailchimp.interface.utils.contacts import (
    add_email_to_list, update_or_create_contact,
    update_or_create_contact_from_order
)
from shuup_mailchimp.interface.utils.testing import interface_test

__all__ = [
    "add_email_to_list",
    "update_or_create_contact",
    "update_or_create_contact_from_order",
    "interface_test"
]
