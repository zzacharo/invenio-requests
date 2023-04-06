# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2022 TU Wien.
# Copyright (C) 2021 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resolver and proxy for requests."""

from invenio_records_resources.references.entity_resolvers import (
    RecordPKProxy,
    RecordResolver,
)
from ..records.api import Request, RequestEvent
from ..services import RequestsServiceConfig, RequestEventsServiceConfig


class RequestResolver(RecordResolver):
    """Resolver for requests."""

    type_id = "request"

    def __init__(self):
        """Initialize the default record resolver."""
        super().__init__(
            record_cls=Request,
            # TODO: The request service is not reegistered in the service registry
            service_id=RequestsServiceConfig.service_id,
            type_key=self.type_id,
            proxy_cls=RecordPKProxy,
        )

    def _reference_entity(self, entity):
        """Create a reference dict for the given request."""
        id_ = entity.number if entity.number is not None else entity.id
        return {"request": str(id_)}


class RequestEventResolver(RecordResolver):
    """Resolver for requests."""

    type_id = "request_event"

    def __init__(self):
        """Initialize the default record resolver."""
        super().__init__(
            record_cls=RequestEvent,
            # TODO: The request service is not reegistered in the service registry
            service_id=RequestEventsServiceConfig.service_id,
            type_key=self.type_id,
            proxy_cls=RecordPKProxy,
        )

    def _reference_entity(self, entity):
        """Create a reference dict for the given request."""
        return {self.type_key: str(entity.id)}
