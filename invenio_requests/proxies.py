# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for generic and customizable requests."""

from flask import current_app
from werkzeug.local import LocalProxy


current_requests = LocalProxy(
    lambda: current_app.extensions['invenio-requests']
)
"""Helper proxy to get the current RDM-Records extension."""
