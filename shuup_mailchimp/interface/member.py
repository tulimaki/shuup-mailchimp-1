# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from mailchimp3.baseapi import BaseApi


class ShuupMember(BaseApi):
    """
    Extension into mailchimp3 package to handle Mailchimp API v3.0 Member update or create

    http://developer.mailchimp.com/documentation/mailchimp/reference/lists/members/#edit-put_lists_list_id_members_subscriber_hash
    """
    def __init__(self, *args, **kwargs):
        super(ShuupMember, self).__init__(*args, **kwargs)
        self.endpoint = 'lists'

    def update_or_create(self, list_id, member_id, data):
        """
        updates an existing list member.
        """
        return self._mc_client._put(url=self._build_path(list_id, 'members', member_id), data=data)
