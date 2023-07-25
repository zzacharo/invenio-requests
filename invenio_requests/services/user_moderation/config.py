# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests permissions."""
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    ServiceConfig,
)

from invenio_requests.services.permissions import UserModerationPermissionPolicy


class UserModerationServiceConfig(ServiceConfig, ConfiguratorMixin):
    """Service config."""

    service_id = "user-moderation"
    permission_policy_cls = UserModerationPermissionPolicy
