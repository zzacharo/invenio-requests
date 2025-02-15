# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Requests service configuration."""

from invenio_records_resources.services import RecordServiceConfig, SearchOptions
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    FromConfigSearchOptions,
    SearchOptionsMixin,
)
from invenio_records_resources.services.records.links import pagination_links

from invenio_requests.services.requests import facets

from ...customizations import RequestActions
from ...records.api import Request
from ..permissions import PermissionPolicy
from .components import (
    EntityReferencesComponent,
    RequestDataComponent,
    RequestNumberComponent,
    RequestPayloadComponent,
)
from .links import RequestLink
from .params import IsOpenParam, IsSharedWithMeParam, ReferenceFilterParam
from .results import RequestItem, RequestList


def _is_action_available(request, context):
    """Check if the given action is available on the request."""
    action = context.get("action")
    identity = context.get("identity")
    permission_policy_cls = context.get("permission_policy_cls")
    permission = permission_policy_cls(f"action_{action}", request=request)
    return RequestActions.can_execute(request, action) and permission.allows(identity)


class RequestSearchOptions(SearchOptions, SearchOptionsMixin):
    """Search options."""

    params_interpreters_cls = SearchOptions.params_interpreters_cls + [
        ReferenceFilterParam.factory(param="created_by", field="created_by"),
        ReferenceFilterParam.factory(param="receiver", field="receiver"),
        ReferenceFilterParam.factory(param="topic", field="topic"),
        IsOpenParam.factory("is_open"),
    ]

    facets = {
        "type": facets.type,
        "status": facets.status,
    }


class UserRequestSearchOptions(RequestSearchOptions):
    """User request search options."""

    params_interpreters_cls = RequestSearchOptions.params_interpreters_cls + [
        IsSharedWithMeParam,
    ]


class RequestsServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    """Requests service configuration."""

    service_id = "requests"

    # common configuration
    permission_policy_cls = FromConfig(
        "REQUESTS_PERMISSION_POLICY", default=PermissionPolicy
    )
    result_item_cls = RequestItem
    result_list_cls = RequestList
    search = FromConfigSearchOptions(
        config_key="REQUESTS_SEARCH",
        sort_key="REQUESTS_SORT_OPTIONS",
        facet_key="REQUESTS_FACETS",
        search_option_cls=RequestSearchOptions,
    )

    # user requests search configuration
    search_user_requests = FromConfigSearchOptions(
        config_key="REQUESTS_SEARCH",
        sort_key="REQUESTS_SORT_OPTIONS",
        facet_key="REQUESTS_FACETS",
        search_option_cls=UserRequestSearchOptions,
    )

    # request-specific configuration
    record_cls = Request  # needed for model queries
    schema = None  # stored in the API classes, for customization
    indexer_queue_name = "requests"
    index_dumper = None

    # links configuration
    links_item = {
        "self": RequestLink("{+api}/requests/{id}"),
        "self_html": RequestLink("{+ui}/requests/{id}"),
        "comments": RequestLink("{+api}/requests/{id}/comments"),
        "timeline": RequestLink("{+api}/requests/{id}/timeline"),
    }
    links_search = pagination_links("{+api}/requests{?args*}")
    links_user_requests_search = pagination_links("{+api}/user/requests{?args*}")
    action_link = RequestLink(
        "{+api}/requests/{id}/actions/{action}", when=_is_action_available
    )

    payload_schema_cls = None

    # TODO: discuss conflict between this and custom request service.
    #  Does it create issues?
    components = FromConfig(
        "REQUESTS_SERVICE_COMPONENTS",
        default=[
            # Order of components is important!
            RequestPayloadComponent,
            RequestDataComponent,
            EntityReferencesComponent,
            RequestNumberComponent,
        ],
    )
