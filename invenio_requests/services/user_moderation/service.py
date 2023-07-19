# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation service."""

from invenio_access.permissions import system_identity, system_user_id
from invenio_i18n import gettext as _

from invenio_requests.customizations.user_moderation.user_moderation import (
    UserModeration,
)
from invenio_requests.resolvers.registry import ResolverRegistry
from invenio_requests.services.user_moderation.errors import InvalidCreator


class UserModerationRequestService:
    """Service for User Moderation requests."""

    def __init__(self, requests_service):
        """Service initialisation as a sub-service of requests."""
        self.requests_service = requests_service

    @property
    def request_type_cls(self):
        """User moderation request type."""
        return UserModeration

    # /users/moderation action="block"

    # service.moderate(identity, user, action)
    #    get user request
    #    request_service.execute_action(identity, action=action)

    def request_moderation(
        self, identity, creator, topic, data=None, uow=None, **kwargs
    ):
        """Creates a UserModeration request and submits it."""
        if creator != system_user_id:
            raise InvalidCreator("Moderation request creator can only be system.")

        data = data or {}

        # For user moderation, topic is the user to be moderated
        topic = ResolverRegistry.resolve_entity_proxy({"user": topic}).resolve()

        receiver = {"user": system_user_id}

        creator = {"user": creator}

        request_item = self.requests_service.create(
            identity,
            data,
            self.request_type_cls,
            receiver,
            creator,
            topic=topic,
        )

        return self.requests_service.execute_action(
            identity=identity,
            id_=request_item.id,
            action="submit",
            data=data,
        )

    def search_moderation_requests(self, identity, params=None):
        """Searchs for user moderation requests.

        Returns only requests that concern the current user.
        """
        params = params or {}

        # Search for UserModeration requests only
        q = f"type:{self.request_type_cls.type_id}"
        return self.requests_service.search_user_requests(identity, q=q, params=params)
