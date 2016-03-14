# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.utils.translation import ugettext as _

from shoop.core.models import Shop
from shoop_mailchimp.interface import (get_or_create_store_id_for_shop,
                                       get_store_id, update_or_create_contacts)


def configurations_test(request, shop_pk):
    if not get_store_id(Shop.objects.get(pk=shop_pk)):
        return JsonResponse({"message": _("Testing configuration failed")}, status=400)
    return JsonResponse({"message": _("Configuration test successful")})


def initialize_store(request, shop_pk):
    if not get_or_create_store_id_for_shop(Shop.objects.get(pk=shop_pk)):
        return JsonResponse({"message": _("Initializing shop failed")}, status=400)
    return JsonResponse({"message": _("Integration initialized")})


def update_contacts(request, shop_pk):
    update_or_create_contacts(Shop.objects.get(pk=shop_pk))
    return JsonResponse({"message": _("Contacts updated")})
