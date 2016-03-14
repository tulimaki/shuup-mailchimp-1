# This file is part of Shoop.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

class PostIsNotAllowed(Exception):
    pass


def raise_on_request(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url
            self.data = kwargs.get("json")
            assert self.data is not None
            self.status_code = 500

        def json(self):
            raise PostIsNotAllowed("Post is not allowed!")
    return MockedResponse(url, **kwargs)


def get_empty_list(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url

        def json(self):
            return {"id": "some_list_id", "stats": {"member_count": 0}}
    return MockedResponse(url, **kwargs)


def get_non_empty_list(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url

        def json(self):
            return {"id": "some_list_id", "stats": {"member_count": 43}}
    return MockedResponse(url, **kwargs)


def create_store_success(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url
            self.data = kwargs.get("json")
            assert self.data is not None
            self.status_code =200

        def json(self):
            return {"id": self.data.get("id")}
    return MockedResponse(url, **kwargs)


def create_or_update_resource_success(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url
            self.data = kwargs.get("json")
            assert self.data is not None
            self.status_code = 200

        def json(self):
            return {"id": self.data.get("id") or 123}  # data does not have id, but actual Mailchimp does
    return MockedResponse(url, **kwargs)


def mailchimp_response_failure_with_200(url, **kwargs):
    class MockedResponse:
        def __init__(self, url, **kwargs):
            self.url = url
            self.data = kwargs.get("json")
            assert self.data is not None
            self.status_code = 200

        def json(self):
            return {"title": "failure", "detail": "Some failure description"}
    return MockedResponse(url, **kwargs)
