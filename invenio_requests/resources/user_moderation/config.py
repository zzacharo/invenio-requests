# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""User moderation resource config."""


from flask_resources import HTTPJSONException, create_error_handler
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from marshmallow import fields

from ...errors import CannotExecuteActionError, NoSuchActionError
from ..requests.fields import ReferenceString


#
# Request args
#
class ModerationSearchArgsSchema(SearchRequestArgsSchema):
    """Add parameter to parse tags."""

    created_by = ReferenceString()
    topic = ReferenceString()
    receiver = ReferenceString()
    is_open = fields.Boolean()


#
# Resource config
#
class UserModerationResourceConfig(RecordResourceConfig):
    """Requests resource configuration."""

    blueprint_name = "user_moderation"
    url_prefix = "/user/moderation"
    routes = {
        "list": "/",
    }

    request_view_args = {}

    request_search_args = ModerationSearchArgsSchema

    error_handlers = {
        CannotExecuteActionError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
        NoSuchActionError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=str(e),
            )
        ),
    }
