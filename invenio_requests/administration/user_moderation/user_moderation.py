# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""Invenio administration view module for user moderation."""
from flask import current_app
from invenio_administration.views.base import AdminView, AdminResourceListView
from marshmallow import Schema

# Custom view
# class UserModerationListView(AdminView):
#     """Search admin view."""

#     name = "user_moderation"
#     category = "Moderation"
#     template = "invenio_requests/administration/user_moderation.html"
#     url = "/moderation"
#     menu_label = "Users"
#     icon = "user"
#     # TODO title not allowed?

#     @staticmethod
#     def disabled():
#         """Disable the view on demand."""
#         # TODO permissions?
#         # return current_app.config["COMMUNITIES_ADMINISTRATION_DISABLED"]
#         return False


class UserModerationListView(AdminResourceListView):
    api_endpoint = "/requests"
    name = "moderation"
    resource_config = "requests_resource"
    search_request_headers = {"Accept": "application/json"}
    title = "Moderation"
    menu_label = "Users"
    category = "Moderation"
    pid_path = "id"
    icon = "users"
    template = "invenio_requests/administration/user_moderation.html"

    display_search = True
    display_delete = False
    display_create = False
    display_edit = False

    item_field_list = {
        "id": {
            "text": "ID",
            "order": 1,
        },
        "topic.user": {
            "text": "User",
            "order": 3,
        },  # TODO we should resolve the user. But this is fetched from the API.
        # TODO can we dereference somehow?
        "created": {"text": "Created", "order": 2},
        "is_open": {"text": "Open", "order": 4}
    }

    actions = {
        "accept": {
            "text": "Approve",
            "payload_schema": None,
            "order": 1,
        },
        "decline": {
            "text": "Block",
            "payload_schema": None,
            "order": 1,
        },
    }
    search_config_name = "REQUESTS_USER_MODERATION_SEARCH"
    search_facets_config_name = "REQUESTS_USER_MODERATION_FACETS"
    search_sort_config_name = "REQUESTS_USER_MODERATION_SORT_OPTIONS"

    @property
    def request_type(self):
        """Request type property."""
        request_type = self.resource.service.request_type_registry.lookup(
            "user-moderation"
        )
        return request_type

    def get_api_endpoint(self):
        """Get search API endpoint.

        Filters only 'user-moderation' requests.
        """
        api_url_prefix = current_app.config["SITE_API_URL"]
        slash_tpl = "/" if not self.api_endpoint.startswith("/") else ""

        filter_q = f"type:{self.request_type.type_id}"
        if not self.api_endpoint.startswith(api_url_prefix):
            return f"{api_url_prefix}{slash_tpl}{self.api_endpoint}?q={filter_q}"

        return f"{slash_tpl}{self.api_endpoint}?q={filter_q}"

    @classmethod
    def get_service_schema(cls):
        """Get marshmallow schema of the assigned service."""
        request_type = cls.resource.service.request_type_registry.lookup(
            "user-moderation"
        )
        schema = request_type.marshmallow_schema()
        # TODO type(schema) == GeneratedSchema and only has ``_declared_fields``, not ``fields``
        setattr(schema, "fields", schema._declared_fields)
        return schema

    @staticmethod
    def disabled():
        """Disable the view on demand."""
        return False
        # return current_app.config["COMMUNITIES_ADMINISTRATION_DISABLED"]
