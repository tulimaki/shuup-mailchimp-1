# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from requests import ConnectionError

from shoop_mailchimp.interface.base import ShoopMailchimp


def interface_test(shop):
    client = ShoopMailchimp(shop)

    try:
        results = client.get_list()
    except ConnectionError:
        return False

    status = None
    if results:
        status = results.get("status", None)
    return False if (status and status != 200) else bool(results)
