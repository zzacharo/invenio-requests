# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 CERN.
# Copyright (C) 2021-2022 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""User moderation resource."""


from copy import deepcopy

from flask import current_app, g
from flask_resources import (
    from_conf,
    request_body_parser,
    resource_requestctx,
    response_handler,
    route,
)
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.resources.records.resource import (
    request_extra_args,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference


#
# Resource
#
class UserModerationResource(RecordResource):
    """Resource for user moderation requests."""

    data_parser = request_body_parser(
        parsers=from_conf("request_body_parsers"),
        default_content_type=from_conf("default_content_type"),
    )

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes

        return [
            route("GET", routes["list"], self.search),
            route("POST", routes["list"], self.moderate),
        ]

    @data_parser
    @response_handler(many=True)
    def moderate(self):
        """
        POST /api/moderation - Bulk accept / decline.

        {
            "request_id": "32131"
            "action": "accept|decline" # perhaps need 4 actions for pending -> approve, pending -> block, block -> approve, approve -> block
        }
        """
        data = deepcopy(resource_requestctx.data) if resource_requestctx.data else {}
        request_id = data.get("request_id")
        action = data.get("action")
        self.service.moderate(identity=g.identity, request_id=request_id, action=action)

        return "", 200

    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the items."""
        hits = self.service.search_moderation_requests(
            identity=g.identity,
            params=resource_requestctx.args,
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200
