# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests service."""

from .config import UserModerationServiceConfig
from .service import UserModerationRequestService

__all__ = ("UserModerationRequestService", "UserModerationServiceConfig")
