# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Search parameter interpreters for requests."""
from functools import partial
from opensearch_dsl import Q

from invenio_records_resources.services.records.params import (
    FilterParam,
    ParamInterpreter,
)

from ...resolvers.registry import ResolverRegistry


class ReferenceFilterParam(FilterParam):
    """Filter for reference dictionaries."""

    def __init__(self, param_name, field_name, config):
        """Constructor."""
        super().__init__(param_name, field_name, config)
        self._match_cache = {}

    def _is_valid(self, ref_type, ref_id):
        """Check if the reference dict is potentially resolvable."""
        if ref_type in self._match_cache:
            return self._match_cache[ref_type]

        # check if there's any resolver registered for the dict
        is_valid = any(
            (
                res.matches_reference_dict({ref_type: ref_id})
                for res in ResolverRegistry().get_registered_resolvers()
            )
        )
        self._match_cache[ref_type] = is_valid
        return is_valid

    def apply(self, identity, search, params):
        """Apply filter for a potentially resolvable reference dict."""
        if self.param_name not in params:
            return search

        ref_dict = params.pop(self.param_name, None)
        ref_type, ref_id = list(ref_dict.items())[0]

        # only apply the filter if it is potentially resolvable
        if self._is_valid(ref_type, ref_id):
            field_name = f"{self.field_name}.{ref_type}"
            if isinstance(ref_id, str):
                search = search.filter("term", **{field_name: ref_id})
            else:
                search = search.filter("terms", **{field_name: ref_id})

        return search


class IsOpenParam(ParamInterpreter):
    """Evaluates the 'is_open' parameter."""

    def __init__(self, field_name, config):
        """Construct."""
        self.field_name = field_name
        super().__init__(config)

    @classmethod
    def factory(cls, field):
        """Create a new filter parameter."""
        return partial(cls, field)

    def apply(self, identity, search, params):
        """Evaluate the is_open parameter on the search."""
        if params.get("is_open") is True:
            search = search.filter("term", **{self.field_name: True})
        elif params.get("is_open") is False:
            search = search.filter("term", **{self.field_name: False})
        return search


class IsSharedWithMeParam(ParamInterpreter):
    """Evaluates the 'shared_with_me' parameter."""

    def apply(self, identity, search, params):
        """Evaluate the shared_with_me parameter on the search."""
        created_by = "created_by.user"
        receiver = "receiver.user"
        my_requests_q = Q(
            "bool",
            should=[
                Q("term", **{created_by: identity.id}),
                Q("term", **{receiver: identity.id}),
            ],
        )
        if params.get("shared_with_me") is True:
            # Shared with me
            search = search.filter(~my_requests_q)
        elif params.get("shared_with_me") is False:
            # My requests
            search = search.filter(my_requests_q)

        return search
