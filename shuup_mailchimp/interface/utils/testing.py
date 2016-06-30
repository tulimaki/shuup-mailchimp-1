# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from requests import ConnectionError

from shuup_mailchimp.interface.base import ShuupMailchimp


def interface_test(shop):
    client = ShuupMailchimp(shop)

    try:
        results = client.get_list()
    except ConnectionError:
        return False

    status = None
    if results:
        status = results.get("status", None)
    return False if (status and status != 200) else bool(results)
