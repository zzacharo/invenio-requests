# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""API classes for requests in Invenio."""

from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.dumpers import ElasticsearchDumper
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField, PIDField

from .actions import RequestAction
from .models import RequestMetadata


class Request(Record):
    """A generic request record."""

    model_cls = RequestMetadata

    dumper = ElasticsearchDumper(
        extensions=[
            # TODO
        ]
    )

    # TODO figure out aliases, multiple mappings, common search fields
    index = IndexField("requests-requests-v1.0.0", search_alias="requests")

    schema = ConstantField("$schema", "local://requests/request-v1.0.0.json")

    request_type = ConstantField("request_type", "Generic Request")
    """The human-readable request type."""

    pid = PIDField('id', provider=RecordIdProviderV2)

    # TODO systemfield?
    @property
    def is_open(self):
        # TODO define (overridable) enum of allowed states for the class
        #      along with info if that's an open state
        #      maybe a dictionary? {"open": True, "closed": False, "rejected": False}
        return self.state == "open"

    available_actions = {
        "accept": RequestAction,
        "cancel": RequestAction,
        "decline": RequestAction,
    }

    def get_action(self, action_name):
        return self.available_actions[action_name](self)

    def execute_action(self, action_name):
        return self.get_action(action_name).execute()
