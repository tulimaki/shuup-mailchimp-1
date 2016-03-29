# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from mailchimp3 import MailChimp

from shoop_mailchimp.interface.member import ShoopMember


class ShoopMailchimpClient(MailChimp):
    """
    mailchimp3.Mailchimp with extended ShoopMember functionality
    """
    def __init__(self, *args, **kwargs):
        super(ShoopMailchimpClient, self).__init__(*args, **kwargs)
        self.shoop_member = ShoopMember(self)
