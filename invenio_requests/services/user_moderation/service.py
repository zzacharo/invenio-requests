# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation service."""
from flask import current_app

from invenio_access.permissions import system_user_id
from invenio_i18n import gettext as _
from invenio_records_resources.services import Service
from invenio_search.engine import dsl

from invenio_requests.customizations.user_moderation.user_moderation import (
    UserModeration,
)
from invenio_requests.proxies import current_request_type_registry
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
        return current_request_type_registry.lookup(UserModeration.type_id)

    def read(self, identity, request_id, **kwargs):
        """Proxy read request."""
        # TODO NOT NEEDED

        return self.requests_service.read(identity=identity, id_=request_id, **kwargs)

    def moderate(self, identity, request_id, action, data=None):
        """Moderates a user."""
        # TODO NOT NEEDED
        return self.requests_service.execute_action(
            identity=identity,
            id_=request_id,
            action=action,
            data=data,
        )

    def request_moderation(
        self, identity, creator, topic, data=None, uow=None, **kwargs
    ):
        """Creates a UserModeration request and submits it."""
        if creator != system_user_id:
            raise InvalidCreator(_("Moderation request creator can only be system."))

        data = data or {}

        # For user moderation, topic is the user to be moderated
        topic = {"user": str(topic)}

        # Receiver can be configured, by default send the request to users with moderation role
        default_receiver = {"role": "administration-moderation"}
        receiver = current_app.config.get(
            "REQUESTS_USER_MODERATION_RECEIVER", default_receiver
        )

        creator = {"role": "administration-moderation"}

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

    def search_moderation_requests(self, identity, params=None, expand=False):
        """Searchs for user moderation requests."""
        # Check moderator permissions
        params = params or {}

        # Search for UserModeration requests only
        user_mod_only_q = dsl.Q(
            "bool",
            should=[
                dsl.Q("term", **{"type": self.request_type_cls.type_id}),
            ],
            minimum_should_match=1,
        )

        extra_filter = user_mod_only_q
        # permission_action is set to None so the user can see all the requests. Permission is checked by user moderation service.
        return self.requests_service.search(
            identity,
            extra_filter=extra_filter,
            params=params,
            expand=expand,
        )
