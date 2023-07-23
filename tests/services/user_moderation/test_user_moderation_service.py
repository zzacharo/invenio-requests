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

from invenio_requests.customizations.user_moderation import UserModeration
from invenio_requests.proxies import current_user_moderation_service
from invenio_requests.services.user_moderation.errors import InvalidCreator


def test_request_moderation(app, es_clear, users, identity_simple):
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


def test_search_moderation(app, es_clear, users, submit_request, mod_identity):
    """Tests the search for request moderation."""

    user = users[1]

    service = current_user_moderation_service

    request_item = service.request_moderation(
        system_identity, creator=system_user_id, topic=user.id
    )
    assert request_item

    # Create a generic request to test the user moderation search filter
    request = submit_request(system_identity, receiver=user)
    assert request

    # The user can't see the moderation requests against him
    user_identity = get_identity(user)
    user_identity.provides.add(Need(method="system_role", value="authenticated_user"))
    search = service.search_moderation_requests(user_identity)
    assert search.total == 0

    # Moderator can see the request
    # TODO moderator is considered Receiver() or Sender() because UserModerationEntity grants that need
    # TODO however, search filters do not allow the moderator to see the requests.
    # TODO either UserModeration() is added to can_search (for the query filter 'match_all' to be added)
    # TODO or the user_moderation should be its own service (add a lot of boilerplate, however we have more control)
    # search = service.search_moderation_requests(mod_identity)
    # assert search.total == 1

    # System process can see the request
    search = service.search_moderation_requests(system_identity)
    assert search.total == 1

    hits = search.to_dict()["hits"]["hits"]
    hit = hits[0]
    assert hit["topic"]["user"] == str(user.id)
    assert hit["type"] == service.request_type_cls.type_id


def test_moderation(app, es_clear, users, mod_identity):
    """Tests the service for moderation."""
    user = users[0]

    service = current_user_moderation_service

    request_item = service.request_moderation(
        system_identity, creator=system_user_id, topic=user.id
    )
    assert request_item
    assert request_item._request.status == "submitted"

    # Test accept then reject
    service.moderate(mod_identity, request_id=request_item.id, action="accept")
    req_read = service.read(mod_identity, request_item.id)
    assert req_read._request.status == "accepted"

    service.moderate(mod_identity, request_id=request_item.id, action="decline")
    req_read = service.read(mod_identity, request_item.id)
    assert req_read._request.status == "declined"

    # Test rejected->acepted transition
    service.moderate(mod_identity, request_id=request_item.id, action="accept")
    req_read = service.read(mod_identity, request_item.id)
    assert req_read._request.status == "accepted"
