# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Test user moderation resource."""

import pytest
from invenio_access.permissions import system_identity, system_user_id

from invenio_requests.proxies import current_user_moderation_service


@pytest.fixture()
def mod_request(app, users):
    user = users[0]
    service = current_user_moderation_service

    request_item = service.request_moderation(
        system_identity, creator=system_user_id, topic=user.id
    )
    assert request_item

    return request_item


def test_moderate(app, es_clear, client_logged_as, headers, mod_request):
    # Log as moderator
    client = client_logged_as("mod@example.org")

    response = client.post(
        "/user/moderation/",
        headers=headers,
        json={"action": "accept", "request_id": mod_request.id},
    )
    assert response.status_code == 200

    response = client.get(
        "/user/moderation/",
        headers=headers,
    )
    assert response.status_code == 200
    hits = response.json["hits"]["hits"]
    assert len(hits) == 1
    assert hits[0]["status"] == "accepted"

    # Decline after accepting
    response = client.post(
        "/user/moderation/",
        headers=headers,
        json={"action": "decline", "request_id": mod_request.id},
    )
    assert response.status_code == 200

    response = client.get(
        "/user/moderation/",
        headers=headers,
    )
    assert response.status_code == 200
    hits = response.json["hits"]["hits"]
    assert len(hits) == 1
    assert hits[0]["status"] == "declined"


@pytest.mark.parametrize(
    "invalid_action,expected_code",
    [
        ("accept", 403),
        ("decline", 403),
    ],
)
def test_moderate_invalid_user(
    app, es_clear, client_logged_as, headers, mod_request, invalid_action, expected_code
):
    """Tests that a regular user can't moderate."""
    # Log as a normal user that can't moderate
    client = client_logged_as("user1@example.org")
    response = client.post(
        "/user/moderation/",
        headers=headers,
        json={"action": invalid_action, "request_id": mod_request.id},
    )
    assert response.status_code == expected_code


@pytest.mark.parametrize(
    "invalid_action,expected_code",
    [
        ("delete", 403),  # invalid action but only system can delete
        ("cancel", 400),  # invalid state transition
        ("submit", 400),  # invalid state transition
        (
            "create",
            403,
        ),  # the action should be invalid and return 400. However, 'authenticated_user' action need is not being considered by the permission policy. Perhaps there's an issue with the tests
        ("invalid", 400),  # action does not exist
    ],
)
def test_invalid_actions_after_submit(
    app, es_clear, client_logged_as, headers, mod_request, invalid_action, expected_code
):
    """Test invalid actions on a user moderation request.

    After created, moderation requests are submitted. Therefore, some actions are not allowed (e.g. 'cancel' and 'submit').
    Other actions are not permitted for a regular user (e.g 'delete' and 'create').
    Permissions are checked first, actions after. Therefore, 'create' is an invalid action but the user does not have permissions. Therefore,
    the resource returns a HTTP 403 Forbidden instead of a HTTP 400 Bad Request.
    """
    # Log as moderator
    client = client_logged_as("mod@example.org")

    # Execute good action (accept)
    response = client.post(
        "/user/moderation/",
        headers=headers,
        json={"action": "accept", "request_id": mod_request.id},
    )

    # Execute invalid actions after accepting
    response = client.post(
        "/user/moderation/",
        headers=headers,
        json={"action": invalid_action, "request_id": mod_request.id},
    )
    assert response.status_code == expected_code


def test_search_as_moderator(app, es_clear, client_logged_as, headers, mod_request):
    """Test search as a moderator."""
    # Log as moderator
    mod_email = "mod@example.org"
    client = client_logged_as(mod_email)

    response = client.get(
        "/user/moderation/",
        headers=headers,
    )
    assert response.status_code == 200
    hits = response.json["hits"]["hits"]
    assert len(hits) == 1
    hit = hits[0]
    assert hit["type"] == "user-moderation"
    assert hit["status"] == "submitted"


def test_search_as_user(app, es_clear, client_logged_as, headers, mod_request):
    """Test search as a regular user."""
    client = client_logged_as("user1@example.org")

    response = client.get(
        "/user/moderation/",
        headers=headers,
    )
    assert response.status_code == 200
    hits = response.json["hits"]["hits"]
    assert len(hits) == 0


def test_links(app, es_clear, client_logged_as, headers, mod_request):
    """Test links on search."""
    # Log as moderator
    mod_email = "mod@example.org"
    client = client_logged_as(mod_email)

    response = client.get(
        "/user/moderation/",
        headers=headers,
    )
    assert response.status_code == 200
    hits = response.json["hits"]["hits"]
    assert len(hits) == 1
    hit = hits[0]
    assert hit["type"] == "user-moderation"
    assert hit["status"] == "submitted"
    links = hit["links"]
    assert set(["accept", "cancel", "decline"]) <= set(links["actions"])

    # TODO
    # # Decline and check links again
    # response = client.post(
    #     links["actions"]["decline"],
    #     headers=headers,
    # )
    # assert response.status_code == 200

    # response = client.get(
    #     "/user/moderation/",
    #     headers=headers,
    # )
    # assert response.status_code == 200
    # hits = response.json["hits"]["hits"]
    # assert len(hits) == 1
    # hit = hits[0]
    # links = hit["links"]
    # breakpoint()
    # # Actions are not allowed anymore
    # assert set(["accept", "cancel", "decline"]) > set(links["actions"])


# TODO test search filters, facets, sorting
