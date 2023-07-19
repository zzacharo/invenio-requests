# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test user moderation service."""

import pytest
from flask_principal import Need
from invenio_access.permissions import system_identity, system_user_id
from invenio_access.utils import get_identity

from invenio_requests.proxies import current_user_moderation_service
from invenio_requests.services.user_moderation.errors import InvalidCreator


def test_request_moderation(app, users, identity_simple):
    """Tests the service for request moderation."""

    user = users[0]

    service = current_user_moderation_service

    # Use system identity
    request_item = service.request_moderation(
        system_identity, creator=system_user_id, topic=user.id
    )
    assert request_item
    # Request moderation creates and submits the moderation request
    assert request_item._request.status == "submitted"

    # User identity is not allowed to submit moderation requests
    with pytest.raises(Exception):
        service.request_moderation(
            identity_simple, creator=system_user_id, topic=user.id
        )

    # Only system user id can be the creator
    with pytest.raises(InvalidCreator):
        service.request_moderation(system_identity, creator=user.id, topic=user.id)


def test_search_moderation(app, users, submit_request):
    """Tests the search for request moderation."""

    user = users[1]

    service = current_user_moderation_service

    request_item = service.request_moderation(
        system_identity, creator=system_user_id, topic=user.id
    )
    assert request_item

    # Retrieve user requests (user has to be authenticated user)
    user_identity = get_identity(user)
    user_identity.provides.add(Need(method="system_role", value="authenticated_user"))

    # Create a generic request to test the user moderation search filter
    request = submit_request(user_identity, receiver=users[2])
    assert request

    # Should only return one request (user moderation)
    search = service.search_moderation_requests(user_identity)
    assert search.total == 1

    hits = search.to_dict()["hits"]["hits"]
    hit = hits[0]
    assert hit["topic"]["user"] == str(user.id)
    assert hit["type"] == service.request_type_cls.type_id
